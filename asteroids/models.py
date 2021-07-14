from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import load_sprite, wrap_position, decelerate, get_random_position, get_random_velocity
from random import randint, choice
import copy

UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity=(0, 0)):
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
    properties_by_rank = {
        1: {"scale": 1, "max_speed": 4},
        2: {"scale": 0.5, "max_speed": 8},
        3: {"scale": 0.25, "max_speed": 16},
    }

    def __init__(self, position, create_asteroid_cb, rank=1):
        self.create_asteroid_cb = create_asteroid_cb
        self.rank = rank
        sprite = rotozoom(load_sprite("asteroid"), 0, self.properties_by_rank[self.rank]["scale"])
        velocity = get_random_velocity(1, self.properties_by_rank[self.rank]["max_speed"])
        self.direction = Vector2(UP)
        self.rotation_angle = choice([num for num in range(-20, 20) if num])
        super().__init__(position, sprite, velocity)

    def draw(self, surface):
        self.direction.rotate_ip(self.rotation_angle)
        super().draw_with_rotation(surface)

    def explode(self):
        def explode_inner(quantity, rank):
            for _ in range(quantity):
                ast = Asteroid(self.position, self.create_asteroid_cb, rank)
                self.create_asteroid_cb(ast)

        if self.rank == 1:
            explode_inner(6, self.rank + 1)
        elif self.rank == 2:
            explode_inner(12, self.rank + 1)


class Ship(GameObject):
    MANOEUVRABILITY = 7
    ACCELERATION = 0.75
    BULLET_SPEED = 10
    sprites = {
        "normal": "spaceship",
        "shielded": "spaceship_shielded",
    }

    def __init__(self, position, create_bullet_cb):
        self.create_bullet_cb = create_bullet_cb
        self.direction = Vector2(UP)
        self.powerups = {
            "shield": False,
            "fast_shoot": False,
            "triple_shoot": False,
            "piercing_shoot": False,
            "boomerang_shoot": False,
        }

        sprite = load_sprite(self.sprites["normal"])

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
        decelerate(self.velocity, 0.97)
        super().move(surface)

    def shoot(self):
        if self.powerups["triple_shoot"]:
            self.shoot_triple()
        else:
            self.shoot_simple()

    def shoot_simple(self):

        bullet_speed = self.BULLET_SPEED * 2.5 if self.powerups["fast_shoot"] else self.BULLET_SPEED

        bullet_velocity = self.direction * bullet_speed + self.velocity
        bullet = Bullet(self.position, bullet_velocity, copy.copy(self.powerups), self.direction)
        self.create_bullet_cb(bullet)

    def shoot_triple(self):

        bullet_speed = self.BULLET_SPEED * 2.5 if self.powerups["fast_shoot"] else self.BULLET_SPEED

        def chiralise_direction(direction, is_left):
            if abs(direction[0] / direction[1]) > 1:
                return Vector2([direction[0], direction[1] + 0.5]) if is_left \
                    else Vector2([direction[0], direction[1] - 0.5])
            else:
                return Vector2([direction[0] + 0.5, direction[1]]) if is_left \
                    else Vector2([direction[0] - 0.5, direction[1]])

        bullet_velocity_L = chiralise_direction(self.direction, True) * (bullet_speed * 1.15) + self.velocity
        bullet_L = Bullet(self.position, bullet_velocity_L, copy.copy(self.powerups), self.direction)

        bullet_velocity_R = chiralise_direction(self.direction, False) * (bullet_speed * 1.15) + self.velocity
        bullet_R = Bullet(self.position, bullet_velocity_R, copy.copy(self.powerups), self.direction)

        self.create_bullet_cb(bullet_L)
        self.create_bullet_cb(bullet_R)
        self.shoot_simple()


class Bullet(GameObject):
    def __init__(self, position, velocity, powerups, direction=0):
        self.powerups = powerups
        if self.powerups["boomerang_shoot"]:
            self.direction = Vector2(*direction)

        sprite_name = "boomerang" if self.powerups["boomerang_shoot"] else "bullet"

        super().__init__(position, load_sprite(sprite_name), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity

    def draw(self, surface):
        if self.powerups["boomerang_shoot"]:
            super().draw_with_rotation(surface)
        else:
            super().draw(surface)


class Powerup(GameObject):
    powerups_ref = {
        1: {"label": "health", "name": "shield"},
        2: {"label": "health", "name": "extra_life"},
        3: {"label": "shoot", "name": "fast_shoot"},
        4: {"label": "shoot", "name": "triple_shoot"},
        5: {"label": "shoot", "name": "piercing_shoot"},
        6: {"label": "shoot", "name": "boomerang_shoot"},
    }

    def __init__(self, position, type=None):
        self.type = type if type else randint(3, 6)
        self.properties = self.powerups_ref[self.type]
        sprite = rotozoom(load_sprite(f"powerup_{self.type}"), 0, 2)
        super().__init__(position, sprite)
