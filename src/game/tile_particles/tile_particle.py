from abc import abstractmethod

from numpy import ndarray
from numpy.random.mtrand import rand, choice
from pygame import Surface

from src.utils.constants import TILE_SIZE


class TileParticle:
    """
    Particles emitted from some tiles.
    Has its position updated every frame until its timer reaches its lifespan.
    """

    def __init__(self, tile_position: ndarray):
        self._position: ndarray = self._initial_position(tile_position)  # in world space
        self._alive: bool = True

    def _expire(self):
        self._alive = False

    @property
    def alive(self):
        return self._alive

    @staticmethod
    def _initial_position(position: ndarray) -> ndarray:
        return position + rand(2) * choice([-1, 1], 2) * TILE_SIZE / 2

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def display(self, screen: Surface, camera_offset: ndarray) -> None:
        pass
