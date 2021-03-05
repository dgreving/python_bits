import math


class Circle:
    def __init__(self, radius=1):
        self.radius = radius

    def __repr__(self):
        return f'Circle({self.radius})'

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def diameter(self):
        return self.radius * 2

    @diameter.setter
    def diameter(self, value):
        self.radius = value / 2

    @property
    def area(self):
        return math.pi * self.radius**2

    @area.setter
    def area(self, value):
        raise AttributeError("can't set attribute")


if __name__ == '__main__':
    c = Circle(2)
    print(c)
    print(c.diameter)
    c.diameter = 5
    print(c.diameter)
    print(c.radius)
    print(c.area)

