class Body(object):
    def __init__(self, color, mass, radius, position, velocity, acceleration):
        self.color = color
        self.mass = mass
        self.radius = radius
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    def update(self, t):
        self.velocity += self.acceleration * t
        self.position += self.velocity * t

    def distance(self, other):
        return self.position.distance(other.position)

    def rect(self):
        left = self.position.x - self.radius
        top = self.position.y - self.radius
        width = height = 2 * self.radius
        return (left, top, width, height)

    def __str__(self):
        return "mass: {}, radius: {}, p: {}, v: {}, a: {}".format(
            self.mass, self.radius,
            self.position, self.velocity, self.acceleration)

    def __repr__(self):
        return self.__str__()
