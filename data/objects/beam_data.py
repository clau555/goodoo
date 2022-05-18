from dataclasses import dataclass

from numpy import ndarray, array


@dataclass(frozen=True)
class Beam:
    start: ndarray = array((0, 0))  # start position of the beam in world space
    end: ndarray = array((0, 0))  # end position of the beam in world space
    power: float = 0.0  # beam is effective is power is greater than 0
