from dataclasses import replace
from typing import Callable

from numpy import vectorize
from pygame import Surface

from data.objects.bonus_data import Bonus
from data.objects.camera_data import Camera
from data.utils.constants import BONUS_SPRITE


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


def destroy_bonus(bonus: Bonus) -> Bonus:
    """
    Destroys the bonus, making it invisible and immune to player collisions.

    :param bonus: bonus data
    :return: updated bonus data
    """
    return replace(bonus, alive=False)
