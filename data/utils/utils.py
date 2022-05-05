from typing import Tuple, List, Optional

import pygame
from numpy import ndarray, sqrt, sum, ndenumerate, zeros
from pygame import Surface, Rect

from data.goalData import Goal
from data.playerData import Player
from data.tileData import Tile
from data.utils.constants import SCREEN_SIZE, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, GREY, TILE_SPRITE, PLAYER_SIZE, \
    TILE_SIZE, BLUE, RED, GOAL_SIZE, SCREEN_RECT


def scale(v: ndarray, length: float) -> ndarray:
    """
    Scales a vector to a given length.

    :param v: 2D numpy array
    :param length: length to scale to
    :return: scaled vector
    """
    return v / sqrt(sum(v**2)) * length


def pos_inside_screen(pos: ndarray, camera_offset: ndarray = zeros(2)) -> bool:
    """
    Checks if a position is inside the screen.

    :param pos: screen position to check
    :param camera_offset: camera offset
    :return: True if inside screen, False otherwise
    """
    return (0 <= pos + camera_offset).all() and (pos + camera_offset < SCREEN_SIZE).all()


def rect_inside_screen(rect: Rect, camera_offset) -> bool:
    offset_rect: Rect = Rect(rect)
    offset_rect.topleft = offset_rect.topleft + camera_offset
    return SCREEN_RECT.colliderect(offset_rect)


def idx_inside_grid(idx: ndarray) -> bool:
    """
    Checks if an index is inside the grid.

    :param idx: 2D numpy array
    :return: True if inside grid, False otherwise
    """
    return (0 <= idx).all() and (idx < GRID_SIZE).all()


def pos_inside_grid(pos: ndarray) -> bool:
    """
    Checks if a world position is inside the grid.

    :param pos: world position to check
    :return: True if inside grid, False otherwise
    """
    idx: ndarray = get_grid_index(pos)
    return idx_inside_grid(idx)


def get_grid_index(pos: ndarray) -> ndarray:
    """
    Returns the grid index of the given position.
    The values will be negative or greater than the grid size if the position is outside the grid.

    :param pos: screen position
    :return: grid index
    """
    return (pos // TILE_SIZE).astype(int)


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
        if idx_inside_grid(offset_idx) and tile_grid[offset_idx[0]][offset_idx[1]]:
            tiles.append(tile_grid[offset_idx[0]][offset_idx[1]])

    return tiles


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
    It must contain white pixels representing the tiles, and a blue pixel representing the player spawn position.

    :param file_path: path to the image file
    :return: player data and the 2D array of tile data
    """
    im: Surface = pygame.image.load(file_path)

    if im.get_width() != GRID_WIDTH or im.get_height() != GRID_HEIGHT:
        raise ValueError("Level map has wrong size.")

    tile_grid: List = [[None for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
    non_empty_tiles: List = []
    player: Optional[Player] = None
    goal: Optional[Goal] = None

    for idx, _ in ndenumerate(zeros(shape=GRID_SIZE)):

        rgb: ndarray = im.get_at(idx)[0:3]

        if color_comparison(rgb, GREY):
            tile: Tile = Tile(Rect(idx * TILE_SIZE, tuple(TILE_SIZE)), TILE_SPRITE)
            tile_grid[idx[0]][idx[1]] = tile
            non_empty_tiles.append(tile)

        elif color_comparison(rgb, BLUE) and not player:
            pos = idx * TILE_SIZE + TILE_SIZE / 2 - PLAYER_SIZE / 2
            player = Player(Rect(tuple(pos), tuple(PLAYER_SIZE)))

        elif color_comparison(rgb, RED) and not goal:
            pos = idx * TILE_SIZE + TILE_SIZE / 2 - GOAL_SIZE / 2
            goal = Goal(Rect(pos, tuple(TILE_SIZE)))

    if not player:
        raise ValueError("No player spawn point detected inside the map.")
    if not goal:
        raise ValueError("No goal detected inside the map.")

    return tile_grid, non_empty_tiles, player, goal
