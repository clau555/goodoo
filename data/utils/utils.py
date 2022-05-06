from copy import deepcopy
from typing import List, Tuple

from numpy import ndarray, sqrt, sum, zeros, random, array
from pygame import Rect

from data.goalData import Goal
from data.playerData import Player
from data.tileData import Tile
from data.utils.constants import SCREEN_SIZE, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, TILE_SPRITE, PLAYER_SIZE, \
    TILE_SIZE, GOAL_SIZE, SCREEN_RECT, AUTOMATON_ITERATION, AUTOMATON_DENSITY, SCREEN_GRID_SIZE


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
    """
    Checks if a rectangle is visible in the screen.

    @param rect: rectangle to check
    @param camera_offset: camera offset
    @return: True if visible, False otherwise
    """
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


def get_moore_neighbors(tile_grid: ndarray, idx: ndarray) -> ndarray:
    """
    Returns neighborhood grid of the given tile position.

    :param tile_grid: world grid
    :param idx: world tile position
    :return: index neighborhood
    """
    clamped_idx: ndarray = idx.clip(1, GRID_SIZE - 2)
    return tile_grid[clamped_idx[0]-1:clamped_idx[0]+2, clamped_idx[1]-1:clamped_idx[1]+2]


def get_screen_grid(tile_grid: ndarray, camera_pos: ndarray) -> ndarray:
    """
    Returns the current tile grid visible on screen which is a sub grid of `tile_grid`.

    :param tile_grid: world grid
    :param camera_pos: top left corner of the camera in world space
    :return: tile grid visible on screen
    """
    idx: ndarray = (get_grid_index(camera_pos)).clip(0, GRID_SIZE - 1)  # top left corner of the camera in grid space
    return tile_grid[idx[0]:idx[0]+SCREEN_GRID_SIZE[0]+1, idx[1]:idx[1]+SCREEN_GRID_SIZE[1]+1]


# ----------------
# World generation
# ----------------


def generate_world() -> Tuple[ndarray, Player, Goal]:
    """
    Returns a world grid containing the wall tiles, and none for the empty tiles.
    Returns also a one-dimensional list of the wall tiles and the player and goal.

    :return: world grid, wall tiles, player, goal
    """

    # initial noise grid
    # TODO: use ndarray and vectorize `update_state` and `bool_grid_to_tile_grid`
    bool_grid: List = (random.choice(
        a=[False, True],
        size=GRID_SIZE,
        p=[1 - AUTOMATON_DENSITY, AUTOMATON_DENSITY])
    ).tolist()

    # cellular automaton execution
    for _ in range(AUTOMATON_ITERATION):
        bool_grid = update_state(bool_grid)

    # TODO: localize regions and build paths between them
    # TODO: add player and goal spawn points

    # conversion to tile grid
    tile_grid: List = bool_grid_to_tile_grid(bool_grid)

    # hard coded player and goal
    player_pos = array((10, 10)) * TILE_SIZE + TILE_SIZE / 2 - PLAYER_SIZE / 2
    player = Player(Rect(tuple(player_pos), tuple(PLAYER_SIZE)))
    goal_pos = array((40, 40)) * TILE_SIZE + TILE_SIZE / 2 - GOAL_SIZE / 2
    goal = Goal(Rect(goal_pos, tuple(TILE_SIZE)))

    return array(tile_grid), player, goal


def update_state(bool_grid: List) -> List:
    """
    Updates the state of each cell of the grid according to Moore's neighborhood.

    :param bool_grid: ndarray of boolean values
    :return: updated grid
    """
    new_grid: List = deepcopy(bool_grid)

    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):

            neighbor_wall_count: int = 0
            border: bool = False

            # checking every neighbor
            for x in range(i - 1, i + 2):
                for y in range(j - 1, j + 2):

                    if idx_inside_grid(array((x, y))):
                        if bool_grid[x][y] and (y != j or x != i):
                            neighbor_wall_count += 1
                    else:
                        # tiles on grid edge are automatically walls
                        border = True

            new_grid[i][j] = neighbor_wall_count > 4 or border

    return new_grid


def bool_grid_to_tile_grid(bool_grid: List) -> List:
    """
    Converts a grid of boolean values to a grid of tiles.

    :param bool_grid: ndarray of boolean values
    :return: grid of tiles and list of wall tiles
    """
    tile_grid: List = [[None for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):

            if bool_grid[i][j]:
                tile: Tile = Tile(Rect(array((i, j)) * TILE_SIZE, tuple(TILE_SIZE)), TILE_SPRITE)
                tile_grid[i][j] = tile

    return tile_grid
