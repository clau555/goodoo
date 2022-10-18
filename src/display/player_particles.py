from dataclasses import replace
from typing import List

from numpy import ndarray, around
from numpy.random import rand, choice
from pygame import Surface, draw

from src.model.constants import GRAVITY, PLAYER_COLOR, PLAYER_PARTICLES_SPAWN_NUMBER, PLAYER_PARTICLE_INIT_VELOCITY, \
    PLAYER_PARTICLE_DECREASE_VELOCITY
from src.model.dataclasses import PlayerParticle, Camera


def spawn_player_particles(particles: List[PlayerParticle], pos: ndarray) -> List[PlayerParticle]:
    """
    Spawns a player at the given position, with a random velocity.

    :param particles: player particles data list
    :param pos: world position
    :return: updated player data list
    """
    particles_: List[PlayerParticle] = particles.copy()
    for _ in range(PLAYER_PARTICLES_SPAWN_NUMBER):
        velocity: ndarray = rand(2) * PLAYER_PARTICLE_INIT_VELOCITY * choice(a=(-1, 1), size=2)
        particles_.append(PlayerParticle(pos, velocity))
    return particles_


def update_display_player_particles(
        particles: List[PlayerParticle],
        screen: Surface,
        camera: Camera,
        delta: float
) -> List[PlayerParticle]:
    """
    Updates then display player particles, decreasing its radius and being affected by gravity.

    :param particles: player particles data
    :param screen: screen surface
    :param camera: camera data
    :param delta: delta between two frames
    :return: updated player data
    """
    particles_: List[PlayerParticle] = particles.copy()

    for i, _ in enumerate(particles_):

        particles_[i] = _update_player_particle(particles_[i], delta)

        if particles_[i].radius <= 0:
            particles_.pop(i)
        else:
            _display_player_particle(particles_[i], screen, camera)

    return particles_


def _update_player_particle(particle: PlayerParticle, delta: float) -> PlayerParticle:
    """
    Updates a single player particle.

    :param particle: player particle data
    :param delta: delta between two frames
    :return: updated player particle data
    """
    v: ndarray = particle.velocity + GRAVITY * delta
    radius: float = particle.radius - PLAYER_PARTICLE_DECREASE_VELOCITY * delta
    pos: ndarray = particle.pos + v

    return replace(
        particle,
        pos=pos,
        velocity=v,
        radius=radius
    )


def _display_player_particle(particle: PlayerParticle, screen: Surface, camera: Camera) -> None:
    """
    Displays a single player particle.

    :param particle: player particle data
    :param screen: screen surface
    :param camera: camera data
    :return: None
    """
    draw.circle(
        screen,
        PLAYER_COLOR,
        around(particle.pos + camera.offset),
        particle.radius
    )
