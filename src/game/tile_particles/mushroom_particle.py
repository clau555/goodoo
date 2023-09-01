from threading import Timer

from numpy import ndarray, array
from numpy.random import random
from pygame import Surface, draw

from src.game.tile_particles.tile_particle import TileParticle
from src.utils.constants import BLACK, MUSHROOM_PARTICLE_LIFESPAN, MUSHROOM_PARTICLE_VELOCITY_NORM, \
    MUSHROOM_PARTICLE_RADIUS, MUSHROOM_PARTICLE_COLOR, MUSHROOM_PARTICLE_LIGHT_RADIUS, \
    MUSHROOM_PARTICLE_LIGHT_TRANSPARENCY
from src.utils.utils import scale_vec, world_to_screen


class MushroomParticle(TileParticle):
    def __init__(self, tile_position: ndarray):
        super().__init__(tile_position)
        self._lifespan_timer: Timer = Timer(MUSHROOM_PARTICLE_LIFESPAN, self._expire)
        self._lifespan_timer.start()

    def update(self) -> None:
        # particle goes up in random direction
        velocity: ndarray = scale_vec(array((1 - random() * 2, -1)), MUSHROOM_PARTICLE_VELOCITY_NORM)
        self._position += velocity

    def display(self, screen: Surface, camera_offset: ndarray) -> None:
        """
        Displays a mushroom particle on screen.
        It is composed of one central small circle and one bigger transparent circle to make a light effect.

        :param screen: main screen surface
        :param camera_offset: camera offset from world origin
        """
        self._draw_halo(screen, camera_offset)
        self._draw_center(screen, camera_offset)

    def _draw_halo(self, screen: Surface, camera_offset: ndarray) -> None:
        surface: Surface = Surface((MUSHROOM_PARTICLE_LIGHT_RADIUS * 2, MUSHROOM_PARTICLE_LIGHT_RADIUS * 2))
        surface_center: ndarray = array((MUSHROOM_PARTICLE_LIGHT_RADIUS, MUSHROOM_PARTICLE_LIGHT_RADIUS))

        draw.circle(
            surface,
            MUSHROOM_PARTICLE_COLOR,
            surface_center,
            MUSHROOM_PARTICLE_LIGHT_RADIUS
        )
        surface.set_colorkey(BLACK)
        surface.set_alpha(MUSHROOM_PARTICLE_LIGHT_TRANSPARENCY)

        screen_position: ndarray = world_to_screen(self._position - surface_center, camera_offset)
        screen.blit(surface, screen_position)

    def _draw_center(self, screen: Surface, camera_offset: ndarray) -> None:
        draw.circle(
            screen,
            MUSHROOM_PARTICLE_COLOR,
            world_to_screen(self._position, camera_offset),
            MUSHROOM_PARTICLE_RADIUS
        )
