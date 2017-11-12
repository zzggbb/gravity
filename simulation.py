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
            'body': (0x00, 0xbc, 0xd4),
            'acceleration': (0xff, 0xeb, 0x3b),
            'velocity': (0x4c, 0xaf, 0x50),
            'collision': (0xe0,66,66),
            'white': (0xff, 0xff, 0xff)
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
        self.bodies = {}

        self.surface.set_colorkey(self.color['background'])

    def collide(self, bodyA, bodyB):
        m_prime = bodyA.mass + bodyB.mass
        v_prime = (bodyA.momentum() + bodyB.momentum()) / m_prime
        self.kill(bodyB.position)
        bodyA.velocity = v_prime
        bodyA.mass = m_prime

    def updateAcceleration(self, body):
        sum = Vector(0,0)
        for position, other in self.bodies.copy().items():
            if position.near(body.position):
                continue

            diff = position - body.position
            distance = diff.magnitude()

            if distance < body.radius + other.radius:
                self.collide(body, other)

            dist_3 = distance ** 3.0
            sum += (other.mass / dist_3) * diff

        body.acceleration = self.GRAVITATION * sum

    def spawn(self, body):
        self.bodies[body.position] = body

    def kill(self, position):
        if position in self.bodies:
            del self.bodies[position]

    def processEvents(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.paused = not self.paused

                if event.key == pg.K_a:
                    self.display['acceleration'] = not self.display['acceleration']

                if event.key == pg.K_n:
                    pos = pg.mouse.get_pos()
                    body = Body(self.color['body'], 10**6, 10, Vector(*pos),
                                Vector(0,0), Vector(0,0))
                    self.spawn(body)

                if event.key == pg.K_s:
                    mouse_pos = Vector(*pg.mouse.get_pos())
                    body = Body(self.color['white'], 10**9, 10, mouse_pos,
                                Vector(0,0), Vector(0,0))
                    self.spawn(body)

                if event.key == pg.K_q:
                    self.running = False

                if event.key == pg.K_v:
                    self.display['velocity'] = not self.display['velocity']

                if event.key == pg.K_x:
                    mouse_pos = Vector(*pg.mouse.get_pos())
                    for position, body in self.bodies.copy().items():
                        if mouse_pos.distance(position) < body.radius:
                            self.kill(position)

    def update(self):
        dt = self.clock.tick_busy_loop(self.FRAMERATE) / 1000.0
        self.processEvents()

        self.surface.fill(self.color['background'])
        for position, body in self.bodies.copy().items():
            if not self.paused:
                self.kill(position)
                body.update(dt)
                self.spawn(body)

            if self.display['acceleration']:
                pg.draw.line(self.surface,
                             self.color['acceleration'],
                             tuple(position),
                             tuple(position + body.acceleration))

            if self.display['velocity']:
                pg.draw.line(self.surface,
                             self.color['velocity'],
                             tuple(position),
                             tuple(position + body.velocity))

            self.updateAcceleration(body)
            pg.draw.circle(self.surface, body.color,
                           tuple(position), body.radius)

        pg.display.flip()

    def loop(self):
        while self.running:
            self.update()
        pg.quit()
