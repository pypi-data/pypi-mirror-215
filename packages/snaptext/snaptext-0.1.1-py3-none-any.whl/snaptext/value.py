from typing import Any, Generic, Optional, TypeVar

from .core import LocationArea


T = TypeVar('T')

class LocatedValue(Generic[T]):
  __match_args__ = ('value', 'area')

  def __init__(self, value: T, area: LocationArea):
    self.area = area
    self.value = value

  @property
  def source(self):
    return self.area.source

  def dislocate(self) -> Any:
    match self.value:
      case dict():
        return { key.dislocate(): value.dislocate() for key, value in self.value.items() }
      case list():
        return [item.dislocate() for item in self.value]
      case set():
        return {item.dislocate() for item in self.value}
      case _:
        return self.value


class LocatedValueContainer(LocatedValue[T], Generic[T]):
  def __repr__(self):
    return repr(self.value)


__all__ = (
  'LocatedValue',
  'LocatedValueContainer'
)
