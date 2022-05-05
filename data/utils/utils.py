from numpy import ndarray, sqrt, sum

from data.utils.constants import SCREEN_SIZE, GRID_SIZE


def is_inside_screen(pos: ndarray) -> bool:
    """
    Checks if a position is inside the screen.

    :param pos: screen position to check
    :return: True if inside screen, False otherwise
    """
    return (0 <= pos).all() and (pos < SCREEN_SIZE).all()


def is_inside_grid(idx: ndarray) -> bool:
    """
    Checks if an index is inside the grid.

    :param idx: 2D numpy array
    :return: True if inside grid, False otherwise
    """
    return (0 <= idx).all() and (idx < GRID_SIZE).all()


def scale(v: ndarray, length: float) -> ndarray:
    """
    Scales a vector to a given length.

    :param v: 2D numpy array
    :param length: length to scale to
    :return: scaled vector
    """
    return v / sqrt(sum(v**2)) * length
