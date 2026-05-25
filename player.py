import pygame
import random
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0
        self.is_thrusting = False

    def draw(self, screen):
        f = pygame.Vector2(0, 1).rotate(self.rotation)
        r = pygame.Vector2(0, 1).rotate(self.rotation + 90)
        p = self.position
        R = self.radius

        if self.is_thrusting:
            back = p - f * R
            tip = back - f * R * random.uniform(0.8, 1.4)
            pygame.draw.polygon(screen, "orange", [
                back - r * 0.25, tip, back + r * 0.25,
            ])
            inner_tip = back - f * R * random.uniform(0.4, 0.8)
            pygame.draw.polygon(screen, "yellow", [
                back - r * 0.12, inner_tip, back + r * 0.12,
            ])

        for side in (-1, 1):
            wing = [
                p + f * 0.2 * R + r * side * 0.35 * R,
                p - f * 0.7 * R + r * side * R,
                p - f * 0.8 * R + r * side * 0.2 * R,
            ]
            pygame.draw.polygon(screen, "white", wing, LINE_WIDTH)

        body = [
            p + f * R,
            p + f * 0.2 * R + r * 0.35 * R,
            p - f * 0.8 * R + r * 0.2 * R,
            p - f * R + r * 0.15 * R,
            p - f * R - r * 0.15 * R,
            p - f * 0.8 * R - r * 0.2 * R,
            p + f * 0.2 * R - r * 0.35 * R,
        ]
        pygame.draw.polygon(screen, "white", body, LINE_WIDTH)

        pygame.draw.circle(screen, "cyan", p + f * 0.55 * R, max(2, int(R * 0.18)))

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.cooldown -= dt
        self.is_thrusting = bool(keys[pygame.K_w] or keys[pygame.K_s])

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_SPACE]:
            if self.cooldown > 0:
                pass
            else:
                self.shoot()
                self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
