from dataclasses import replace
from typing import List

from numpy import cos, ndarray, array, around
from pygame import Rect, Surface, SRCALPHA, draw, BLEND_RGB_ADD

from data.objects.bonus_data import Bonus
from data.objects.camera_data import Camera
from data.utils.constants import TILE_EDGE, LIGHT_COLOR, LIGHT_RADIUS, BONUS_ANIMATION_SPEED


def update_bonus(bonus: Bonus, timer: float) -> Bonus:
    """
    Makes the bonus cycle in a movement from top to bottom.

    :param bonus: bonus data
    :param timer: game timer
    :return: updated bonus data
    """
    rect: Rect = bonus.rect
    rect.y = bonus.origin[1] + cos(timer / BONUS_ANIMATION_SPEED) * TILE_EDGE / 3
    return replace(bonus, rect=rect)


def destroy_bonus(bonus: Bonus) -> Bonus:
    """
    Destroys the bonus, making it invisible and immune to player collisions.

    :param bonus: bonus data
    :return: updated bonus data
    """
    return replace(bonus, alive=False)


def _circle_surface(radius: float) -> Surface:
    """
    Returns a surface containing a transparent blue circle of the given radius.

    :param radius: radius
    :return: surface
    """
    surface: Surface = Surface((radius * 2, radius * 2), SRCALPHA)
    draw.circle(surface, LIGHT_COLOR, (radius, radius), radius)
    surface.set_alpha(255)
    return surface


def display_light(screen: Surface, pos: ndarray, camera: Camera, timer: float) -> None:
    """
    Displays a light animation at a certain position.

    :param screen: screen surface
    :param pos: world position
    :param camera: camera data
    :param timer: game timer
    """
    radius_: List[float] = [
        LIGHT_RADIUS * ((timer % BONUS_ANIMATION_SPEED) / BONUS_ANIMATION_SPEED),
        LIGHT_RADIUS * ((BONUS_ANIMATION_SPEED - timer % BONUS_ANIMATION_SPEED) / BONUS_ANIMATION_SPEED)
    ]
    lights: List[Surface] = [_circle_surface(radius) for radius in radius_]

    for i in range(2):
        screen.blit(
            lights[i],
            around(pos - array((radius_[i], radius_[i]), dtype=int) + camera.offset),
            special_flags=BLEND_RGB_ADD
        )
