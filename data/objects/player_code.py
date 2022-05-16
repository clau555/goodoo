from dataclasses import replace

from numpy import ndarray, array, ndenumerate
from numpy.linalg import linalg
from pygame.rect import Rect

from data.objects.player_data import Player
from data.utils.constants import GRAVITY, PLAYER_MAX_V
from data.utils.functions import scale, get_grid_index, get_neighbor_grid, idx_inside_grid


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
        v = scale(v, PLAYER_MAX_V)

    # getting neighbor tiles to check collision
    player_idx: ndarray = get_grid_index(array(player.rect.center))
    if not idx_inside_grid(player_idx):
        raise ValueError("Player out of bounds")
    neighbor_tiles: ndarray = get_neighbor_grid(tile_grid, player_idx)

    rect: Rect = Rect(player.rect)
    on_ground: bool = False

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
