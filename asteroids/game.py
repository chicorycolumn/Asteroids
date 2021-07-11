import pygame
from utils import load_sprite
from models import GameObject
from models import Ship, Asteroid
from utils import load_sprite, wrap_position, decelerate, get_random_position


class Asteroids:

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((1250, 850))
        self.background = load_sprite("galaxy", False, True)
        self.clock = pygame.time.Clock()
        self.MIN_ASTEROID_DISTANCE = 150
        self.asteroids = []
        self.bullets = []
        self.ship = Ship((400, 300), self.bullets.append)

        for _ in range(4):
            while True:
                position = get_random_position(self.screen)
                if (
                        position.distance_to(self.ship.position)
                        > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.ship:
            game_objects.append(self.ship)

        return game_objects

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Asteroids")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            elif self.ship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.ship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.ship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.ship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.ship.rotate(clockwise=False)
            elif is_key_pressed[pygame.K_UP]:
                self.ship.accelerate()
            # elif is_key_pressed[pygame.K_SPACE]:
            #     self.ship.shoot()

    def _process_game_logic(self):
        for g_obj in self.get_game_objects():
            g_obj.move(self.screen)

        if self.ship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.ship):
                    self.ship = None
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if bullet.collides_with(asteroid):
                    asteroid.explode()
                    self.asteroids.remove(asteroid)
                    if not self.ship.powerups["hard_bullets"]:
                        self.bullets.remove(bullet)
                    break

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for g_obj in self.get_game_objects():
            g_obj.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(30)
