from numpy import ndarray, array
from numpy.random.mtrand import rand, choice
from pygame import draw, Surface

from src.utils.constants import GRAVITY, PLAYER_COLOR, PLAYER_PARTICLE_INIT_RADIUS, PLAYER_PARTICLE_DECREASE_VELOCITY, \
    PLAYER_PARTICLE_INIT_VELOCITY_STRENGTH
from src.utils.utils import world_to_screen


class PlayerParticle:
    """
    Particle occasionally emitted by player when colliding with an obstacle tile, and upon death.
    """

    def __init__(self, position: ndarray) -> None:
        self._position: ndarray = array(position)  # in world space
        self._velocity: ndarray = self._init_velocity()
        self._radius: float = PLAYER_PARTICLE_INIT_RADIUS

    @staticmethod
    def _init_velocity() -> ndarray:
        return rand(2) * PLAYER_PARTICLE_INIT_VELOCITY_STRENGTH * choice(a=(-1, 1), size=2)

    @property
    def alive(self) -> bool:
        return self._radius > 0

    def update(self, delta: float) -> None:
        self._velocity += GRAVITY * delta
        self._radius -= PLAYER_PARTICLE_DECREASE_VELOCITY * delta
        self._position += self._velocity

    def display(self, screen: Surface, camera_offset: ndarray) -> None:
        draw.circle(
            screen,
            PLAYER_COLOR,
            world_to_screen(self._position, camera_offset),
            self._radius
        )
