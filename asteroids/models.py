from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import load_sprite, wrap_position, slow_down_velocity
from random import randint, choice
import time

UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def draw_with_rotation(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Asteroid(GameObject):
    direction = Vector2(UP)

    def __init__(self, surface):
        w, h = surface.get_size()
        x = choice(range(w))
        y = choice(range(h))
        position = (x, y)
        sprite = load_sprite("asteroid")
        super().__init__(position, sprite, Vector2(0))

    def move(self, surface):
        super().move(surface)


class Spaceship(GameObject):
    direction = Vector2(UP)
    MANOEUVRABILITY = 7
    ACCELERATION = 0.25

    def __init__(self, position, sprite=None):
        if not sprite:
            sprite = load_sprite("spaceship")

        super().__init__(position, sprite, Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANOEUVRABILITY * sign
        print("angle", angle)
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        super().draw_with_rotation(surface)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION

    def move(self, surface):
        slow_down_velocity(self.velocity)
        super().move(surface)
