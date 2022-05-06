from typing import Callable

from numpy import vectorize, ndarray
from pygame import Surface

from data.tileData import Tile


def display_tile(tile: Tile, screen: Surface, camera_offset: ndarray) -> None:
    """
    Displays a tile on the screen.

    :param tile: tile data
    :param screen: screen surface
    :param camera_offset: camera offset
    """
    if tile:
        screen.blit(tile.sprite, tile.rect.topleft + camera_offset)


# vectorized display function to apply to an array of tiles
display_tiles: Callable = vectorize(display_tile, excluded=['camera_offset'])
