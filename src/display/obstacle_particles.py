from dataclasses import replace
from random import random
from typing import List

from numpy import around, ndarray, array
from numpy.random import rand, choice
from pygame import draw
from pygame.surface import Surface

from src.model.constants import ANIMATION_SPEED, AMETHYST_PARTICLE_SPRITES, TILE_SIZE, MUSHROOM_PARTICLE_LIFESPAN, \
    MUSHROOM_PARTICLE_VELOCITY_NORM, MUSHROOM_PARTICLE_RADIUS, MUSHROOM_PARTICLE_COLOR, \
    MUSHROOM_PARTICLE_LIGHT_RADIUS, MUSHROOM_PARTICLE_LIGHT_TRANSPARENCY, BLACK
from src.model.dataclasses import ObstacleParticle, Camera
from src.model.utils import scale_vec


def spawn_obstacle_particle(particles: List[ObstacleParticle], pos: ndarray) -> List[ObstacleParticle]:
    """
    Spawns a particle at the given position.

    :param particles: particles data list
    :param pos: world position
    :return: updated particles data list
    """
    particles_: List[ObstacleParticle] = particles.copy()
    particle_pos: ndarray = pos + rand(2) * choice([-1, 1], 2) * TILE_SIZE / 2
    particles_.append(ObstacleParticle(particle_pos))
    return particles_


def update_and_display_amethyst_particles(
        particles: List[ObstacleParticle],
        screen: Surface,
        camera: Camera,
        delta_time: float
) -> List[ObstacleParticle]:
    """
    Updates and display amethyst particles on screen.
    Increments their timer and removes them if they finished their animation.

    :param particles: amethyst particles data list
    :param screen: screen surface
    :param camera: camera data
    :param delta_time: delta time between two frames
    :return: updated particles data list
    """
    particles_: List[ObstacleParticle] = particles.copy()
    for i, _ in enumerate(particles_):

        particles_[i] = replace(particles_[i], timer=particles_[i].timer + delta_time)
        sprite_idx: int = int(particles_[i].timer / ANIMATION_SPEED * len(AMETHYST_PARTICLE_SPRITES))

        # particle dies when animation finishes
        if sprite_idx >= len(AMETHYST_PARTICLE_SPRITES):
            particles_.pop(i)
        else:
            screen.blit(AMETHYST_PARTICLE_SPRITES[sprite_idx], around(around(particles_[i].pos) + camera.offset))

    return particles_


def update_and_display_mushroom_particles(
        particles: List[ObstacleParticle],
        screen: Surface,
        camera: Camera,
        delta_time: float
) -> List[ObstacleParticle]:
    """
    Updates mushroom particles position and display on screen.
    Increments their timer and removes them if they finished their animation.

    :param particles: particles data list
    :param screen: screen surface
    :param camera: camera data
    :param delta_time: delta time between two frames
    :return: updated particles data list
    """
    particles_: List[ObstacleParticle] = particles.copy()
    for i, _ in enumerate(particles_):

        # particle goes up in random direction
        v: ndarray = scale_vec(array((1 - random() * 2, -1)), MUSHROOM_PARTICLE_VELOCITY_NORM)

        particles_[i] = replace(
            particles_[i],
            pos=particles_[i].pos + v,
            timer=particles_[i].timer + delta_time
        )

        # particle dies when its lifespan expires
        if particles_[i].timer >= MUSHROOM_PARTICLE_LIFESPAN:
            particles_.pop(i)
        else:
            _display_mushroom_particle(particles_[i], screen, camera)

    return particles_


def _display_mushroom_particle(particle: ObstacleParticle, screen: Surface, camera: Camera) -> None:
    """
    Displays a mushroom obstacle particle on screen.
    It is composed of one central small circle and one bigger transparent circle to make a light effect.

    :param particle: particle data
    :param screen: screen surface
    :param camera: camera data
    """

    # light blur
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
    screen.blit(surface, around(around(particle.pos) - surface_center + camera.offset))

    # particle center
    draw.circle(
        screen,
        MUSHROOM_PARTICLE_COLOR,
        around(around(particle.pos) + camera.offset),
        MUSHROOM_PARTICLE_RADIUS
    )
