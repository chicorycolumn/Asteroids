from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import load_sprite, wrap_position, slow_down_velocity, get_random_position, get_random_velocity
from random import randint, choice

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
    size_to_scale = {
        3: 1,
        2: 0.5,
        1: 0.25
    }

    def __init__(self, position, create_asteroid_cb, size=3):
        self.create_asteroid_cb = create_asteroid_cb
        self.size = size
        sprite = rotozoom(load_sprite("asteroid"), 0, self.size_to_scale[self.size])
        velocity = get_random_velocity(1, 10)
        self.direction = Vector2(UP)
        self.rotation_angle = choice([num for num in range(-20, 20) if num])
        super().__init__(position, sprite, velocity)

    def move(self, surface):
        super().move(surface)

    def draw(self, surface):
        self.direction.rotate_ip(self.rotation_angle)
        super().draw_with_rotation(surface)

    def explode(self):
        def explode_inner(quantity, size):
            for _ in range(quantity):
                ast = Asteroid(self.position, self.create_asteroid_cb, size)
                self.create_asteroid_cb(ast)

        if self.size == 3:
            explode_inner(2, self.size - 1)
        elif self.size == 2:
            explode_inner(4, self.size - 1)


class Spaceship(GameObject):
    MANOEUVRABILITY = 7
    ACCELERATION = 0.25
    BULLET_SPEED = 10

    def __init__(self, position, create_bullet_cb):
        self.create_bullet_cb = create_bullet_cb
        self.direction = Vector2(UP)

        sprite = load_sprite("spaceship")

        super().__init__(position, sprite, Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANOEUVRABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        super().draw_with_rotation(surface)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION

    def move(self, surface):
        slow_down_velocity(self.velocity)
        super().move(surface)

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_cb(bullet)


class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity
