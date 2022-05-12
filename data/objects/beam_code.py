from dataclasses import replace

import pygame
from numpy import ndarray, array
from numpy.linalg import linalg
from pygame.surface import Surface

from data.objects.beam_data import Beam
from data.objects.camera_data import Camera
from data.objects.player_data import Player
from data.utils.constants import BEAM_STRENGTH, BEAM_DECREASE, BEAM_VECTOR_STEP, TILE_EDGE
from data.utils.functions import scale, pos_inside_screen, get_grid_index, pos_inside_grid


def display_beam(beam: Beam, screen: Surface, camera: Camera) -> None:
    """
    Displays the beam on the screen.

    :param beam: beam data
    :param screen: screen surface
    :param camera: camera data
    """
    pygame.draw.line(
        screen,
        (255, 0, 0),
        beam.start + camera.offset,
        beam.end + camera.offset,
        int(beam.power * TILE_EDGE / 2)
    )


def update_beam(beam: Beam, player: Player, tile_grid: ndarray, camera: Camera, delta: float) -> Beam:
    """
    Updates the beam, decreasing its power and setting its start and end points.

    :param beam: beam data
    :param player: player data
    :param tile_grid: world grid
    :param camera: camera data, used to calculate mouse position in world
    :param delta: delta time
    :return: updated beam data
    """
    start: ndarray = array(player.rect.center).astype(float)
    end: ndarray = array(start)
    step: ndarray = array(pygame.mouse.get_pos()) - camera.offset - start

    if linalg.norm(step) != 0:

        collide: bool = False
        step = scale(step, BEAM_VECTOR_STEP)
        end += step

        # increasing vector until it collides with a tile or goes out of screen
        while not collide and pos_inside_screen(end, camera) and pos_inside_grid(end):

            idx: ndarray = get_grid_index(end)
            if tile_grid[idx[0], idx[1]]:
                collide = True
            end += step

    power: float = beam.power - BEAM_DECREASE * delta
    power = power if beam.power > 0 else 0  # clamp power to 0

    return replace(beam, start=start, end=end, power=power)


def fire_beam(beam: Beam) -> Beam:
    """
    Fires the beam, setting its power to the maximum.

    :param beam: beam data
    :return: updated beam data
    """
    return replace(beam, power=1)


def get_beam_velocity(beam: Beam) -> ndarray:
    """
    Returns the velocity impulse the beam would give to the player.
    Returns a zero vector if the beam has no power left.

    :param beam: beam data
    :return: updated beam data
    """
    if beam.power > 0:
        v: ndarray = beam.start - beam.end
        if linalg.norm(v) != 0:
            v = scale(v, BEAM_STRENGTH)
            return v
    return array((0, 0))
