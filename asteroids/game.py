import pygame
from utils import load_sprite
from models import GameObject
from models import Spaceship, Asteroid


class Asteroids:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.spaceship = Spaceship((400, 300))
        self.asteroids = []
        ast1 = Asteroid(self.screen, -1)
        ast2 = Asteroid(self.screen, -50)
        self.asteroids.append(ast1)
        self.asteroids.append(ast2)

    def get_game_objects(self):
        return [self.spaceship, *self.asteroids]

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

        is_key_pressed = pygame.key.get_pressed()

        if is_key_pressed[pygame.K_RIGHT]:
            self.spaceship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.spaceship.rotate(clockwise=False)
        elif is_key_pressed[pygame.K_UP]:
            self.spaceship.accelerate()

    def _process_game_logic(self):
        for g_obj in self.get_game_objects():
            g_obj.move(self.screen)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for g_obj in self.get_game_objects():
            g_obj.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(30)
