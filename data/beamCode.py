import dataclasses
from typing import List

import pygame
from pygame.math import Vector2
from pygame.surface import Surface

from data.beamData import BeamData
from data.constants import BEAM_STRENGTH, RED, BEAM_DECREASE, TILE_EDGE, BEAM_VECTOR_STEP, \
    BEAM_MAX_VECTOR_STEP
from data.playerData import PlayerData
from data.tileData import TileData


def display_beam(beam: BeamData, screen: Surface) -> None:
    pygame.draw.line(
        screen,
        RED,
        beam.start,
        beam.end,
        int(beam.power * TILE_EDGE / 2)
    )


def update_beam(beam: BeamData, player: PlayerData, tiles: List[TileData], delta: float) -> BeamData:

    start: Vector2 = Vector2(player.rect.center)
    end: Vector2 = Vector2(start)

    step: Vector2 = pygame.mouse.get_pos() - start
    step.scale_to_length(BEAM_VECTOR_STEP)

    # increasing vector until it collides with a tile
    end += step
    collide: bool = False
    for _ in range(BEAM_MAX_VECTOR_STEP):

        for tile in tiles:
            if tile.rect.collidepoint(tuple(end)):
                collide = True
                break

        if collide:
            break

        end += step

    power: float = beam.power - BEAM_DECREASE * delta
    power = power if beam.power > 0 else 0  # clamp power to 0

    return dataclasses.replace(beam, start=start, end=end, power=power)


def fire(beam: BeamData) -> BeamData:
    return dataclasses.replace(beam, power=1)


def get_beam_velocity(beam: BeamData) -> Vector2:
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
