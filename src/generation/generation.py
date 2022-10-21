from typing import Tuple

from numpy import ndarray, array, argwhere
from numpy.random import randint
from pygame import Rect

from src.generation.cave import generate_cave_grid, rooms_connections_points, generate_connections, generate_exit, \
    generate_cave
from src.generation.decoration import generate_decoration
from src.model.constants import TILE_SIZE, GRID_HEIGHT, \
    PLAYER_SIZE
from src.model.dataclasses import Player, TileMaps


def generate_world() -> Tuple[TileMaps, Player]:
    """
    Returns a world grid containing the wall tiles, and none for the empty tiles.
    Returns also the player.

    :return: tile grid and player data
    """
    cave_grid: ndarray = generate_cave_grid()
    cave_grid = generate_exit(cave_grid)
    cave_grid = generate_connections(cave_grid, rooms_connections_points(cave_grid))

    tile_maps: TileMaps = TileMaps(generate_cave(cave_grid), generate_decoration(cave_grid))

    if tile_maps.cave.shape != tile_maps.decoration.shape:
        raise ValueError("Generated tile maps don't have same shapes.")

    return tile_maps, _spawn_player(cave_grid)


def _spawn_player(cave: ndarray) -> Player:
    """
    Spawns the player in the cave by searching for the most bottom free tile.

    :param cave: boolean grid
    :return: player
    """

    # getting the first row with empty tiles starting from bottom of the grid
    spawn_height: int = GRID_HEIGHT - 1
    empty_xs: ndarray = argwhere(cave[:, spawn_height])
    for j in range(GRID_HEIGHT - 1, 0, -1):
        empty_xs = argwhere(cave[:, j] == False)  # have to do this boolean comparison because of numpy
        if empty_xs.size > 0:
            spawn_height = j
            break

    if empty_xs.size == 0:
        raise ValueError("No player spawn point found")
    if empty_xs.size == 1:
        x: int = int(empty_xs[0])  # choosing the only empty tile
    else:
        x: int = int(empty_xs[randint(0, empty_xs.size - 1)])  # choosing a random empty tile

    player_idx: ndarray = array((x, spawn_height))  # grid space
    player_pos: ndarray = player_idx * TILE_SIZE + TILE_SIZE / 2 - PLAYER_SIZE / 2  # world space
    return Player(player_pos, Rect(tuple(player_pos), tuple(PLAYER_SIZE)))
