from numpy import ndarray, array, around
from pygame import Surface, draw, Rect

from src.game.lava import Lava
from src.game.player.player import Player
from src.utils.constants import JAUGE_RECT, GRID_HEIGHT, JAUGE_POS, JAUGE_SIZE, JAUGE_PLAYER_SIZE, \
    BLACK, JAUGE_OUTLINE_SURFACE, JAUGE_OUTLINE_POS, TILE_EDGE, LAVA_COLOR, PLAYER_COLOR


def display_jauge(player: Player, lava: Lava, screen: Surface) -> None:
    """
    Displays progression jauge on the right of the screen.
    It shows player level and lava level.

    :param player: player object
    :param lava: lava object
    :param screen: screen surface
    """
    screen.blit(JAUGE_OUTLINE_SURFACE, JAUGE_OUTLINE_POS)
    draw.rect(screen, BLACK, JAUGE_RECT)
    draw.rect(screen, LAVA_COLOR, _lava_rect(lava))
    draw.rect(screen, PLAYER_COLOR, _player_rect(player))


def _player_rect(player: Player) -> Rect:
    """
    Returns the rect representing player that will be displayed on the jauge.

    :param player: player object
    :return: player jauge rect
    """
    player_progression: float = 1 - ((float(player.world_position[1]) / TILE_EDGE) / GRID_HEIGHT)
    player_pos: ndarray = JAUGE_POS - around(array((0, -JAUGE_SIZE[1] + JAUGE_SIZE[1] * player_progression)))

    player_rect: Rect = Rect(tuple(player_pos), tuple(JAUGE_PLAYER_SIZE))
    # clamping player at bottom of the jauge
    player_rect.bottom = min(player_rect.bottom, int(JAUGE_POS[1] + JAUGE_SIZE[1]))

    return player_rect


def _lava_rect(lava: Lava) -> Rect:
    """
    Returns the rect representing lava that will be displayed on the jauge.

    :param lava: lava object
    :return: lava jauge rect
    """
    lava_progression: float = 1 - ((lava.y / TILE_EDGE) / GRID_HEIGHT)
    lava_pos: ndarray = JAUGE_POS - around(array((0, -JAUGE_SIZE[1] + JAUGE_SIZE[1] * lava_progression)))

    lava_rect_height: float = JAUGE_POS[1] + JAUGE_SIZE[1] - lava_pos[1]
    lava_rect: Rect = Rect(tuple(lava_pos), (JAUGE_SIZE[0], lava_rect_height))
    lava_rect.top = max(lava_rect.top, int(JAUGE_POS[1]))  # clamping lava rect at top of the jauge

    return lava_rect
