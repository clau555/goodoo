import dataclasses
import pygame.display
from pygame import Rect, Vector2

from data.constants import GRAVITY
from data.playerData import PlayerData
from data.tileData import TileData


def display_player(player: PlayerData) -> None:
    """
    Display the player's sprite on the screen.

    :param player: player object
    """
    pygame.display.get_surface().blit(player.sprite, player.rect.topleft)


def update_velocity(player: PlayerData, input_v: Vector2) -> PlayerData:
    """
    Update the player's velocity based on user inputs
    and environmental factors such as gravity and frictions.

    :param player: player object
    :param input_v: velocity inputted by user
    :return: updated player object
    """

    v: Vector2 = Vector2(0, 0)

    v.x = input_v.x

    # gravity
    v.y = player.velocity.y + input_v.y + GRAVITY

    """
    # x-axis friction
    if input_v.x > 0:
        v.x -= FRICTION
    elif input_v.x < 0:
        v.x += FRICTION

    # clamp velocity
    if v.length() > PLAYER_MAX_V:
        v.scale_to_length(PLAYER_MAX_V)
    """

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

            elif v.x < 0:
                rect.left = tile.rect.right
                v.x = 0

    # y movement and collision
    rect.y += int(v.y * delta)

    for tile in tiles:
        if rect.colliderect(tile.rect):

            if v.y > 0:
                rect.bottom = tile.rect.top
                on_ground = True
                v.y = 0

            elif v.y < 0:
                rect.top = tile.rect.bottom
                v.y = 0

    return dataclasses.replace(
        player, rect=rect, velocity=v, on_ground=on_ground
    )
