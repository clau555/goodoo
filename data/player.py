from dataclasses import dataclass, replace

from pygame import Rect, Vector2
from pygame.surface import Surface

from data.utils.constants import GRAVITY, PLAYER_MAX_V, PLAYER_SPRITE
from data.tile import Tile
from data.utils.screen import world_to_screen


@dataclass(frozen=True)
class Player:
    rect: Rect
    sprite: Surface = PLAYER_SPRITE
    velocity: Vector2 = Vector2(0)
    on_ground: bool = False


def display_player(player: Player, screen: Surface) -> None:
    """
    Display the player's sprite on the screen.

    :param player: player object
    :param screen: screen surface
    """
    screen.blit(player.sprite, world_to_screen(player.rect.topleft))


def update_velocity(player: Player, beam_velocity: Vector2) -> Player:
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

    return replace(player, velocity=v)


def move_and_collide(
    player: Player,
    tiles: list[Tile],
    delta: float
) -> Player:
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

    # x movement clipped to world pixels
    rect.x += int(v.x * delta)

    # x collision
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

    # y movement clipped to world pixels
    rect.y += int(v.y * delta)

    # y collisions
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

    return replace(
        player, rect=rect, velocity=v, on_ground=on_ground
    )
