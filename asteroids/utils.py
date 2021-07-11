from pygame.image import load
from pygame.math import Vector2


def load_sprite(name, with_alpha=True):
    path = f"asteroids/assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def slow_down_velocity(vel):
    def slowed(point):
        return 0 if 0.01 > point > -0.01 else point * 0.99

    vel[0] = slowed(vel[0])
    vel[1] = slowed(vel[1])
