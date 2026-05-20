import pygame
from circleshape import CircleShape
from constants import *
from logger import log_state, log_event
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "purple", self.position, self.radius, LINE_WIDTH)

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