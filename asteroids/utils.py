from pygame.image import load
from pygame.math import Vector2
import random


def load_sprite(name, with_alpha=True):
    path = f"asteroids/assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height())
    )


def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def is_offscreen(game_object, surface):
    x, y = game_object.position
    w, h = surface.get_size()
    print(f"x{x}, y{y}, width{w}, height{h}")
    return (x < 0 or x > w) or (y < 0 or y > h)


def slow_down_velocity(vel):
    def slowed(point):
        return 0 if 0.01 > point > -0.01 else point * 0.99

    vel[0] = slowed(vel[0])
    vel[1] = slowed(vel[1])
