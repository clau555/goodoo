from dataclasses import replace
from random import random

from numpy import around, ndarray, array
from numpy.random import rand, choice, random_sample
from pygame import draw
from pygame.surface import Surface

from src.model.constants import ANIMATION_SPEED, AMETHYST_PARTICLE_SPRITES, TILE_SIZE, MUSHROOM_PARTICLE_LIFESPAN, \
    MUSHROOM_PARTICLE_VELOCITY_NORM, MUSHROOM_PARTICLE_RADIUS, MUSHROOM_PARTICLE_COLOR, \
    MUSHROOM_PARTICLE_LIGHT_RADIUS, MUSHROOM_PARTICLE_LIGHT_TRANSPARENCY, BLACK
from src.model.dataclasses import ObstacleParticle, Camera, ObstacleParticles, Player
from src.model.utils import scale_vec


def spawn_obstacle_particle(particles: list[ObstacleParticle], pos: ndarray) -> list[ObstacleParticle]:
    """
    Spawns a particle in a particle list at the given world position.

    :param particles: particles data list
    :param pos: world position
    :return: updated particles data list
    """
    particles_: list[ObstacleParticle] = particles.copy()
    particle_pos: ndarray = pos + rand(2) * choice([-1, 1], 2) * TILE_SIZE / 2
    particles_.append(ObstacleParticle(particle_pos))
    return particles_


def spawn_colliding_mushrooms_particles(
        player: Player,
        obstacle_particles: ObstacleParticles
) -> ObstacleParticles:
    """
    Returns the obstacle particles data with mushroom particles spawned at the mushroom's position.

    :param player: player data
    :param obstacle_particles: obstacle particles data
    :return: updated obstacle particles data
    """
    for mushroom in player.colliding_mushrooms:
        for _ in range(5):
            obstacle_particles = replace(obstacle_particles, mushroom=spawn_obstacle_particle(
                obstacle_particles.mushroom,
                array(mushroom.rect.center) + (random_sample(2) - 0.5) * 20
            ))
    return obstacle_particles


def update_display_amethyst_particles(
        particles: ObstacleParticles,
        screen: Surface,
        camera: Camera,
        delta_time: float
) -> ObstacleParticles:
    """
    Updates and display amethyst particles on screen.
    Increments their timer and removes them if they finished their animation.

    :param particles: amethyst particles data list
    :param screen: screen surface
    :param camera: camera data
    :param delta_time: delta time between two frames
    :return: updated particles data list
    """
    particles_: list[ObstacleParticle] = particles.amethyst
    for i, _ in enumerate(particles_):

        particles_[i] = replace(particles_[i], timer=particles_[i].timer + delta_time)
        sprite_idx: int = int(particles_[i].timer / ANIMATION_SPEED * len(AMETHYST_PARTICLE_SPRITES))

        # particle dies when animation finishes
        if sprite_idx >= len(AMETHYST_PARTICLE_SPRITES):
            particles_.pop(i)
        else:
            screen.blit(AMETHYST_PARTICLE_SPRITES[sprite_idx], around(around(particles_[i].pos) + camera.offset))

    return replace(particles, amethyst=particles_)


def update_display_mushroom_particles(
        particles: ObstacleParticles,
        screen: Surface,
        camera: Camera,
        delta_time: float
) -> ObstacleParticles:
    """
    Updates mushroom particles position and display on screen.
    Increments their timer and removes them if they finished their animation.

    :param particles: particles data list
    :param screen: screen surface
    :param camera: camera data
    :param delta_time: delta time between two frames
    :return: updated particles data list
    """
    particles_: list[ObstacleParticle] = particles.mushroom
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

    return replace(particles, mushroom=particles_)


def _display_mushroom_particle(particle: ObstacleParticle, screen: Surface, camera: Camera) -> None:
    """
    Displays a mushroom obstacle particle on screen.
    It is composed of one central small circle and one bigger transparent circle to make a light effect.

    :param particle: particle data
    :param screen: screen surface
    :param camera: camera data
    """

    # light transparent disk
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
