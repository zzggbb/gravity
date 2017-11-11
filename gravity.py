import sys
import pygame as pg

class Vector(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, n):
        return Vector(self.x * n, self.y * n)

    def __radd__(self, value):
        return self.__add__(value)

    def __rmul__(self, n):
        return self.__mul__(n)

    def __iter__(self):
        yield int(self.x)
        yield int(self.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

class Mass(object):
    def __init__(self, color, mass, radius, p, v, a):
        self.color = color
        self.mass = mass
        self.radius = radius
        self.p = p
        self.v = v
        self.a = a

    def rect(self):
        return pg.Rect(self.p.x - self.radius, self.p.y - self.radius,
                       2 * self.radius, 2 * self.radius)

    def draw(self, surface):
        pg.draw.circle(surface, self.color, tuple(self.p), self.radius)

    def update(self, t):
        self.v += self.a * t
        self.p += self.v * t

    def __str__(self):
        return "mass: {}, radius: {}, p: {}, v: {}, a: {}".format(
            self.mass, self.radius, self.p, self.v, self.a)

class Simulation(object):
    def __init__(self):
        pg.init()
        pg.font.init()

        self.background_color = (0, 0, 0)
        self.mass_color = (0x00, 0xae, 0xdb)
        self.font = pg.font.SysFont("monospace", 20)
        self.surface = pg.display.set_mode((400,400))

        self.clock = pg.time.Clock()
        self.framerate = None
        self.running = True
        self.paused = False

        self.masses = [
            Mass(self.mass_color, 10, 10, Vector(100,100), Vector(20, 20), Vector(0,0)),
            Mass(self.mass_color, 10, 10, Vector(300,100), Vector(-20,20), Vector(0,0))
        ]

        # only draw the background once, since we're blitting!
        self.surface.fill(self.background_color)
        self.surface.set_colorkey(self.background_color)

    def processEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.paused = not self.paused

    def update(self):
        dt = self.clock.tick_busy_loop() / 1000.0
        self.processEvents()
        if self.paused:
            return

        dirty = []
        for mass in self.masses:
            # get current_rect of mass
            current_rect = mass.rect()
            # draw background over current_rect (erase it)
            self.surface.blit(pg.Surface(current_rect.size), current_rect)
            # append current_rect to dirty
            dirty.append(current_rect)
            # move the mass
            mass.update(dt)
            # draw the mass
            mass.draw(self.surface)
            # get new_rect of mass
            new_rect = mass.rect()
            # append new_rect to dirty
            dirty.append(new_rect)

        pg.display.update(dirty)

    def loop(self):
        while self.running:
            self.update()
        pg.quit()

sim = Simulation()
sim.loop()
