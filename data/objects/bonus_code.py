from dataclasses import replace
from typing import Callable

from numpy import vectorize, cos
from pygame import Surface, Rect

from data.objects.bonus_data import Bonus
from data.objects.camera_data import Camera
from data.utils.constants import BONUS_SPRITE, TILE_EDGE


def display_bonus(bonus: Bonus, screen: Surface, camera: Camera) -> None:
    """
    Displays the bonus on the screen.

    :param bonus: bonus data
    :param screen: screen surface
    :param camera: camera data
    """
    if bonus.alive:
        screen.blit(BONUS_SPRITE, bonus.rect.topleft + camera.offset)


display_bonuses: Callable = vectorize(display_bonus)


def update_bonus(bonus: Bonus, counter: int) -> Bonus:
    rect: Rect = bonus.rect
    rect.y = bonus.origin[1] + cos(counter) * TILE_EDGE / 3
    return replace(bonus, rect=rect)


def destroy_bonus(bonus: Bonus) -> Bonus:
    """
    Destroys the bonus, making it invisible and immune to player collisions.

    :param bonus: bonus data
    :return: updated bonus data
    """
    return replace(bonus, alive=False)
