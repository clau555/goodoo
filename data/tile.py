from dataclasses import dataclass

from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from data.constants import tuple_to_screen, GROUND_SPRITE, GRASS_SPRITE


@dataclass(frozen=True)
class Tile:
    rect: Rect
    sprite: Surface


def display_tile(tile: Tile, screen: Surface) -> None:
    """
    Displays the tile on the screen.

    :param tile: tile object
    :param screen: screen surface
    """
    screen.blit(tile.sprite, tuple_to_screen(tile.rect.topleft))
    if tile.sprite == GROUND_SPRITE:
        grass_pos = tile.rect.topleft - Vector2(2)
        screen.blit(GRASS_SPRITE, tuple_to_screen(grass_pos))
