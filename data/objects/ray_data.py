from dataclasses import dataclass

from numpy import ndarray, array


@dataclass(frozen=True)
class Ray:
    start: ndarray = array((0, 0), dtype=float)  # start position of the ray in world space
    end: ndarray = array((0, 0), dtype=float)  # end position of the ray in world space
    power: float = 0.  # ray is effective is power is greater than 0
