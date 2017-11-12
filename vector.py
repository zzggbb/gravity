import math

class Vector(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.EPSILON = 0.001

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def distance(self, other, diff=None):
        if not diff:
            diff = other - self
        return diff.magnitude()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def near(self, other):
        return abs(self.x - other.x) < self.EPSILON and \
               abs(self.y - other.y) < self.EPSILON

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return Vector(self.x * n, self.y * n)

    def __truediv__(self, n):
        return Vector(self.x/n, self.y/n)

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
        return "({0:.4f}, {1:.4f})".format(self.x, self.y)
