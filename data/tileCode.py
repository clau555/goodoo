from typing import Callable

from numpy import  vectorize, array
from pygame import Surface

from data.tileData import Tile


def display_tile(tile: Tile, screen: Surface, camera_offset_x: int, camera_offset_y: int) -> None:
    """
    Displays a tile on the screen.

    :param tile: tile data
    :param screen: screen surface
    :param camera_offset_x: x-axis camera offset
    :param camera_offset_y: y-axis camera offset
    """
    if tile:
        screen.blit(tile.sprite, tile.rect.topleft + array((camera_offset_x, camera_offset_y)))


# vectorized display function to apply to an array of tiles
display_tiles: Callable = vectorize(display_tile)
