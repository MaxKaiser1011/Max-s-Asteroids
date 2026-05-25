import math
import random
import sys

from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from constants import *
from explosion import Explosion
from logger import log_event, log_state
from player import Player
import pygame
from shot import Shot

player = None

def _draw_stars(screen, stars, t):
    for sx, sy, sr, sb, sp in stars:
        b = int(sb * (0.75 + 0.25 * math.sin(t * 2 + sp)))
        pygame.draw.circle(screen, (b, b, b), (sx, sy), max(1, sr))

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField()

    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)

    Explosion.containers = (updatable, drawable)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    score = 0
    score_timer = 0.0
    star_time = 0.0
    stars = [
        (
            random.randint(0, SCREEN_WIDTH),
            random.randint(0, SCREEN_HEIGHT),
            random.choices([1, 2, 3], weights=[6, 3, 1])[0],
            random.randint(120, 255),
            random.uniform(0, math.pi * 2),
        )
        for _ in range(150)
    ]
    dt = 0
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        log_state()
        star_time += dt
        score_timer += dt
        if score_timer >= 1:
            score += 1
            score_timer -= 1
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player) == True:
                log_event("player_hit")
                Explosion(player.position.x, player.position.y, player.radius * 2)
                end_timer = 0.5
                while end_timer > 0:
                    ms = clock.tick(60)
                    end_dt = ms / 1000
                    end_timer -= end_dt
                    updatable.update(end_dt)
                    star_time += end_dt
                    screen.fill("black")
                    _draw_stars(screen, stars, star_time)
                    for i in drawable:
                        i.draw(screen)
                    screen.blit(font.render(f"Score: {score}", True, "white"), (10, 10))
                    pygame.display.flip()
                print("Game over!")
                sys.exit()
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot) == True:
                    log_event("asteroid_shot")
                    Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                    score += 1
                    shot.kill()
                    asteroid.split()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        _draw_stars(screen, stars, star_time)
        for i in drawable:
            i.draw(screen)
        screen.blit(font.render(f"Score: {score}", True, "white"), (10, 10))
        pygame.display.flip()
        ms = clock.tick(60)
        dt = ms/1000




if __name__ == "__main__":
    main()
