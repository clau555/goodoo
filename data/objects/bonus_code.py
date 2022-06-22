from dataclasses import replace
from typing import List

from numpy import cos, array, around
from pygame import Rect, Surface, BLEND_RGB_ADD

from data.objects.bonus_data import Bonus
from data.objects.camera_data import Camera
from data.utils.constants import TILE_EDGE, LIGHT_RADIUS, BONUS_ANIMATION_SPEED, BONUS_SPRITE, LIGHT_RECT
from data.utils.functions import bonus_light_surface, rect_inside_screen


def update_bonus(bonus: Bonus, timer: float) -> Bonus:
    """
    Makes the bonus cycle in a movement from top to bottom,
    and updates its light effect.

    :param bonus: bonus data
    :param timer: game timer
    :return: updated bonus data
    """
    rect: Rect = bonus.rect
    rect.y = bonus.origin[1] + cos(timer / BONUS_ANIMATION_SPEED) * TILE_EDGE / 3

    radius: List[float] = [
        LIGHT_RADIUS * ((timer % BONUS_ANIMATION_SPEED) / BONUS_ANIMATION_SPEED),
        LIGHT_RADIUS * ((BONUS_ANIMATION_SPEED - timer % BONUS_ANIMATION_SPEED) / BONUS_ANIMATION_SPEED)
    ]
    lights: List[Surface] = [bonus_light_surface(r) for r in radius]

    return replace(bonus, rect=rect, lights=lights)


def destroy_bonus(bonus: Bonus) -> Bonus:
    """
    Destroys the bonus, making it invisible and immune to player collisions.

    :param bonus: bonus data
    :return: updated bonus data
    """
    return replace(bonus, alive=False)


def bonus_inside_screen(bonus: Bonus, camera: Camera) -> bool:
    """
    Checks if a bonus is visible on screen.

    :param bonus: bonus data
    :param camera: camera data
    :return: True if bonus is visible, False otherwise
    """
    light_rect: Rect = Rect(LIGHT_RECT)
    light_rect.center = bonus.rect.center
    if rect_inside_screen(light_rect, camera):
        return True
    return False


def display_bonus(bonus: Bonus, screen: Surface, camera: Camera) -> None:
    """
    Displays a bonus along with its light effect.

    :param bonus:
    :param screen: screen surface
    :param camera: camera data
    """
    screen.blit(BONUS_SPRITE, around(bonus.rect.topleft + camera.offset))

    for light in bonus.lights:
        screen.blit(
            light,
            around(
                array(bonus.rect.center, dtype=float) - array(light.get_rect().size, dtype=float) // 2 + camera.offset),
            special_flags=BLEND_RGB_ADD
        )
