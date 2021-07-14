import pygame
from utils import load_sprite
from models import GameObject
import time
from models import Ship, Asteroid, Powerup
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
        self.powerups = []
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
        game_objects = [*self.asteroids, *self.bullets, *self.powerups]

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

    def _process_game_logic(self):
        for g_obj in self.get_game_objects():
            g_obj.move(self.screen)

        if self.ship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.ship):
                    if self.ship.powerups["shield"]:
                        self.ship.powerups["shield"] = False
                        self.ship.sprite = load_sprite(self.ship.sprites["normal"])
                        break
                    else:
                        self.ship = None
                        break

            for powerup in self.powerups:
                if powerup.collides_with(self.ship):
                    powerup_name = powerup.properties["name"]

                    if powerup_name == "shield":
                        self.ship.sprite = load_sprite(self.ship.sprites["shielded"])

                    self.ship.powerups[powerup_name] = True
                    self.powerups.remove(powerup)
                    break

            def generate_powerup():
                if not len(self.powerups) and int(str(time.time())[-3:]) < 100:
                    while True:
                        position = get_random_position(self.screen)
                        if (
                                position.distance_to(self.ship.position)
                                > self.MIN_ASTEROID_DISTANCE
                        ):
                            break

                    self.powerups.append(Powerup(position))

            generate_powerup()

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if bullet.collides_with(asteroid):
                    asteroid.explode()
                    self.asteroids.remove(asteroid)
                    if not self.ship.powerups["piercing_shoot"]:
                        self.bullets.remove(bullet)
                    break

            for powerup in self.powerups[:]:
                if bullet.collides_with(powerup):
                    self.powerups.remove(powerup)
                    break


        for powerup in self.powerups[:]:
            for asteroid in self.asteroids[:]:
                if powerup.collides_with(asteroid):
                    self.powerups.remove(powerup)
                    break


    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for g_obj in self.get_game_objects():
            g_obj.draw(self.screen)
        pygame.display.flip()

        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        X = 200
        Y = 200
        # display_surface = pygame.display.set_mode((X, Y))
        font = pygame.font.Font('freesansbold.ttf', 64)
        text = font.render('GeeksForGeeks', True, white, white)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2)
        self.screen.blit(text, textRect)

        self.clock.tick(30)
