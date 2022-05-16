from dataclasses import replace

from numpy import cos
from pygame import Rect

from data.objects.bonus_data import Bonus
from data.utils.constants import TILE_EDGE


def update_bonus(bonus: Bonus, counter: float) -> Bonus:
    """
    Makes the bonus cycle in a movement from top to bottom.

    :param bonus: bonus data
    :param counter: game counter
    :return: updated bonus data
    """
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
