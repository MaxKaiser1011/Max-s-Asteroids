import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        if self.velocity.length() == 0:
            return
        direction = self.velocity.normalize()
        start = self.position - direction * 10
        end = self.position + direction * 10
        pygame.draw.line(screen, (220, 60, 60), start, end, 4)
        pygame.draw.line(screen, "white", start, end, 2)

    def update(self, dt):
        self.position += self.velocity * dt