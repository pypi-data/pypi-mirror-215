import re
from typing import Any

from .string import LocatedString, Source
from .value import LocatedValue, LocatedValueContainer


constants = {
  'false': False,
  'true': True,
  'null': None
}

class Parser:
  def __init__(self, contents: str):
    self.index = 0
    self.source = Source(contents)

  def read_char(self):
    if self.index >= len(self.source):
      raise Exception("Unexpected EOF")

    return self.source[self.index]

  def read_text(self):
    return self.source[self.index:]

  def consume_array(self):
    start_offset = self.index

    self.index += 1
    self.consume_whitespace()

    output = list[Any]()

    while True:
      if self.read_char() == "]":
        self.index += 1
        break

      if output:
        if self.read_char() != ",":
          raise Exception("Missing comma")

        self.index += 1
        self.consume_whitespace()

      output.append(self.consume_value())

    return LocatedValueContainer(output, self.source.area % (start_offset, self.index))

  def consume_object(self):
    start_offset = self.index

    self.index += 1
    self.consume_whitespace()

    output = dict[LocatedString, Any]()

    while True:
      if self.read_char() == "}":
        self.index += 1
        break

      if output:
        if self.read_char() != ",":
          raise Exception("Missing comma")

        self.index += 1
        self.consume_whitespace()

      key = self.consume_string()

      self.consume_whitespace()

      if self.read_char() != ":":
        raise Exception("Missing colon")

      self.index += 1

      value = self.consume_value()
      output[key] = value

    return LocatedValueContainer(output, self.source.area % (start_offset, self.index))

  def consumer_number(self):
    text = self.read_text()
    match = re.match(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?", text)

    if match:
      value = float(match.group())
    else:
      match = re.match(r"-?(?:0|[1-9]\d*)", text)

      if not match:
        raise Exception("Unexpected token")

      value = int(match.group())

    start_offset = self.index
    self.index += len(match.group())

    return LocatedValueContainer(value, self.source.area % (start_offset, self.index))

  def consume_string(self):
    self.index += 1
    start_offset = self.index

    while True:
      ch = self.read_char()

      if ch == '"':
        break

      self.index += 1

    value = self.source[start_offset:self.index]
    self.index += 1

    return value

  def consume_value(self):
    self.consume_whitespace()

    char = self.read_char()
    text = self.read_text()

    for name, const_value in constants.items():
      if text.startswith(name):
        self.index += len(name)
        value = LocatedValueContainer(const_value, self.source.area % (self.index - len(name), self.index))
        break
    else:
      if char == '"':
        value = self.consume_string()
      elif char == "[":
        value = self.consume_array()
      elif char == "{":
        value = self.consume_object()
      elif re.match(r"[-0-9]", char):
        value = self.consumer_number()
      else:
        raise Exception("Unexpected token")

    self.consume_whitespace()
    return value

  def consume_whitespace(self):
    while True:
      ch = self.source[self.index]

      if ch not in (" ", "\t", "\n", "\r"):
        break

      self.index += 1


def loads(contents: str, /) -> LocatedValue:
  parser = Parser(contents)
  return parser.consume_value()


__all__ = [
  'loads'
]
