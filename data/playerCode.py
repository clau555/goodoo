from dataclasses import replace

from numpy import ndarray, array, ndenumerate
from numpy.linalg import linalg
from pygame.rect import Rect
from pygame.surface import Surface

from data.playerData import Player
from data.utils.constants import GRAVITY, PLAYER_MAX_V
from data.utils.utils import scale, get_grid_index, get_moore_neighbors, idx_inside_grid


def display_player(player: Player, screen: Surface, camera_offset: ndarray) -> None:
    """
    Displays the player's sprite on the screen.

    :param player: player data
    :param screen: screen surface
    :param camera_offset: camera offset
    """
    screen.blit(player.sprite, player.rect.topleft + camera_offset)


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


def move_and_collide(player: Player, tile_grid: ndarray, delta: float) -> Player:
    """
    Moves the player with its current velocity then collide with the tiles.
    If any collision occurs, the player is moved to the appropriate position.
    Updates also player's velocity.

    :param player: player data
    :param tile_grid: world grid
    :param delta: time elapsed since last frame
    :return: updated player data
    """
    rect: Rect = Rect(player.rect.topleft, player.rect.size)
    v: ndarray = player.velocity
    on_ground: bool = False

    # getting neighbor tiles to check collision
    player_idx: ndarray = get_grid_index(array(player.rect.center))
    if not idx_inside_grid(player_idx):
        raise ValueError("Player out of bounds")
    neighbor_tiles: ndarray = get_moore_neighbors(tile_grid, player_idx)

    # x movement executes first
    rect.x += v[0] * delta

    # x collision and correction
    for _, tile in ndenumerate(neighbor_tiles):
        if tile:

            if rect.colliderect(tile.rect):

                if v[0] > 0:
                    rect.right = tile.rect.left
                    v[0] = 0
                    break

                elif v[0] < 0:
                    rect.left = tile.rect.right
                    v[0] = 0
                    break

    # y movement executes second
    rect.y += v[1] * delta

    # y collisions and correction
    for _, tile in ndenumerate(neighbor_tiles):
        if tile:

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
