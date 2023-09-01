import time

from numpy import ndarray, around
from pygame import Surface

from src.game.tile_particles.tile_particle import TileParticle
from src.utils.constants import ANIMATION_SPEED, AMETHYST_PARTICLE_SPRITES


class AmethystParticle(TileParticle):
    """
    Particles emitted by amethyst tile.
    Its life is as long as its animation.
    """

    def __init__(self, tile_position: ndarray):
        super().__init__(tile_position)
        self._sprite_index: int = 0

        self._counter: float = 0.
        self._last_time: float = time.time()

    def update(self) -> None:
        now: float = time.time()
        self._counter += now - self._last_time
        self._last_time = now

        self._sprite_index = int(self._counter / ANIMATION_SPEED * len(AMETHYST_PARTICLE_SPRITES))
        if self._animation_finished():
            self._expire()

    def _animation_finished(self) -> bool:
        return self._sprite_index >= len(AMETHYST_PARTICLE_SPRITES)

    def display(self, screen: Surface, camera_offset: ndarray) -> None:
        sprite: Surface = AMETHYST_PARTICLE_SPRITES[self._sprite_index]
        position: ndarray = around(around(self._position) + camera_offset)
        screen.blit(sprite, position)
