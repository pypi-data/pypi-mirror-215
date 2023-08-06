import ast
import functools
import re
from re import Match, Pattern
from typing import Any, Optional, Self, cast, overload

from .core import LocationArea, LocationRange, Position
from .value import LocatedValue


class LocatedString(str, LocatedValue[str]):
  def __new__(cls, value: str, *args, **kwargs):
    return super(LocatedString, cls).__new__(cls, value)

  @overload
  def __init__(self, value: str, area: LocationArea, *, symbolic: bool = False):
    ...

  @overload
  def __init__(self, value: Self | str, /):
    ...

  def __init__(self, value: Self | str, area: Optional[LocationArea] = None, *, symbolic: bool = False):
    if area is not None:
      LocatedValue.__init__(self, value, area)
    elif hasattr(value, 'area'):
      LocatedValue.__init__(self, value.value, value.area) # type: ignore
    # elif isinstance(value, LocatedString):
    #   LocatedValue.__init__(self, value.value, value.area)
    else:
      LocatedValue.__init__(self, value, Source(value).area)

    self.symbolic = symbolic

  # Overriden methods

  def __add__(self, other: Self | str, /):
    other_located = isinstance(other, LocatedString)

    return LocatedString(
      self.value + str(other),
      (self.area + other.area) if other_located else self.area,
      symbolic=(self.symbolic or (other_located and other.symbolic))
    )

  def __radd__(self, other: Self, /):
    return self + other

  def __getitem__(self, key: int | slice, /) -> 'LocatedString':
    if isinstance(key, slice):
      if self.symbolic:
        return LocatedString(self.value[key], self.area, symbolic=True)
      else:
        start, stop, step = key.indices(len(self))
        return LocatedString(self.value[key], self.area % (start, stop))
    else:
      return self[key:(key + 1)] if key >= 0 else self[key:((key - 1) if key < -1 else None)]

  def split(self, sep: Optional[str], maxsplit: int = -1):
    if sep is None:
      raise Exception("Not supported")

    index = 0

    def it(frag: str):
      nonlocal index

      value = self[index:(index + len(frag))]
      index += len(frag) + len(sep)
      return value

    fragments = self.value.split(sep, maxsplit)
    return [it(frag) for frag in fragments]

  def splitlines(self, keepends: bool = False):
    indices = [index for index, char in enumerate(self.value) if char == "\n"]
    return [self[((a + 1) if a is not None else a):((b + 1) if keepends and (b is not None) else b)] for a, b in zip([None, *indices], [*indices, None])]

  def strip(self, chars: Optional[str] = None):
    return self.lstrip(chars).rstrip(chars)

  def lstrip(self, chars: Optional[str] = None):
    stripped = self.value.lstrip(chars)
    return self[(len(self) - len(stripped)):]

  def rstrip(self, chars: Optional[str] = None):
    stripped = self.value.rstrip(chars)
    return self[0:len(stripped)]

  # New methods

  @functools.cached_property
  def _line_cumlengths(self):
    lengths = [0]

    for line in self.splitlines(keepends=True):
      lengths.append(lengths[-1] + len(line))

    return lengths

  def compute_ast_node_area(self, node: ast.expr | ast.stmt):
    assert not self.symbolic
    assert node.end_lineno is not None
    assert node.end_col_offset is not None

    start = self.get_location_from_position(Position(node.lineno - 1, node.col_offset))
    end = self.get_location_from_position(Position(node.end_lineno - 1, node.end_col_offset))

    return self.area % (start, end)

  def get_location_from_position(self, position: Position, /):
    return self._line_cumlengths[position.line] + position.column

  def index_ast_node(self, node: ast.expr, /):
    return LocatedString(self.value, area=self.compute_ast_node_area(node), symbolic=True)

  def index_syntax_error(self, err: SyntaxError, /):
    assert err.lineno is not None
    assert err.offset is not None
    assert err.end_lineno is not None
    assert err.end_offset is not None

    start = self.get_location_from_position(Position(err.lineno - 1, err.offset - 1))
    end = self.get_location_from_position(Position(err.end_lineno - 1, err.end_offset - 1))

    return self[start:end]

  def offset_position(self, offset: int, /):
    line = self.value[:offset].count("\n")
    column = (offset - self.value[:offset].rindex("\n") - 1) if line > 0 else offset

    return Position(line, column)

  def sub(self, pattern: str, repl: str, count: int = 0, flags: int = 0):
    output = LocatedString(str(), area=LocationArea([], source=self.source))
    last_offset = 0

    for match_index, match in enumerate(re.finditer(pattern, self, flags)):
      if (count > 0) and (match_index >= count):
        break

      loc_match = self.transform_match(match)
      span = match.span()
      output += self[last_offset:span[0]]
      last_offset = span[1]

      last_repl_offset = 0

      for repl_match in re.finditer(r"\\([1-9]\d*)|\\g<(\d*)>|\\g<([a-z]+)>", repl):
        repl_span = repl_match.span()
        output += repl[last_repl_offset:repl_span[0]].encode('utf-8').decode('unicode_escape')

        if ((group_id := repl_match.group(1)) is not None) or (group_id := repl_match.group(1) is not None):
          group = loc_match.group(int(group_id))
          assert group
          output += group
        elif (group_name := repl_match.group(2)) is not None:
          group = loc_match.group(group_name)
          assert group
          output += group

        last_repl_offset = repl_span[1]

      output += repl[last_repl_offset:].encode('utf-8').decode('unicode_escape')

    output += self[last_offset:]

    return output


  def match_re(self, pattern: Pattern | str, flags: int = 0):
    return self.transform_match(re.match(pattern, self, flags) if isinstance(pattern, str) else pattern.match(self, flags))

  def transform_match(self, match: Optional[Match[str]], /):
    return LocatedMatch(match, self) if match else None


class LocatedMatch:
  def __init__(self, match: Match[str], string: LocatedString):
    self._match = match
    self._string = string

  @functools.cached_property
  def area(self):
    return self.group().area

  def group(self, group: int | str = 0, /):
    span = self._match.span(group)

    if span[0] < 0:
      return cast(LocatedString, None)

    return self._string[span[0]:span[1]]

  def span(self, group: int | str = 0, /):
    return self._match.span(group)


class Source(LocatedString):
  def __init__(self, value: LocatedString | str, *, origin: Any = None):
    if isinstance(value, LocatedString):
      super().__init__(value.value, value.area)
    else:
      super().__init__(value, LocationArea([LocationRange(0, len(value), source=self)]))

    self.origin = origin


__all__ = (
  'LocatedMatch',
  'LocatedString',
  'Source'
)
