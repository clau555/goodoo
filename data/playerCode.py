from dataclasses import replace

from numpy import ndarray, array
from numpy.linalg import linalg
from pygame.rect import Rect
from pygame.surface import Surface

from data.playerData import Player
from data.tileData import Tile
from data.utils.constants import GRAVITY, PLAYER_MAX_V
from data.utils.math import scale
from data.utils.screen import world_to_screen


def display_player(player: Player, screen: Surface) -> None:
    """
    Displays the player's sprite on the screen.

    :param player: player data
    :param screen: screen surface
    """
    screen.blit(player.sprite, world_to_screen(array(player.rect.topleft)))


def update_velocity(player: Player, beam_velocity: ndarray) -> Player:
    """
    Updates the player's velocity based on the beam's velocity.
    Normal gravity is applied if beam's velocity is zero.

    :param player: player data
    :param beam_velocity: beam's velocity
    :return: updated player data
    """
    v: ndarray = player.velocity + GRAVITY
    v = beam_velocity if linalg.norm(beam_velocity) != 0 else v

    # clamp velocity
    if linalg.norm(v) > PLAYER_MAX_V:
        v = scale(v, PLAYER_MAX_V)

    return replace(player, velocity=v)


def move_and_collide(player: Player, tiles: list[Tile], delta: float) -> Player:
    """
    Moves the player with its current velocity then collide with the tiles.
    If any collision occurs, the player is moved to the appropriate position.
    Updates also player's velocity.

    :param player: player data
    :param tiles: neighboring tiles
    :param delta: time elapsed since last frame
    :return: updated player data
    """
    rect: Rect = Rect(player.rect.topleft, player.rect.size)
    on_ground: bool = False
    v: ndarray = player.velocity

    # x movement clipped to world pixels
    rect.x += int(v[0] * delta)

    # x collision
    for tile in tiles:
        if rect.colliderect(tile.rect):

            if v[0] > 0:
                rect.right = tile.rect.left
                v[0] = 0
                break

            elif v[0] < 0:
                rect.left = tile.rect.right
                v[0] = 0
                break

    # y movement clipped to world pixels
    rect.y += int(v[1] * delta)

    # y collisions
    for tile in tiles:
        if rect.colliderect(tile.rect):

            if v[1] > 0:
                rect.bottom = tile.rect.top
                on_ground = True
                v = array((0, 0))
                break

            elif v[1] < 0:
                rect.top = tile.rect.bottom
                v[1] = 0
                break

    return replace(player, rect=rect, velocity=v, on_ground=on_ground)
