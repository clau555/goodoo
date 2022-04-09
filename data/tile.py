from dataclasses import dataclass

from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from data.utils import TILE_SIZE
from data.utils.screen import tuple_to_screen


@dataclass(frozen=True)
class Tile:
    rect: Rect
    sprite: Surface
    sprite_size: Vector2


def display_tile(tile: Tile, screen: Surface) -> None:
    """
    Displays the tile on the screen.

    :param tile: tile object
    :param screen: screen surface
    """
    offset_pos = tile.rect.topleft - (tile.sprite_size - TILE_SIZE) // 2
    screen.blit(tile.sprite, tuple_to_screen(offset_pos))
