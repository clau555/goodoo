from threading import Timer
from typing import Dict

from numpy import ndarray, zeros
from numpy.random import randint
from pygame import Surface, Rect
from pygame.event import Event, post
from pygame.transform import rotate

from src.game.tile_particles.mushroom_particle import MushroomParticle
from src.game.tile_particles.tile_particle import TileParticle
from src.game.tiles.tile import Tile
from src.utils.constants import MUSHROOM_SPRITE, MUSHROOM_BUMP_FACTOR, MUSHROOM_SHAKE_DURATION, MUSHROOM_SHAKING_OFFSET
from src.utils.events import MUSHROOM_BUMPED


class Mushroom(Tile):
    """
    Mushroom tile, makes the player bounce on it on collision.
    """

    def __init__(self, rect: Rect, angle: int):
        sprite: Surface = rotate(MUSHROOM_SPRITE, angle)
        super().__init__(rect, sprite)
        self._is_shaking: bool = False
        self._shaking_timer: Timer = self._new_timer()

    def _new_timer(self) -> Timer:
        return Timer(MUSHROOM_SHAKE_DURATION, self._stop_shaking)

    def _stop_shaking(self) -> None:
        self._is_shaking = False

    def create_particle(self, position: ndarray) -> TileParticle:
        return MushroomParticle(position)

    def collided_with_player(self, player_velocity: float) -> float:
        self._is_shaking = True
        self._restart_timer()
        self._fire_collision_event()
        return player_velocity * MUSHROOM_BUMP_FACTOR

    def _restart_timer(self) -> None:
        self._shaking_timer.cancel()
        self._shaking_timer = self._new_timer()
        self._shaking_timer.start()

    def _fire_collision_event(self) -> None:
        args: Dict = {"mushroom": self}
        collision: Event = Event(MUSHROOM_BUMPED, args)
        post(collision)

    def display(self, screen: Surface, camera_offset: ndarray) -> None:
        shaking_offset: ndarray = zeros(2)
        if self._is_shaking:
            shaking_offset = randint(-MUSHROOM_SHAKING_OFFSET, MUSHROOM_SHAKING_OFFSET, 2)
        super().display(screen, camera_offset + shaking_offset)
