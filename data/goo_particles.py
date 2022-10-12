from dataclasses import replace
from typing import List

from numpy import ndarray, around
from numpy.random import rand, choice
from pygame import Surface
from pygame.draw import circle

from data.constants import GRAVITY, PLAYER_COLOR, GOO_PARTICLES_INIT_VELOCITY, GOO_PARTICLES_DECREASE_VELOCITY, \
    GOO_PARTICLES_SPAWN_NUMBER
from data.dataclasses import GooParticle, Camera


def spawn_goo_particles(particles: List[GooParticle], pos: ndarray) -> List[GooParticle]:
    """
    Spawns a goo at the given position, with a random velocity.

    :param particles: goo particles data list
    :param pos: world position
    :return: updated goo data list
    """
    particles_: List[GooParticle] = particles.copy()
    for _ in range(GOO_PARTICLES_SPAWN_NUMBER):
        velocity: ndarray = rand(2) * GOO_PARTICLES_INIT_VELOCITY * choice(a=(-1, 1), size=2)
        particles_.append(GooParticle(pos, velocity))
    return particles_


def update_and_display_goo_particles(
        particles: List[GooParticle],
        screen: Surface,
        camera: Camera,
        delta: float
) -> List[GooParticle]:
    """
    Updates then display goo particles, decreasing its radius and being affected by gravity.

    :param particles: goo particles data
    :param screen: screen surface
    :param camera: camera data
    :param delta: delta between two frames
    :return: updated goo data
    """
    particles_: List[GooParticle] = particles.copy()

    for i, _ in enumerate(particles_):

        particles_[i] = _update_goo_particle(particles_[i], delta)

        if particles_[i].radius <= 0:
            particles_.pop(i)
        else:
            _display_goo_particle(particles_[i], screen, camera)

    return particles_


def _update_goo_particle(particle: GooParticle, delta: float) -> GooParticle:
    """
    Updates a single goo particle.

    :param particle: goo particle data
    :param delta: delta between two frames
    :return: updated goo particle data
    """
    v: ndarray = particle.velocity + GRAVITY * delta
    radius: float = particle.radius - GOO_PARTICLES_DECREASE_VELOCITY * delta
    pos: ndarray = particle.pos + v

    return replace(
        particle,
        pos=pos,
        velocity=v,
        radius=radius
    )


def _display_goo_particle(particle: GooParticle, screen: Surface, camera: Camera) -> None:
    """
    Displays a single goo particle.

    :param particle: goo particle data
    :param screen: screen surface
    :param camera: camera data
    :return: None
    """
    circle(
        screen,
        PLAYER_COLOR,
        around(particle.pos + camera.offset),
        particle.radius
    )
