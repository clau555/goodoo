from typing import List

from numpy import ndarray, sqrt, sum
from pygame import Rect, Surface

from data.objects.camera_data import Camera
from data.utils.constants import SCREEN_SIZE, GRID_SIZE, TILE_SIZE, SCREEN_RECT, SCREEN_GRID_SIZE


def scale(v: ndarray, length: float) -> ndarray:
    """
    Scales a vector to a given length.

    https://stackoverflow.com/a/21031303/17987233

    :param v: grid index
    :param length: length to scale to
    :return: scaled vector
    """
    return v / sqrt(sum(v ** 2)) * length


def animation_frame(sprites: List[Surface], counter: float):
    """
    Returns current frame of an animation based on the given counter.

    :param sprites: list of sprites
    :param counter: game counter
    :return: current frame
    """
    return sprites[int(counter % len(sprites))]


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
    return SCREEN_RECT.colliderect(Rect(rect.topleft + camera.offset, rect.size))


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
    return idx_inside_grid(get_grid_index(pos))


def get_grid_index(pos: ndarray) -> ndarray:
    """
    Returns the grid index of the given world position.

    Warning : the values will be negative or greater than the grid size if the position is outside the grid.

    :param pos: position in world space
    :return: grid index
    """
    return (pos // TILE_SIZE).astype(int)


def get_screen_grid(grid: ndarray, camera: Camera) -> ndarray:
    """
    Returns a sub grid of `tile_grid` which is the current tile grid visible on screen.

    :param grid: world grid
    :param camera: camera data
    :return: tile grid visible on screen
    """
    idx: ndarray = (get_grid_index(camera.top_left)).clip(0, GRID_SIZE - 1)  # conversion in grid space
    return grid[
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
