import pygame
from circleshape import CircleShape
from constants import *
from logger import log_state, log_event
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        num_points = 12
        self._offsets = [random.uniform(0.7, 1.0) for _ in range(num_points)]
        self._angles = [i * (360 / num_points) for i in range(num_points)]

    def draw(self, screen):
        points = [
            self.position + pygame.Vector2(0, -self.radius * r).rotate(a)
            for r, a in zip(self._offsets, self._angles)
        ]
        pygame.draw.polygon(screen, "purple", points, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        new_vel1 = self.velocity.rotate(angle)
        new_vel2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        ast1 = Asteroid(self.position.x, self.position.y, new_radius)
        ast1.velocity = new_vel1 * 1.2
        ast2 = Asteroid(self.position.x, self.position.y, new_radius)
        ast2.velocity = new_vel2 * 1.2