from typing import Tuple

from numpy import ndarray, sqrt, sum


def tupint(v: ndarray) -> Tuple[int, int]:
    """
    Converts a numpy vector to a tuple of ints.
    
    :param v: 2D numpy array
    :return: tuple of ints
    """
    return int(v[0]), int(v[1])


def scale(v: ndarray, length: float) -> ndarray:
    """
    Scales a vector to a given length.

    :param v: 2D numpy array
    :param length: length to scale to
    :return: scaled vector
    """
    return v / sqrt(sum(v**2)) * length
