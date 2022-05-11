from typing import Tuple, Optional, Callable, List

from numpy import ndarray, sqrt, sum, zeros, random, array, argwhere, vectorize, mgrid, invert, full, amin, sign
from pygame import Rect
from scipy.ndimage.measurements import label
from scipy.spatial.distance import cdist

from data.objects.camera_data import Camera
from data.objects.goal_data import Goal
from data.objects.player_data import Player
from data.objects.tile_data import Tile
from data.utils.constants import SCREEN_SIZE, GRID_SIZE, TILE_SPRITE, PLAYER_SIZE, \
    TILE_SIZE, GOAL_SIZE, SCREEN_RECT, AUTOMATON_ITERATION, NOISE_DENSITY, SCREEN_GRID_SIZE, GRID_HEIGHT, GRID_WIDTH


# ----
# Math
# ----

def scale(v: ndarray, length: float) -> ndarray:
    """
    Scales a vector to a given length.

    https://stackoverflow.com/a/21031303/17987233

    :param v: grid index
    :param length: length to scale to
    :return: scaled vector
    """
    return v / sqrt(sum(v ** 2)) * length


# ------
# Screen
# ------

def pos_inside_screen(pos: ndarray, camera: Camera) -> bool:
    """
    Checks if a position is inside the screen.

    :param pos: position in world space
    :param camera: camera data
    :return: True if inside screen, False otherwise
    """
    return (pos + camera.offset >= 0).all() and (pos + camera.offset < SCREEN_SIZE).all()


def rect_inside_screen(rect: Rect, camera: Camera) -> bool:
    """
    Checks if a rectangle is visible in the screen.

    :param rect: rectangle in world space
    :param camera: camera data
    :return: True if visible, False otherwise
    """
    offset_rect: Rect = Rect(rect)
    offset_rect.topleft = offset_rect.topleft + camera.offset
    return SCREEN_RECT.colliderect(offset_rect)


# ----
# Grid
# ----

def idx_inside_grid(idx: ndarray) -> bool:
    """
    Checks if an index is inside the grid.

    :param idx: grid index
    :return: True if inside grid, False otherwise
    """
    return (0 <= idx).all() and (idx < GRID_SIZE).all()


def pos_inside_grid(pos: ndarray) -> bool:
    """
    Checks if a world position is inside the grid.

    :param pos: position in world space
    :return: True if inside grid, False otherwise
    """
    idx: ndarray = get_grid_index(pos)
    return idx_inside_grid(idx)


def get_grid_index(pos: ndarray) -> ndarray:
    """
    Returns the grid index of the given world position.

    Warning : the values will be negative or greater than the grid size if the position is outside the grid.

    :param pos: position in world space
    :return: grid index
    """
    return (pos // TILE_SIZE).astype(int)


def get_screen_grid(tile_grid: ndarray, camera: Camera) -> ndarray:
    """
    Returns a sub grid of `tile_grid` which is the current tile grid visible on screen.

    :param tile_grid: world grid
    :param camera: camera data
    :return: tile grid visible on screen
    """
    idx: ndarray = (get_grid_index(camera.top_left)).clip(0, GRID_SIZE - 1)  # conversion in grid space
    return tile_grid[
           idx[0]: idx[0] + SCREEN_GRID_SIZE[0] + 1,
           idx[1]: idx[1] + SCREEN_GRID_SIZE[1] + 1
           ]


def get_neighbor_grid(tile_grid: ndarray, idx: ndarray) -> ndarray:
    """
    Returns neighborhood grid of the given tile position.

    :param tile_grid: world grid
    :param idx: world tile position
    :return: index neighborhood
    """
    clamped_idx: ndarray = idx.clip(1, GRID_SIZE - 2)
    return tile_grid[
           clamped_idx[0] - 1: clamped_idx[0] + 2,
           clamped_idx[1] - 1: clamped_idx[1] + 2
           ]


# ----------------
# World generation
# ----------------

def get_neighbors_count_grid(bool_grid: ndarray) -> ndarray:
    """
    Returns a grid with the number of neighbors for each cell.
    A neighbor is counted if it's true.

    :param bool_grid: grid of booleans
    :return: grid with the number of neighbors for each cell
    """
    neighbors_mat: ndarray = zeros(bool_grid.shape, dtype=int)
    int_grid: ndarray = bool_grid.astype(int)
    neighbors_mat[1:-1, 1:-1] = (int_grid[:-2, :-2] + int_grid[:-2, 1:-1] + int_grid[:-2, 2:]
                                 + int_grid[1:-1, :-2] + int_grid[1:-1, 2:] + int_grid[2:, :-2]
                                 + int_grid[2:, 1:-1] + int_grid[2:, 2:])
    return neighbors_mat


def cell_to_tile(cell: bool, x_idxes: ndarray, y_idxes: ndarray) -> Optional[Tile]:
    """
    Returns the tile corresponding to the given cell.

    :param cell: boolean cell
    :param x_idxes: x indices of the cell
    :param y_idxes: y indices of the cell
    :return: tile if cell is true, None otherwise
    """
    if cell:
        return Tile(Rect(array((x_idxes, y_idxes)) * TILE_SIZE, tuple(TILE_SIZE)), TILE_SPRITE)
    return None


cells_to_tiles: Callable = vectorize(cell_to_tile)


def generate_world() -> Tuple[ndarray, Player, Goal]:
    """
    Returns a world grid containing the wall tiles, and none for the empty tiles.
    Returns also the spawned player and goal.

    Algorithm uses cellular automaton cave generation described here : https://youtu.be/slTEz6555Ts

    Implementation is based on vectorized cellular automaton implementation described here :
    https://lhoupert.fr/test-jbook/04-code-vectorization.html#uniform-vectorization

    :return: world grid, player, goal
    """
    # initial noise grid
    bool_grid: ndarray = random.choice(
        a=[True, False],
        size=GRID_SIZE,
        p=[NOISE_DENSITY, 1 - NOISE_DENSITY]
    )

    # cellular automaton execution
    for _ in range(AUTOMATON_ITERATION):

        # getting each cell neighbors count
        n_count_grid: ndarray = get_neighbors_count_grid(bool_grid)

        # flatten grids
        bool_grid_flat: ndarray = bool_grid.ravel()
        n_count_grid_flat: ndarray = n_count_grid.ravel()

        # cellular automaton rules
        wall_tiles = argwhere(n_count_grid_flat > 4)
        empty_tiles = argwhere(n_count_grid_flat <= 3)

        # rules application
        bool_grid_flat[wall_tiles] = True
        bool_grid_flat[empty_tiles] = False

        # border tiles are walls
        bool_grid[0, :] = bool_grid[-1, :] = bool_grid[:, 0] = bool_grid[:, -1] = True

    # TODO: localize regions and build paths between them
    # TODO: add player and goal spawn points

    # conversion to tile grid
    x_idxes, y_idxes = mgrid[:GRID_WIDTH, :GRID_HEIGHT]
    tile_grid: ndarray = cells_to_tiles(bool_grid, x_idxes, y_idxes)

    # hard coded player and goal
    player_pos = array((GRID_WIDTH / 2, 40)) * TILE_SIZE + TILE_SIZE / 2 - PLAYER_SIZE / 2
    player = Player(Rect(tuple(player_pos), tuple(PLAYER_SIZE)))
    goal_pos = array((GRID_WIDTH, GRID_HEIGHT)) * TILE_SIZE + TILE_SIZE / 2 - GOAL_SIZE / 2
    goal = Goal(Rect(goal_pos, tuple(TILE_SIZE)))

    return tile_grid, player, goal
