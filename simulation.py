import pygame as pg

from vector import Vector
from body import Body

class Simulation(object):
    def __init__(self):
        pg.init()
        pg.font.init()
        self.GRAVITATION = 1
        self.FRAMERATE = 100
        self.WINDOW = (1920,1080)
        self.color = {
            'background': (0x00,0x00,0x00),
            'object': (0x00, 0xbc, 0xd4),
            'acceleration': (0xff, 0xeb, 0x3b),
            'velocity': (0x4c, 0xaf, 0x50)
        }
        self.display = {
            'acceleration': True,
            'velocity': True,
        }
        self.font = pg.font.SysFont("monospace", 20)
        self.surface = pg.display.set_mode(self.WINDOW)
        self.clock = pg.time.Clock()
        self.running = True
        self.paused = False
        self.bodies = []

        self.surface.set_colorkey(self.color['background'])

    def updateAcceleration(self, body):
        sum = Vector(0,0)
        for other in self.bodies:
            if other == body:
                continue

            diff = other.position - body.position
            dist_3 = body.distance(other) ** 3.0
            sum += (other.mass / dist_3) * diff

        body.acceleration = self.GRAVITATION * sum

    def removeBody(self, pos):
        for body in self.bodies:
            if body.position.distance(pos) < body.radius:
                self.bodies.remove(body)

    def processEvents(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.paused = not self.paused

                if event.key == pg.K_a:
                    self.display['acceleration'] = not self.display['acceleration']

                if event.key == pg.K_n:
                    pos = pg.mouse.get_pos()
                    self.bodies.append(Body(
                        self.color['object'], 10**6, 10, Vector(*pos),
                        Vector(0,0), Vector(0,0)
                    ))

                if event.key == pg.K_q:
                    self.running = False

                if event.key == pg.K_v:
                    self.display['velocity'] = not self.display['velocity']

                if event.key == pg.K_x:
                    pos = pg.mouse.get_pos()
                    self.removeBody(Vector(*pos))

    def update(self):
        dt = self.clock.tick_busy_loop(self.FRAMERATE) / 1000.0
        self.processEvents()

        self.surface.fill(self.color['background'])
        for body in self.bodies:
            if not self.paused:
                body.update(dt)

            if self.display['acceleration']:
                pg.draw.line(self.surface,
                             self.color['acceleration'],
                             tuple(body.position),
                             tuple(body.position + body.acceleration))

            if self.display['velocity']:
                pg.draw.line(self.surface,
                             self.color['velocity'],
                             tuple(body.position),
                             tuple(body.position + body.velocity))

            self.updateAcceleration(body)
            pg.draw.circle(self.surface, body.color,
                           tuple(body.position), body.radius)

        pg.display.flip()

    def loop(self):
        while self.running:
            self.update()
        pg.quit()
