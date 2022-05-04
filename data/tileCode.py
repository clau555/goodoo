from numpy import ndarray
from pygame.surface import Surface

from data.tileData import Tile
from data.utils.constants import TILE_SIZE
from data.utils.screen import world_to_screen


def display_tile(tile: Tile, screen: Surface) -> None:
    """
    Displays the tile on the screen.

    :param tile: tile data
    :param screen: screen surface
    """
    offset_pos: ndarray = tile.rect.topleft - (tile.sprite_size - TILE_SIZE) // 2
    # screen_pos: ndarray = do_camera_offset(world_to_screen(offset_pos), player)
    screen.blit(tile.sprite, world_to_screen(offset_pos))
