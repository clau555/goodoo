from dataclasses import dataclass, replace
from typing import List

import pygame
from pygame.math import Vector2
from pygame.surface import Surface

from data.player import Player
from data.tile import Tile
from data.utils import BEAM_STRENGTH, RED, BEAM_DECREASE, \
    BEAM_VECTOR_STEP, TILE_EDGE, vec_to_screen
from data.utils.screen import tuple_to_pix, is_inside_screen


@dataclass(frozen=True)
class Beam:
    start: Vector2 = Vector2(0)
    end: Vector2 = Vector2(0)
    power: float = 0.0


def display_beam(beam: Beam, screen: Surface) -> None:
    """
    Displays the beam on the screen.

    :param beam: beam object
    :param screen: screen surface
    """
    pygame.draw.line(
        screen,
        RED,
        vec_to_screen(beam.start),
        vec_to_screen(beam.end),
        int(beam.power * TILE_EDGE / 2)
    )


def update_beam(
    beam: Beam,
    player: Player,
    tiles: List[Tile],
    delta: float
) -> Beam:
    """
    Updates the beam, decreasing its power and setting its start and end points.

    :param beam: beam object
    :param player: player object
    :param tiles: list of tile objects
    :param delta: delta time
    :return: updated beam object
    """
    start: Vector2 = Vector2(player.rect.center)
    end: Vector2 = Vector2(start)

    step: Vector2 = tuple_to_pix(pygame.mouse.get_pos()) - start

    if step.length() != 0:
        step.scale_to_length(BEAM_VECTOR_STEP)

        end += step
        collide: bool = False

        # increasing vector until it collides with a tile or goes out of screen
        while not collide and is_inside_screen(end):

            for tile in tiles:
                if tile.rect.collidepoint(tuple(end)):
                    collide = True
                    break

            end += step

    power: float = beam.power - BEAM_DECREASE * delta
    power = power if beam.power > 0 else 0  # clamp power to 0

    return replace(beam, start=start, end=end, power=power)


def fire_beam(beam: Beam) -> Beam:
    """
    Fires the beam, setting its power to the maximum.

    :param beam: beam object
    :return: updated beam object
    """
    return replace(beam, power=1)


def get_beam_velocity(beam: Beam) -> Vector2:
    """
    Returns the velocity impulse the beam would give to the player.
    Returns a zero vector if the beam has no power left.

    :param beam: beam object
    :return: updated beam object
    """
    if beam.power > 0:
        v: Vector2 = beam.start - beam.end
        v.scale_to_length(BEAM_STRENGTH)
        return v
    return Vector2(0)
