import math

class Vector(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.EPSILON = 0.001

    def distance(self, other):
        diff = other - self
        return math.sqrt(diff.x**2 + diff.y**2)

    def __eq__(self, other):
        return abs(self.x - other.x) >= self.EPSILON and \
               abs(self.y - other.y) >= self.EPSILON

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return Vector(self.x * n, self.y * n)

    def __radd__(self, value):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __rmul__(self, n):
        return self.__mul__(n)

    def __iter__(self):
        yield int(self.x)
        yield int(self.y)

    def __str__(self):
        return "({0:.4f}, {0:.4f})".format(self.x, self.y)
