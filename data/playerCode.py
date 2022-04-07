import dataclasses
from typing import Tuple

import pygame.display
from pygame import Rect, Vector2

from data.constants import GRAVITY, PLAYER_MAX_V, TILE_EDGE
from data.playerData import PlayerData
from data.tileData import TileData


def display_player(player: PlayerData) -> None:
    """
    Display the player's sprite on the screen.

    :param player: player object
    """
    pygame.display.get_surface().blit(player.sprite, player.rect.topleft)


def get_grid_index(player: PlayerData) -> Tuple[int, int]:
    return player.rect.centerx // TILE_EDGE, player.rect.centery // TILE_EDGE


def update_velocity(player: PlayerData, beam_velocity: Vector2) -> PlayerData:
    """
    Update the player's velocity based on the beam's velocity.
    Normal gravity is applied if beam's velocity is zero.

    :param player: player object
    :param beam_velocity: beam's velocity
    :return: updated player object
    """

    v: Vector2 = player.velocity + GRAVITY
    v = beam_velocity if beam_velocity.xy != (0.0, 0.0) else v

    # clamp velocity
    if v.length() > PLAYER_MAX_V:
        v.scale_to_length(PLAYER_MAX_V)

    return dataclasses.replace(player, velocity=v)


def move_and_collide(
        player: PlayerData,
        tiles: list[TileData],
        delta: float
) -> PlayerData:
    """
    Move the player with its current velocity then collide with the tiles.
    If any collision occurs, the player is moved to the appropriate position.

    :param player: player object
    :param tiles: neighboring tiles
    :param delta: time elapsed since last frame
    :return: updated player object
    """

    rect: Rect = Rect(player.rect.topleft, player.rect.size)
    on_ground: bool = False
    v: Vector2 = Vector2(player.velocity)

    # x movement and collision
    rect.x += int(v.x * delta)

    for tile in tiles:
        if rect.colliderect(tile.rect):

            if v.x > 0:
                rect.right = tile.rect.left
                v.x = 0
                break

            elif v.x < 0:
                rect.left = tile.rect.right
                v.x = 0
                break

    # y movement and collision
    rect.y += int(v.y * delta)

    for tile in tiles:
        if rect.colliderect(tile.rect):

            if v.y > 0:
                rect.bottom = tile.rect.top
                on_ground = True
                v.xy = 0, 0
                break

            elif v.y < 0:
                rect.top = tile.rect.bottom
                v.y = 0
                break

    return dataclasses.replace(
        player, rect=rect, velocity=v, on_ground=on_ground
    )
