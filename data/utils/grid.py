from typing import List, Tuple, Optional

import pygame.image
from pygame.math import Vector2
from pygame.pixelarray import PixelArray
from pygame.rect import Rect
from pygame.surface import Surface

from data.goal import Goal
from data.player import Player
from data.tile import Tile
from data.utils import BLUE, TILE_SIZE, PLAYER_SIZE, WHITE, RED, \
    TILE_SPRITE, GROUND_SPRITE, GROUND_SPRITE_SIZE, TILE_SPRITE_SIZE, GOAL_SIZE, \
    GREY, PILLAR_TOP_SPRITE_SIZE, PILLAR_TOP_SPRITE, PILLAR_SPRITE_SIZE, \
    PILLAR_SPRITE

Grid = List[List[Optional[Tile]]]

GRID_SIZE: Tuple[int, int] = 32, 18  # world size in tiles
GRID_WIDTH: int = GRID_SIZE[0]
GRID_HEIGHT: int = GRID_SIZE[1]


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


def init_world(file_path: str) -> Tuple[Player, Goal, Grid]:
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

    if im.get_width() != GRID_WIDTH or im.get_height() != GRID_HEIGHT:
        raise ValueError("Level map has wrong size.")

    tile_grid: Grid = [
        [None for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)
    ]
    player: Optional[Player] = None
    goal: Optional[Goal] = None

    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):

            idx: Vector2 = Vector2(i, j)
            rgb: Tuple[int, int, int] = im.unmap_rgb(pixel_array[i, j])[0:3]
            pos: Vector2 = idx.elementwise() * TILE_SIZE

            if color_comparison(rgb, GREY):
                # rock tiles
                if j > 0 and not tile_grid[i][j - 1]:
                    tile_grid[i][j] = Tile(
                        Rect(pos, TILE_SIZE),
                        GROUND_SPRITE,
                        GROUND_SPRITE_SIZE
                    )
                else:
                    tile_grid[i][j] = Tile(
                        Rect(pos, TILE_SIZE),
                        TILE_SPRITE,
                        TILE_SPRITE_SIZE
                    )

            if color_comparison(rgb, WHITE):
                # pillar tiles
                if j > 0 and not tile_grid[i][j - 1]:
                    tile_grid[i][j] = Tile(
                        Rect(pos, TILE_SIZE),
                        PILLAR_TOP_SPRITE,
                        PILLAR_TOP_SPRITE_SIZE

                    )
                else:
                    tile_grid[i][j] = Tile(
                        Rect(pos, TILE_SIZE),
                        PILLAR_SPRITE,
                        PILLAR_SPRITE_SIZE
                    )

            elif color_comparison(rgb, BLUE) and not player:
                # spawn position at the center of the tile
                pos = idx.elementwise() * TILE_SIZE \
                               + TILE_SIZE // 2 \
                               - PLAYER_SIZE // 2
                player = Player(Rect(pos, PLAYER_SIZE))

            elif color_comparison(rgb, RED) and not goal:
                # goal at the center of the tile
                pos = idx.elementwise() * TILE_SIZE \
                               + TILE_SIZE // 2 \
                               - GOAL_SIZE // 2
                goal = Goal(Rect(pos, TILE_SIZE))

    if not player:
        raise ValueError("No player spawn point detected inside the map.")
    if not goal:
        raise ValueError("No goal detected inside the map.")

    return player, goal, tile_grid


def get_grid_tiles(tile_grid: Grid) -> List[Tile]:
    """
    Returns the list of all the non-null tiles in the grid.

    :param tile_grid: world grid
    :return: tile objects of the world
    """
    tiles: List[Tile] = []

    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):

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

            if 0 <= i < GRID_WIDTH and 0 <= j < GRID_HEIGHT \
                    and tile_grid[i][j]:
                tiles.append(tile_grid[i][j])

    return tiles


def get_grid_index(rect: Rect) -> Tuple[int, int]:
    """
    Returns the grid index of the given rectangle.

    :param rect: pygame rectangle
    :return: corresponding grid index
    """
    return int(rect.centerx // TILE_SIZE.x), int(rect.centery // TILE_SIZE.y)
