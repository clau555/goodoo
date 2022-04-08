from typing import List, Tuple, Optional

import pygame.image
from pygame.pixelarray import PixelArray
from pygame.rect import Rect
from pygame.surface import Surface

from data.constants import WORLD_WIDTH, WORLD_HEIGHT, BLUE, TILE_EDGE, \
    TILE_SIZE, PLAYER_EDGE, PLAYER_SIZE, PLAYER_SPRITE, WHITE
from data.player import Player
from data.tile import Tile

Grid = List[List[Optional[Tile]]]


def color_comparison(
        color1: Tuple[int, int, int],
        color2: Tuple[int, int, int],
        margin: int = 10
) -> bool:
    """
    Compares two colors and returns True if they are close enough.

    :param color1: rgb color
    :param color2: rgb color
    :param margin: maximum difference between colors
    :return: comparison result
    """
    return color2[0] - margin <= color1[0] <= color2[0] + margin and \
           color2[1] - margin <= color1[1] <= color2[1] + margin and \
           color2[2] - margin <= color1[2] <= color2[2] + margin


def init_world(file_path: str) -> Tuple[Player, Grid]:
    """
    Loads a level from an image file.
    The image must be of `WORLD_WIDTH` by `WORLD_HEIGHT` size.
    It must contain white pixels representing the tiles,
    and a blue pixel representing the player spawn position.

    :param file_path: path to the image file
    :return: the player object and the 2D array of tile objects
    """
    im: Surface = pygame.image.load(file_path)
    pixel_array: PixelArray = pygame.PixelArray(im)

    if im.get_width() != WORLD_WIDTH or im.get_height() != WORLD_HEIGHT:
        raise ValueError("Level map has wrong size.")

    tile_grid: Grid = [
        [None for _ in range(WORLD_HEIGHT)] for _ in range(WORLD_WIDTH)
    ]
    player: Optional[Player] = None

    for i in range(WORLD_WIDTH):
        for j in range(WORLD_HEIGHT):

            rgb: Tuple[int, int, int] = im.unmap_rgb(pixel_array[i, j])[0:3]

            if color_comparison(rgb, BLUE) and not player:
                # spawn position at the center of the tile
                pos: Tuple[int, int] = (
                    i * TILE_EDGE + TILE_EDGE // 2 - PLAYER_EDGE // 2,
                    j * TILE_EDGE + TILE_EDGE // 2 - PLAYER_EDGE // 2
                )
                # player sprite is scaled up to world dimensions
                sprite: Surface = pygame.transform.scale(
                    pygame.image.load(PLAYER_SPRITE), PLAYER_SIZE
                )
                player = Player(Rect(pos, PLAYER_SIZE), sprite)

            elif color_comparison(rgb, WHITE):
                pos: Tuple[int, int] = (i * TILE_EDGE, j * TILE_EDGE)
                top: bool = j > 0 and not tile_grid[i][j - 1]
                tile_grid[i][j] = Tile(Rect(pos, TILE_SIZE), top)

    if not player:
        raise ValueError("No player spawn point detected inside the map.")

    return player, tile_grid


def get_grid_tiles(tile_grid: Grid) -> List[Tile]:
    """
    Returns the list of all the non-null tiles in the grid.

    :param tile_grid: world grid
    :return: tile objects of the world
    """
    tiles: List[Tile] = []

    for i in range(WORLD_WIDTH):
        for j in range(WORLD_HEIGHT):

            if tile_grid[i][j]:
                tiles.append(tile_grid[i][j])

    return tiles


def get_neighbor_tiles(tile_grid: Grid, idx: Tuple[int, int]) -> List[Tile]:
    """
    Returns the list of all the neighbor tiles of the given tile position.

    :param tile_grid: world grid
    :param idx: world tile position
    :return: neighbor tiles
    """
    tiles: List[Tile] = []

    for i in range(idx[0] - 1, idx[0] + 2):
        for j in range(idx[1] - 1, idx[1] + 2):

            if 0 <= i < WORLD_WIDTH and 0 <= j < WORLD_HEIGHT \
                    and tile_grid[i][j]:
                tiles.append(tile_grid[i][j])

    return tiles


def get_grid_index(rect: Rect) -> Tuple[int, int]:
    """
    Returns the grid index of the given rectangle.

    :param rect: pygame rectangle
    :return: corresponding grid index
    """
    return rect.centerx // TILE_EDGE, rect.centery // TILE_EDGE
