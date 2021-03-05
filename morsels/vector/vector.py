import numbers
from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    __slots__ = ('x', 'y', 'z')
    x: float
    y: float
    z: float

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __eq__(self, other):
        return all(a == b for a, b in zip(self, other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError
        return Vector(*[a + b for a, b in zip(self, other)])

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError
        return Vector(*[a - b for a, b in zip(self, other)])

    def __mul__(self, other):
        if not isinstance(other, numbers.Number):
            raise TypeError
        return Vector(*(other*_ for _ in self))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self.__mul__(1./other)

