from dataclasses import dataclass

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from data.constants import TILE_COLOR, GROUND_COLOR, GROUND_SIZE


@dataclass(frozen=True)
class Tile:
    rect: Rect
    top: bool


def display_tile(tile: Tile, screen: Surface) -> None:
    """
    Displays the tile on the screen.
    Displays also the ground if the tile is a ground tile.

    :param tile: tile object
    :param screen: screen surface
    """
    pygame.draw.rect(screen, TILE_COLOR, tile.rect)
    if tile.top:
        ground: Rect = Rect(tile.rect.topleft, GROUND_SIZE)
        pygame.draw.rect(screen, GROUND_COLOR, ground)
