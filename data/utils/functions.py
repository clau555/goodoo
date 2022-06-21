from typing import List

from numpy import ndarray, clip, around, array
from numpy.linalg import norm
from pygame import Rect, Surface

from data.objects.camera_data import Camera
from data.utils.constants import SCREEN_SIZE, GRID_SIZE, TILE_SIZE, SCREEN_RECT, SCREEN_GRID_SIZE, ANIMATION_SPEED


def scale_vec(v: ndarray, length: float) -> ndarray:
    """
    Scales a vector to a given length.

    :param v: grid index
    :param length: length to scale to
    :return: scaled vector
    """
    return v / norm(v) * length


def animation_frame(sprites: List[Surface], timer: float) -> Surface:
    """
    Returns current frame of an animation based on the given timer.

    :param sprites: list of sprites
    :param timer: game timer
    :return: current frame
    """
    return sprites[int(((timer % ANIMATION_SPEED) / ANIMATION_SPEED) * len(sprites))]


def background_position(camera: Camera) -> ndarray:
    """
    Returns current background top left position in screen space.

    :param camera: camera data
    :return: background screen position
    """
    return array((clip(around(camera.offset[0]), 0, None), 0))


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
    Checks if a rectangle is visible on screen.

    :param rect: rectangle in world space
    :param camera: camera data
    :return: True if visible, False otherwise
    """
    return SCREEN_RECT.colliderect(Rect(rect.topleft + camera.offset, rect.size))


def idx_inside_grid(idx: ndarray) -> bool:
    """
    Checks if a grid space index is inside the grid.

    :param idx: index in grid space
    :return: True if inside grid, False otherwise
    """
    return (0 <= idx).all() and (idx < GRID_SIZE).all()


def pos_inside_grid(pos: ndarray) -> bool:
    """
    Checks if a world position is inside the grid.

    :param pos: position in world space
    :return: True if inside grid, False otherwise
    """
    return idx_inside_grid(world_to_grid(pos))


def world_to_grid(pos: ndarray) -> ndarray:
    """
    Returns the grid index of the given world position.

    Warning : the values will be negative or greater than the grid size if the position is outside the grid.

    :param pos: position in world space
    :return: grid index
    """
    return (pos // TILE_SIZE).astype(int)


def get_screen_grid(grid: ndarray, camera: Camera) -> ndarray:
    """
    Returns a sub grid of `grid` which is the current grid visible on screen.

    :param grid: world tile grid
    :param camera: camera data
    :return: tile grid visible on screen
    """
    idx: ndarray = (world_to_grid(camera.top_left)).clip(0, GRID_SIZE - 1)  # conversion in grid space
    return grid[
           idx[0]: idx[0] + SCREEN_GRID_SIZE[0] + 1,
           idx[1]: idx[1] + SCREEN_GRID_SIZE[1] + 1
           ]


def get_moore_neighborhood(grid: ndarray, idx: ndarray) -> ndarray:
    """
    Returns the Moore neighborhood grid of the given tile index.

    :param grid: world tile grid
    :param idx: tile index
    :return: index neighborhood
    """
    idx_: ndarray = idx.clip(1, GRID_SIZE - 2)
    return grid[
           idx_[0] - 1: idx_[0] + 2,
           idx_[1] - 1: idx_[1] + 2
           ]
