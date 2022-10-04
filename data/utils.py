from typing import List, Sequence

from numpy import ndarray
from numpy.linalg import norm
from pygame import Surface

from data.constants import GRID_SIZE, TILE_SIZE, SCREEN_GRID_SIZE, ANIMATION_SPEED, KEY_MAPS
from data.dataclasses import Camera


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


def visible_grid(grid: ndarray, camera: Camera) -> ndarray:
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


def moore_neighborhood(grid: ndarray, idx: ndarray) -> ndarray:
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


def is_pressed(action: str, pressed_keys: Sequence[bool], keyboard_layout) -> bool:
    """
    Checks if the given action is pressed.

    :param action: action pressed ("left", "right" or "down")
    :param pressed_keys: list of pressed keys
    :param keyboard_layout: keyboard layout ("QWERTY" or "AZERTY")
    :return: True if the action is pressed, False otherwise
    """
    for key in KEY_MAPS[keyboard_layout][action]:
        if pressed_keys[key]:
            return True
    return False
