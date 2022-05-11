from typing import Callable

from numpy import vectorize
from pygame import Surface

from data.objects.camera_data import Camera
from data.objects.tile_data import Tile


def display_tile(tile: Tile, screen: Surface, camera: Camera) -> None:
    """
    Displays a tile on the screen.

    :param tile: tile data
    :param screen: screen surface
    :param camera: camera data
    """
    if tile:
        screen.blit(tile.sprite, tile.rect.topleft + camera.offset)


# vectorized display function to apply to an array of tiles
display_tiles: Callable = vectorize(display_tile)
