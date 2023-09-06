from abc import abstractmethod
from typing import Optional

from numpy import ndarray
from pygame import Rect, Surface

from src.game.tile_particles.tile_particle import TileParticle
from src.utils.utils import world_to_screen


class Tile:
    """
    Rect composing the world map and colliding with player.
    """

    def __init__(self, rect: Rect, sprite: Surface):
        self._rect: Rect = rect
        self._sprite: Surface = sprite

    @property
    def rect(self) -> Rect:
        return self._rect

    @property
    def sprite(self) -> Surface:
        return self._sprite

    def display(self, screen: Surface, camera_offset: ndarray) -> None:
        screen_position: ndarray = world_to_screen(self._rect.topleft, camera_offset)
        screen.blit(self._sprite, screen_position)

    @abstractmethod
    def create_particle(self, position: ndarray) -> Optional[TileParticle]:
        pass

    @abstractmethod
    def collided_with_player(self, player_velocity: float) -> float:
        """
        Meant to be fired when the player collides with this tile.

        :param player_velocity: velocity on one axis only of the player
        :return: repulsion velocity
        """
        return 0
