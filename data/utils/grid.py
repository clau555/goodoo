from typing import Optional, Tuple, List

import pygame.image
from numpy import ndarray, zeros, ndenumerate
from pygame.pixelarray import PixelArray
from pygame.rect import Rect
from pygame.surface import Surface

from data.goalData import Goal
from data.playerData import Player
from data.tileData import Tile
from data.utils.constants import BLUE, TILE_SIZE, PLAYER_SIZE, RED, GOAL_SIZE, GREY, GRID_WIDTH, GRID_HEIGHT, \
    GRID_SIZE, TILE_SPRITE
from data.utils.utils import is_inside_grid


def color_comparison(color1: ndarray, color2: ndarray, margin: int = 10) -> bool:
    """
    Compares two colors and returns True if they are close enough.

    :param color1: rgb color
    :param color2: rgb color
    :param margin: maximum difference between colors
    :return: comparison result
    """
    return (color2 - margin <= color1).all() and (color1 <= color2 + margin).all()


def init_world(file_path: str) -> Tuple[List, List, Player, Goal]:
    """
    Loads a level from an image file.
    The image must be of `WORLD_WIDTH` by `WORLD_HEIGHT` size.
    It must contain white pixels representing the tiles,
    and a blue pixel representing the player spawn position.

    :param file_path: path to the image file
    :return: player data and the 2D array of tile data
    """
    im: Surface = pygame.image.load(file_path)
    pixel_array: PixelArray = pygame.PixelArray(im)

    if im.get_width() != GRID_WIDTH or im.get_height() != GRID_HEIGHT:
        raise ValueError("Level map has wrong size.")

    tile_grid: List = [[None for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
    non_empty_tiles: List = []
    player: Optional[Player] = None
    goal: Optional[Goal] = None

    for idx, _ in ndenumerate(zeros(shape=GRID_SIZE)):

        rgb: ndarray = im.unmap_rgb(pixel_array[idx])[0:3]

        if color_comparison(rgb, GREY):
            tile: Tile = Tile(get_tile_rect(idx), TILE_SPRITE)
            tile_grid[idx[0]][idx[1]] = tile
            non_empty_tiles.append(tile)

        elif color_comparison(rgb, BLUE) and not player:
            pos = idx * TILE_SIZE + TILE_SIZE / 2 - PLAYER_SIZE / 2
            player = Player(Rect(tuple(pos), tuple(PLAYER_SIZE)))

        elif color_comparison(rgb, RED) and not goal:
            pos = idx * TILE_SIZE + TILE_SIZE / 2 - GOAL_SIZE / 2
            goal = Goal(Rect(pos, TILE_SIZE))

    if not player:
        raise ValueError("No player spawn point detected inside the map.")
    if not goal:
        raise ValueError("No goal detected inside the map.")

    return tile_grid, non_empty_tiles, player, goal


def get_grid_index(pos: ndarray) -> ndarray:
    """
    Returns the grid index of the given position.
    Raise an exception if the position is outside the grid.

    :param pos: screen position
    :return: grid index
    """
    idx: ndarray = pos // TILE_SIZE
    if not is_inside_grid(idx):
        raise ValueError("Index out of bound.")
    return idx.astype(int)


def get_tile_rect(idx: ndarray) -> Rect:
    """
    Returns the rectangle of the tile at the given grid index.

    :param idx: world tile position
    :return: corresponding rectangle
    """
    return Rect(idx * TILE_SIZE, TILE_SIZE)


def get_neighbor_tiles(tile_grid: List, idx: ndarray) -> List:
    """
    Returns the list of all the neighbor tiles of the given tile position.
    Does not contain empty tiles.

    :param tile_grid: world grid
    :param idx: world tile position
    :return: neighbor tiles
    """
    tiles: List = []

    for i, _ in ndenumerate(zeros(shape=(3, 3))):

        offset_idx: ndarray = idx + i - 1
        if is_inside_grid(offset_idx) and tile_grid[offset_idx[0]][offset_idx[1]]:
            tiles.append(tile_grid[offset_idx[0]][offset_idx[1]])

    return tiles
