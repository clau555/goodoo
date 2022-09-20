from dataclasses import dataclass

from numpy import ndarray, zeros


@dataclass(frozen=True)
class Grapple:
    start: ndarray = zeros(2, dtype=float)  # start position of the grapple (=player position) in world space
    end: ndarray = zeros(2, dtype=float)  # end position of the grapple in world space
    head: ndarray = zeros(2, dtype=float)
    head_velocity: ndarray = zeros(2, dtype=float)
    head_start: ndarray = zeros(2, dtype=float)  # point at which the head is fired
