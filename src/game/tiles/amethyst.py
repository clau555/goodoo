from numpy import ndarray
from pygame import Surface, Rect
from pygame.event import Event, post
from pygame.transform import rotate

from src.game.tile_particles.amethyst_particle import AmethystParticle
from src.game.tile_particles.tile_particle import TileParticle
from src.game.tiles.tile import Tile
from src.utils.constants import AMETHYST_SPRITE
from src.utils.events import PLAYER_DIES


class Amethyst(Tile):
    """
    Amethyst obstacle, kills the player on collision.
    """

    def __init__(self, rect: Rect, angle: int):
        sprite: Surface = rotate(AMETHYST_SPRITE, angle)
        super().__init__(rect, sprite)

    def create_particle(self, position: ndarray) -> TileParticle:
        return AmethystParticle(position)

    def collided_with_player(self, player_velocity) -> float:
        self._fire_player_death_event()
        return super().collided_with_player(player_velocity)

    @staticmethod
    def _fire_player_death_event() -> None:
        player_death: Event = Event(PLAYER_DIES)
        post(player_death)
