from dataclasses import replace

from numpy import ndarray, array, ndenumerate, around
from numpy.linalg import linalg
from pygame import Surface
from pygame.rect import Rect
from pygame.transform import flip

from data.objects.camera_data import Camera
from data.objects.player_data import Player
from data.objects.ray_data import Ray
from data.utils.constants import GRAVITY, PLAYER_MAX_V, BONUS_VALUE, PLAYER_MAX_GOO, PLAYER_SPRITES, PLAYER_PALE_SPRITES
from data.utils.functions import scale_vec, world_to_grid, get_neighbor_grid, idx_inside_grid, animation_frame


def display_player(player: Player, ray: Ray, screen: Surface, camera: Camera, timer: float) -> None:
    """
    Displays the player on the screen.
    The player is oriented towards the direction of the ray.
    The more goo the player has, the more it will be colored.

    :param player: player data
    :param ray: ray data
    :param screen: screen surface
    :param camera: camera data
    :param timer: game timer
    """
    screen_pos: ndarray = around(player.rect.topleft + camera.offset)

    player_sprite: Surface = animation_frame(PLAYER_SPRITES, timer)
    player_sprite.set_alpha(int(player.goo / PLAYER_MAX_GOO * 255))

    if ray.start[0] - ray.end[0] < 0:
        screen.blit(animation_frame(PLAYER_PALE_SPRITES, timer), screen_pos)
        screen.blit(player_sprite, screen_pos)
    else:
        screen.blit(flip(animation_frame(PLAYER_PALE_SPRITES, timer), True, False), screen_pos)
        screen.blit(flip(player_sprite, True, False), screen_pos)


def update_player(player: Player, input_velocity: ndarray, tile_grid: ndarray, delta: float) -> Player:
    """
    Moves the player according to the input velocity then collide with the tiles.
    If any collision occurs, the player is moved to the appropriate position, and its velocity is updated accordingly.

    :param player: player data
    :param input_velocity: velocity inputted by user
    :param tile_grid: world tile grid
    :param delta: delta between two frames
    :return: updated player data
    """
    # velocity update
    v: ndarray = player.velocity + GRAVITY * delta
    v = input_velocity if linalg.norm(input_velocity) != 0 else v

    # clamp velocity
    if linalg.norm(v) > PLAYER_MAX_V:
        v = scale_vec(v, PLAYER_MAX_V)

    # getting neighbor tiles to check collision
    player_idx: ndarray = world_to_grid(array(player.rect.center))
    if not idx_inside_grid(player_idx):
        raise ValueError("Player out of bounds")
    neighbor_tiles: ndarray = get_neighbor_grid(tile_grid, player_idx)

    pos: ndarray = array(player.pos)
    rect: Rect = Rect(player.rect)

    # x movement executes first
    pos[0] += v[0] * delta
    rect.x = round(pos[0])

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
    rect.y = round(pos[1])

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


def add_goo_from_bonus(player: Player) -> Player:
    """
    Adds the `BONUS_VALUE` to player goo quantity.
    Player's goo quantity is capped to `PLAYER_MAX_GOO`.

    :param player: player data
    :return: updated player data
    """
    goo: int = player.goo + BONUS_VALUE
    goo = goo if goo < PLAYER_MAX_GOO else PLAYER_MAX_GOO
    return replace(player, goo=goo)


def decrease_goo(player: Player) -> Player:
    """
    Decrease player's goo quantity by one, at a minimum of zero.

    :param player: player data
    :return: updated player data
    """
    goo: int = player.goo - 1 if player.goo > 0 else 0
    return replace(player, goo=goo)
