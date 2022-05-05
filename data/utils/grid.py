from typing import Optional, Tuple

import pygame.image
from numpy import ndarray, array, zeros
from pygame.pixelarray import PixelArray
from pygame.rect import Rect
from pygame.surface import Surface

from data.goalData import Goal
from data.playerData import Player
from data.utils.constants import BLUE, TILE_SIZE, PLAYER_SIZE, RED, GOAL_SIZE, GREY, color, \
    GRID_WIDTH, GRID_HEIGHT, GRID_SIZE


def color_comparison(color1: color, color2: color, margin: int = 10) -> bool:
    """
    Compares two colors and returns True if they are close enough.

    :param color1: rgb color
    :param color2: rgb color
    :param margin: maximum difference between colors
    :return: comparison result
    """
    return \
        color2[0] - margin <= color1[0] <= color2[0] + margin and \
        color2[1] - margin <= color1[1] <= color2[1] + margin and \
        color2[2] - margin <= color1[2] <= color2[2] + margin


def init_world(file_path: str) -> Tuple[ndarray, Player, Goal]:
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

    tile_grid: ndarray = zeros(shape=GRID_SIZE, dtype=bool)
    player: Optional[Player] = None
    goal: Optional[Goal] = None

    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):

            idx: ndarray = array((i, j))
            rgb: color = im.unmap_rgb(pixel_array[i, j])[0:3]

            if color_comparison(rgb, GREY):
                tile_grid[i, j] = True

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

    return tile_grid, player, goal


def get_grid_index(pos: ndarray) -> ndarray:
    """
    Returns the grid index of the given position.

    :param pos: screen position
    :return: grid index
    """
    return pos // TILE_SIZE


def get_position(idx: ndarray) -> ndarray:
    """
    Returns the world position of the given grid index.

    :param idx: grid index
    :return: world position
    """
    return idx * TILE_SIZE


def get_tile_rect(idx: ndarray) -> Rect:
    """
    Returns the rectangle of the tile at the given grid index.

    :param idx: world tile position
    :return: corresponding rectangle
    """
    return Rect(idx * TILE_SIZE, TILE_SIZE)


def get_neighbor_idxes(idx: ndarray) -> ndarray:
    """
    Returns the grid indices of the neighbors of the given grid index.

    :param idx: grid index
    :return: neighbor grid indices
    """
    return array([[idx + array((i, j)) for j in range(-1, 2)] for i in range(-1, 2)])


def is_empty(tile_grid: ndarray, idx: ndarray) -> bool:
    """
    Returns whether the given tile is empty.

    :param tile_grid: world grid
    :param idx: grid index
    :return: true if empty, false otherwise
    """
    return not tile_grid[int(idx[0]), int(idx[1])]
