from dataclasses import dataclass

from numpy import ndarray, array


@dataclass(frozen=True)
class Ray:
    # TODO revamp data as `start` as it is always the same as `player.rect.center`
    start: ndarray = array((0, 0), dtype=float)  # start position of the ray in world space
    end: ndarray = array((0, 0), dtype=float)  # end position of the ray in world space
