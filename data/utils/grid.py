from typing import List, Optional, Tuple

import pygame.image
from numpy import ndarray, array
from pygame.pixelarray import PixelArray
from pygame.rect import Rect
from pygame.surface import Surface

from data.goalData import Goal
from data.playerData import Player
from data.tileData import Tile
from data.utils.constants import BLUE, TILE_SIZE, PLAYER_SIZE, WHITE, RED, TILE_SPRITE, GROUND_SPRITE, \
    GROUND_SPRITE_SIZE, TILE_SPRITE_SIZE, GOAL_SIZE, GREY, PILLAR_TOP_SPRITE_SIZE, PILLAR_TOP_SPRITE, \
    PILLAR_SPRITE_SIZE, PILLAR_SPRITE, color

Grid = List[List[Optional[Tile]]]

GRID_SIZE: ndarray = array((32, 18))  # world size in tiles
GRID_WIDTH: int = GRID_SIZE[0]
GRID_HEIGHT: int = GRID_SIZE[1]


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


def init_world(file_path: str) -> Tuple[Player, Goal, Grid]:
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

    tile_grid: Grid = [
        [None for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)
    ]
    player: Optional[Player] = None
    goal: Optional[Goal] = None

    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):

            idx: ndarray = array((i, j))
            rgb: color = im.unmap_rgb(pixel_array[i, j])[0:3]
            pos: ndarray = idx * TILE_SIZE

            if color_comparison(rgb, GREY):
                # rock tiles
                if j > 0 and not tile_grid[i][j - 1]:
                    tile_grid[i][j] = Tile(Rect(pos, TILE_SIZE), GROUND_SPRITE, GROUND_SPRITE_SIZE)
                else:
                    tile_grid[i][j] = Tile(Rect(pos, TILE_SIZE), TILE_SPRITE, TILE_SPRITE_SIZE)

            if color_comparison(rgb, WHITE):
                # pillar tiles
                if j > 0 and not tile_grid[i][j - 1]:
                    tile_grid[i][j] = Tile(Rect(pos, TILE_SIZE), PILLAR_TOP_SPRITE, PILLAR_TOP_SPRITE_SIZE)
                else:
                    tile_grid[i][j] = Tile(Rect(pos, TILE_SIZE), PILLAR_SPRITE, PILLAR_SPRITE_SIZE)

            elif color_comparison(rgb, BLUE) and not player:
                # spawn position at the center of the tile
                pos = idx * TILE_SIZE + TILE_SIZE // 2 - PLAYER_SIZE // 2
                player = Player(Rect(tuple(pos), tuple(PLAYER_SIZE)))

            elif color_comparison(rgb, RED) and not goal:
                # goal at the center of the tile
                pos = idx * TILE_SIZE + TILE_SIZE // 2 - GOAL_SIZE // 2
                goal = Goal(Rect(pos, TILE_SIZE))

    if not player:
        raise ValueError("No player spawn point detected inside the map.")
    if not goal:
        raise ValueError("No goal detected inside the map.")

    return player, goal, tile_grid


def get_grid_tiles(tile_grid: Grid) -> "ndarray[Tile]":
    """
    Returns the list of all the non-null tiles in the grid.
    All tiles representing pillars are placed at the end of the list
    for them to be rendered last.

    :param tile_grid: world grid
    :return: world's tile data list
    """
    tiles: List[Tile] = []
    pillars: List[Tile] = []

    for j in range(GRID_HEIGHT):
        for i in range(GRID_WIDTH):

            tile: Tile = tile_grid[i][j]

            if tile:
                if tile.sprite == PILLAR_SPRITE or tile.sprite == PILLAR_TOP_SPRITE:
                    pillars.append(tile)
                else:
                    tiles.append(tile)

    tiles.extend(pillars)
    return array(tiles)


def get_neighbor_tiles(tile_grid: Grid, idx: ndarray) -> "ndarray[Tile]":
    """
    Returns the list of all the neighbor tiles of the given tile position.

    :param tile_grid: world grid
    :param idx: world tile position
    :return: neighbor tiles
    """
    tiles: List[Tile] = []

    for i in range(idx[0] - 1, idx[0] + 2):
        for j in range(idx[1] - 1, idx[1] + 2):

            if 0 <= i < GRID_WIDTH and 0 <= j < GRID_HEIGHT and tile_grid[i][j]:
                tiles.append(tile_grid[i][j])

    return array(tiles)


def get_grid_index(rect: Rect) -> ndarray:
    """
    Returns the grid index of the given rectangle.

    :param rect: pygame rectangle
    :return: corresponding grid index
    """
    return rect.center // TILE_SIZE
