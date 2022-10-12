from dataclasses import replace

import pygame
from numpy import ndarray, array, zeros, absolute, around
from numpy.linalg import norm
from pygame.draw import line, circle
from pygame.surface import Surface

from data.constants import GRAPPLE_VECTOR_STEP, PLAYER_COLOR, GRAPPLE_ACCELERATION, GRAPPLE_HEAD_VELOCITY, \
    GRAPPLE_THICKNESS, GRAPPLE_HEAD_RADIUS
from data.dataclasses import Camera, Grapple, Player
from data.utils import scale_vec, world_to_grid, pos_inside_grid


def display_grapple(grapple: Grapple, screen: Surface, camera: Camera) -> None:
    """
    Displays the grapple on the screen.

    :param grapple: grapple data
    :param screen: screen surface
    :param camera: camera data
    """
    line(
        screen,
        PLAYER_COLOR,
        around(around(grapple.start) + camera.offset),
        around(around(grapple.head) + camera.offset),
        GRAPPLE_THICKNESS
    )
    circle(
        screen,
        PLAYER_COLOR,
        around(around(grapple.head) + camera.offset),
        GRAPPLE_HEAD_RADIUS
    )


def update_grapple_start(grapple: Grapple, player: Player) -> Grapple:
    """
    Updates the grapple start position to the player's position.

    :param grapple: grapple data
    :param player: player data
    :return: updated grapple data
    """
    return replace(grapple, start=array(player.rect.center).astype(float))


def fire(grapple: Grapple, tile_cave: ndarray, camera: Camera) -> Grapple:
    """
    Projects the grapple starting from the player's position
    to the mouse position and beyond until it collides with a tile.

    :param grapple: grapple data
    :param tile_cave: world tile grid
    :param camera: camera data
    :return: updated grapple data
    """

    # finding the end point of the grapple
    end: ndarray = array(grapple.start, dtype=float)
    step: ndarray = array(pygame.mouse.get_pos()) - camera.offset - grapple.start

    if norm(step) != 0:

        step = scale_vec(step, GRAPPLE_VECTOR_STEP)

        collide: bool = False
        inside_grid: bool = True

        end += step

        # increasing vector until it collides with a tile or goes out of screen
        while not collide and inside_grid:

            idx: ndarray = world_to_grid(end)
            if tile_cave[idx[0], idx[1]]:
                collide = True
            end += step
            inside_grid = pos_inside_grid(end)

    # head velocity
    head_velocity: ndarray = zeros(2)
    v: ndarray = end - grapple.start
    if norm(v) != 0:
        head_velocity = scale_vec(v, GRAPPLE_HEAD_VELOCITY)

    return replace(grapple, end=end, head=grapple.start, head_velocity=head_velocity, head_start=grapple.start)


def update_grapple_head(grapple: Grapple, delta: float) -> Grapple:
    """
    Updates the grapple head position making it fly towards the grapple end point.
    The head stops when it reaches the end point.

    :param grapple: grapple data
    :param delta: delta between two frames
    :return: updated grapple data
    """
    head: ndarray = grapple.head + grapple.head_velocity * delta
    diff: ndarray = absolute(grapple.end - grapple.head_start) - absolute(head - grapple.head_start)
    if diff[0] < 0 or diff[1] < 0:
        head = grapple.end
    return replace(grapple, head=head)


def reset_grapple_head(grapple: Grapple) -> Grapple:
    """
    Resets the grapple head position to the player's position.

    :param grapple: grapple data
    :return: updated grapple data
    """
    return replace(grapple, head=grapple.start, head_velocity=zeros(2), head_start=grapple.start)


def grapple_acceleration(grapple: Grapple) -> ndarray:
    """
    Returns the acceleration impulse the grapple would give to the player.

    :param grapple: grapple data
    :return: updated grapple data
    """
    v: ndarray = grapple.end - grapple.start
    if norm(v) != 0:
        return scale_vec(v, GRAPPLE_ACCELERATION)
    return array((0, 0))
