from typing import Tuple

from numpy import ndarray, array, argwhere
from numpy.random import randint
from pygame import Rect

from src.game.player.player import Player
from src.generation.cave import generate_cave_grid, rooms_connections_points, generate_connections, generate_exit, \
    generate_cave
from src.generation.decoration import generate_decoration
from src.utils.constants import GRID_HEIGHT, TILE_SIZE, PLAYER_SIZE


def generate_world() -> Tuple[ndarray, ndarray, Player]:
    """
    Returns tile maps of the world, one for the physical tiles, one for the decorations.
    Returns also the player.

    :return: cave map, decoration map, and player
    """
    cave_grid: ndarray = generate_cave_grid()
    cave_grid = generate_exit(cave_grid)
    cave_grid = generate_connections(cave_grid, rooms_connections_points(cave_grid))
    cave_map: ndarray = generate_cave(cave_grid)
    decoration_map: ndarray = generate_decoration(cave_grid)

    if cave_map.shape != decoration_map.shape:
        raise ValueError("Generated tile maps don't have same shapes.")

    return cave_map, decoration_map, _spawn_player(cave_grid)


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
    player_rect: Rect = Rect(tuple(player_pos), tuple(PLAYER_SIZE))
    return Player(player_pos, player_rect)
