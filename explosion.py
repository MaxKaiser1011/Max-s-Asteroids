import pygame
import random

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.max_radius = radius * 1.5
        self.elapsed = 0
        self.lifetime = 0.45
        num_particles = max(6, int(radius / 4))
        self.particles = []
        for _ in range(num_particles):
            angle = random.uniform(0, 360)
            speed = random.uniform(40, radius * 4)
            vel = pygame.Vector2(0, 1).rotate(angle) * speed
            life = random.uniform(0.2, 0.45)
            self.particles.append([pygame.Vector2(x, y), vel, life, life])

    def update(self, dt):
        self.elapsed += dt
        for p in self.particles:
            p[0] += p[1] * dt
            p[2] -= dt
        self.particles = [p for p in self.particles if p[2] > 0]
        if self.elapsed >= self.lifetime:
            self.kill()

    def draw(self, screen):
        t = min(1.0, self.elapsed / self.lifetime)
        ring_r = int(self.max_radius * t)
        if ring_r > 0:
            pygame.draw.circle(screen, "orange", self.position, ring_r, 2)
        for p in self.particles:
            fade = p[2] / p[3]
            color = "yellow" if fade > 0.5 else "orange"
            pygame.draw.circle(screen, color, p[0], max(1, int(3 * fade)))
