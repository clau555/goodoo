from dataclasses import replace

from numpy import ndarray, array, ndenumerate
from numpy.linalg import linalg
from pygame.rect import Rect

from data.objects.player_data import Player
from data.utils.constants import GRAVITY, PLAYER_MAX_V
from data.utils.functions import scale_vec, world_to_grid, get_neighbor_grid, idx_inside_grid


def update_player(player: Player, input_velocity: ndarray, tile_grid: ndarray, delta: float) -> Player:
    """
    Moves the player with according to the input velocity then collide with the tiles.
    If any collision occurs, the player is moved to the appropriate position, and its velocity is updated accordingly.

    :param player: player data
    :param input_velocity: velocity inputted by user
    :param tile_grid: world tile grid
    :param delta: time elapsed since last frame
    :return: updated player data
    """
    # velocity update
    v: ndarray = player.velocity + GRAVITY
    v = input_velocity if linalg.norm(input_velocity) != 0 else v

    # clamp velocity
    if linalg.norm(v) > PLAYER_MAX_V:
        v = scale_vec(v, PLAYER_MAX_V)

    # getting neighbor tiles to check collision
    player_idx: ndarray = world_to_grid(array(player.rect.center))
    if not idx_inside_grid(player_idx):
        raise ValueError("Player out of bounds")
    neighbor_tiles: ndarray = get_neighbor_grid(tile_grid, player_idx)

    rect: Rect = Rect(player.rect)
    pos: ndarray = array(player.pos)

    # x movement executes first
    pos[0] += v[0] * delta
    rect.x = pos[0]

    # x collision and correction
    for _, tile in ndenumerate(neighbor_tiles):
        if tile:

            if rect.colliderect(tile.rect):

                if v[0] > 0:
                    rect.right = tile.rect.left
                    pos[0] = rect.x
                    v[0] = 0
                    break

                elif v[0] < 0:
                    rect.left = tile.rect.right
                    pos[0] = rect.x
                    v[0] = 0
                    break

    # y movement executes second
    pos[1] += v[1] * delta
    rect.y = pos[1]

    # y collisions and correction
    for _, tile in ndenumerate(neighbor_tiles):
        if tile:

            if rect.colliderect(tile.rect):

                if v[1] > 0:
                    rect.bottom = tile.rect.top
                    pos[1] = rect.y
                    v = array((0, 0))
                    break

                elif v[1] < 0:
                    rect.top = tile.rect.bottom
                    pos[1] = rect.y
                    v[1] = 0
                    break

    return replace(player, pos=pos, rect=rect, velocity=v)
