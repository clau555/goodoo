from dataclasses import replace
from typing import List

from numpy import around, ndarray
from numpy.random import rand, choice
from pygame.surface import Surface

from data.constants import ANIMATION_SPEED, AMETHYST_PARTICLES_SPRITES, TILE_SIZE
from data.dataclasses import AmethystParticle, Camera


def spawn_amethyst_particle(particles: List[AmethystParticle], pos: ndarray) -> List[AmethystParticle]:
    """
    Spawns a particle at the given position.

    :param particles: amethyst particles data list
    :param pos: world position
    :return: updated particles data list
    """
    particles_: List[AmethystParticle] = particles.copy()
    particle_pos: ndarray = pos + rand(2) * choice([-1, 1], 2) * TILE_SIZE / 2
    particles_.append(AmethystParticle(particle_pos))
    return particles_


def update_and_display_amethyst_particles(
        particles: List[AmethystParticle],
        screen: Surface,
        camera: Camera,
        delta_time: float
) -> List[AmethystParticle]:
    """
    Updates and displays particles on screen.
    Increments their timer and removes them if they finished their animation.

    :param particles: amethyst particles data list
    :param screen: screen surface
    :param camera: camera data
    :param delta_time: delta time between two frames
    :return: updated particles data list
    """
    particles_: List[AmethystParticle] = particles.copy()
    for i, _ in enumerate(particles_):

        particles_[i] = replace(particles_[i], timer=particles_[i].timer + delta_time)
        sprite_idx: int = int(particles_[i].timer / ANIMATION_SPEED * len(AMETHYST_PARTICLES_SPRITES))

        if sprite_idx >= len(AMETHYST_PARTICLES_SPRITES):
            particles_.pop(i)
        else:
            screen.blit(AMETHYST_PARTICLES_SPRITES[sprite_idx], around(around(particles_[i].pos) + camera.offset))

    return particles_
