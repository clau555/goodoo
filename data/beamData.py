from dataclasses import dataclass

from numpy import ndarray, array


@dataclass(frozen=True)
class Beam:
    start: ndarray = array((0, 0))
    end: ndarray = array((0, 0))
    power: float = 0.0
