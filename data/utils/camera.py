from numpy import array, ndarray

from data.playerData import Player
from data.utils.screen import world_to_screen, SCREEN_CENTER


def do_camera_offset(screen_pos: ndarray, player: Player) -> ndarray:
    return screen_pos + SCREEN_CENTER - world_to_screen(array(player.rect.center))


def undo_camera_offset(screen_pos: ndarray, player: Player) -> ndarray:
    return screen_pos - SCREEN_CENTER + world_to_screen(array(player.rect.center))
