from dataclasses import dataclass
import functools
import math
from typing import TYPE_CHECKING, Optional, Self

if TYPE_CHECKING:
  from .string import Source


@dataclass(frozen=True)
class Position:
  """
  An immutable object describing a position in a source string using a (line, column) tuple.

  Both line and column start at 0.
  """

  line: int
  column: int


@dataclass(frozen=True)
class LocationRange:
  """
  An immutable object describing a continuous range of positions in a source string using two offsets.

  The start offset must be lower than or equal to the end offset. A range with equal start and end offsets is referred to as an _empty range_. The start offset is inclusive, while the end offset is exclusive.
  """

  start: int
  end: int
  source: 'Source'

  def __mod__(self, offset: tuple[int, int] | int):
    start, end = offset if isinstance(offset, tuple) else (offset, offset + 1)

    return LocationRange(
      source=self.source,
      start=(self.start + start),
      end=(self.start + end)
    )

  def __lt__(self, other: Self, /):
    return (self.start < other.start) or ((self.start == other.start) and (self.end < other.end))

  def __repr__(self):
    return f"{self.__class__.__name__}({self.start} -> {self.end})"

  @functools.cached_property
  def empty(self):
    """
    `True` if the range is empty.
    """

    return (self.start == self.end)

  @functools.cached_property
  def start_position(self):
    """
    A `Position` object representing the start of the range.
    """

    return self.source.offset_position(self.start)

  @functools.cached_property
  def end_position(self):
    """
    A `Position` object representing the end of the range.
    """

    return self.source.offset_position(self.end)


@dataclass
class LocationArea:
  """
  An immutable object describing a discontinuous set of continuous position ranges in a source string.

  The `ranges` attribute is a list of non-overlapping and sorted `LocationRange` objects.
  """

  ranges: list[LocationRange]
  source: 'Source'

  def __init__(self, ranges: list[LocationRange], source: Optional['Source'] = None):
    """
    Create a new `LocationArea` instance.

    Parameters
      ranges: A list of `LocationRange` objects, not necessarily non-overlapping nor sorted. May be empty. All ranges must have the same source.
      source: The `Source` object the area is associated with. Only required if the area is empty.
    """

    self.ranges = list[LocationRange]()

    for locrange in sorted(ranges):
      # TODO: Handle empty ranges

      if self.ranges and (self.ranges[-1].end >= locrange.start):
        self.ranges[-1] = LocationRange(
          source=self.ranges[-1].source,
          start=self.ranges[-1].start,
          end=max(self.ranges[-1].end, locrange.end)
        )
      else:
        self.ranges.append(locrange)

    if not self.empty:
      self.source = source if (source is not None) else self.ranges[0].source

      for locrange in self.ranges:
        if not(locrange.source is self.source):
          raise ValueError("All ranges must have the same source.")
    else:
      if source is None:
        raise TypeError("Empty location areas must have an explicit source.")

      self.source = source

  @property
  def continuous(self):
    """
    `True` if the area only contains a single range.
    """

    return len(self.ranges) == 1

  @property
  def empty(self):
    """
    `True` if the area doesn't contain any range.
    """

    return not self.ranges

  @functools.cached_property
  def enclosing_range(self):
    """
    Return a `LocationRange` object representing the smallest continuous range that contains all the ranges in the area.
    """

    return LocationRange(
      source=self.source,
      start=self.ranges[0].start,
      end=self.ranges[-1].end
    )

  def append(self, locrange: LocationRange, /):
    """
    Create a new `LocationArea` object with the given range appended to the area.
    """

    return self.__class__(self.ranges + [locrange], self.source)

  def single_range(self):
    """
    Return the single range in the area. Only applies if the area is continuous.
    """

    if not self.continuous:
      raise ValueError("The area is not continuous.")

    return self.ranges[0]

  def format(self):
    output = str()

    if not self.ranges:
      return output

    source = self.ranges[0].source
    lines_source = source.splitlines()

    lines_ranges = dict()

    for locrange in self.ranges:
      start = locrange.start_position
      end = locrange.end_position

      for line_index in range(start.line, end.line + (1 if end.column > 0 else 0)):
        if not (line_index in lines_ranges):
          lines_ranges[line_index] = list()

        lines_ranges[line_index].append(range(
          start.column if line_index == start.line else 0,
          end.column if line_index == end.line else len(lines_source[line_index]) + 1
        ))

    lines_list = sorted(lines_ranges.keys())

    width_line = math.ceil(math.log(lines_list[-1] + 2, 10))

    for index, line_index in enumerate(lines_list):
      line_source = lines_source[line_index]

      if (index > 0) and (line_index != (lines_list[index - 1] + 1)):
        output += "\n"

      output += f" {str(line_index + 1).rjust(width_line, ' ')} | {line_source}\n"

      if line_index in lines_ranges:
        line_ranges = lines_ranges[line_index]

        output += f" {' ' * width_line} | " + "".join(
          [("-" if column_index == len(line_source) else "^") if any(
            [column_index in line_range for line_range in line_ranges]
          ) else " " for column_index in range(0, len(line_source) + 1)
        ]) + "\n"

    return output

  def __add__(self, other: Self, /):
    """
    Return a new `LocationArea` object representing the union of the two areas.
    """

    # Check this here as it wouldn't be verified in the constructor if 'other' is empty.
    if other.source is not self.source:
      raise ValueError("Both areas must have the same source.")

    return self.__class__(self.ranges + other.ranges, self.source)

  def __mod__(self, offset: tuple[int, int] | int, /):
    """
    Create a subset of this area by indexing with the given offset, using the area's coordinate system.

    Parameters
      offset: A tuple of two integers representing the start and end of the subset, or a single integer representing the offset of a single character covered by the returned area. If a tuple is provided and the start offset is greather than or equal to the end offset, an empty area is returned.
    """

    start, end = offset if isinstance(offset, tuple) else (offset, offset + 1)

    index = 0
    ranges = list[LocationRange]()

    for locrange in self.ranges:
      range_start = index
      range_end = index + (locrange.end - locrange.start)

      delta_start = 0
      delta_end = 0

      if (start > range_start) and (start <= range_end):
        delta_start = range_start - start

      if (end >= range_start) and (end < range_end):
        delta_end = range_end - end

      if not ((end < range_start) or (start > range_end)):
        ranges.append(LocationRange(locrange.start - delta_start, locrange.end - delta_end, source=locrange.source))

      index += (locrange.end - locrange.start)

    return self.__class__(ranges, self.source)

  def __repr__(self):
    return f"{self.__class__.__name__}(" + ", ".join([f"{range.start} -> {range.end}" for range in self.ranges]) + ")"


__all__ = (
  'LocationArea',
  'LocationRange',
  'Position'
)
