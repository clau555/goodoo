from dataclasses import replace
from random import random, getrandbits
from typing import List

from numpy import around, ndarray, array
from pygame import Rect
from pygame.surface import Surface
from pygame.transform import flip

from src.model.constants import PLAYER_SPRITE, GRAVITY, SCREEN_SIZE, PLAYER_SIZE, PLAYER_MAX_V
from src.model.dataclasses import MenuParticle
from src.model.utils import clamp_vec


def spawn_menu_particle(particles: List[MenuParticle]) -> List[MenuParticle]:
    """
    Spawns a menu particle at a random position on top of the screen.

    :param particles: menu particle data
    :return: updated menu particles list
    """
    particles_: List[MenuParticle] = particles.copy()

    pos: ndarray = array((
        random() * SCREEN_SIZE[0] - PLAYER_SIZE[0],
        -PLAYER_SIZE[1]
    ))
    v: ndarray = array((1 - random() * 2, 0))

    particles_.append(MenuParticle(
        pos,
        Rect(tuple(pos), tuple(PLAYER_SIZE)),
        v,
        bool(getrandbits(1))
    ))
    return particles_


def update_display_menu_particles(particles: List[MenuParticle], screen: Surface, delta: float) -> List[MenuParticle]:
    """
    Updates then display on screen a menu particles list.

    :param particles: menu particles list
    :param screen: screen surface
    :param delta: delta between two frames
    :return: updated menu particles list
    """
    particles_: List[MenuParticle] = particles.copy()
    for i, _ in enumerate(particles_):

        particles_[i] = _update_particle(particles_[i], delta)
        _display_menu_particles(particles_[i], screen)

        if particles_[i].rect.top > SCREEN_SIZE[1]:
            particles_.pop(i)

    return particles_


def _display_menu_particles(particle: MenuParticle, screen: Surface) -> None:
    """
    Displays a menu particle on screen.
    It has the appearance of a player sprite.

    :param particle: menu particle data
    :param screen: screen surface
    """
    sprite: Surface = PLAYER_SPRITE if not particle.flipped else flip(PLAYER_SPRITE, True, False)
    screen.blit(sprite, around(particle.rect.topleft))


def _update_particle(particle: MenuParticle, delta: float) -> MenuParticle:
    """
    Update a menu particle position, making it fall.

    :param particle: menu particle data
    :param delta: delta between two frames
    :return: updated menu particle data
    """
    v: ndarray = particle.velocity + GRAVITY * delta
    v = clamp_vec(v, PLAYER_MAX_V)
    pos: ndarray = particle.pos + v

    rect: Rect = Rect(particle.rect)
    rect.topleft = around(pos)

    return replace(particle, pos=pos, rect=rect, velocity=v)
