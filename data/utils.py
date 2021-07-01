from pygame.rect import Rect

from data.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SCALE, WORLD_WIDTH, WORLD_HEIGHT


def get_index_from_screen_position(screen_pos: tuple[int, int]) -> tuple[int, int]:
    """
    Returns a tile position on the indexed tile map from a position on screen.\n
    :param screen_pos: position on screen
    :return: position in the tile map
    """
    if 0 <= screen_pos[0] < SCREEN_WIDTH and 0 <= screen_pos[1] < SCREEN_HEIGHT:
        return screen_pos[0] // TILE_SCALE, screen_pos[1] // TILE_SCALE


def get_tile_position_from_index(index_pos: tuple[int, int]) -> tuple[int, int]:
    """
    Returns a tile position on screen from an index on the tile map.\n
    :param index_pos: position in the tile map
    :return: position on screen
    """
    if 0 <= index_pos[0] < WORLD_WIDTH and 0 <= index_pos[1] < WORLD_HEIGHT:
        return index_pos[0] * TILE_SCALE, index_pos[1] * TILE_SCALE


def get_tile_center_from_index(index_pos: tuple[int, int]) -> tuple[int, int]:
    """
    Returns a tile center position on screen from an index on the tile map.\n
    :param index_pos: position in the tile map
    :return: tile center position on screen
    """
    if 0 <= index_pos[0] < WORLD_WIDTH and 0 <= index_pos[1] < WORLD_HEIGHT:
        return (index_pos[0] * TILE_SCALE) + TILE_SCALE // 2, \
               (index_pos[1] * TILE_SCALE) + TILE_SCALE // 2


def get_item_placement_from_tile_position(screen_pos: tuple[int, int]) -> tuple[int, int]:
    """
    Returns the position on screen so that when an item is created
    at that position, it is centered inside its tile placement.\n
    :param screen_pos: tile position on screen
    :return: eventual item position on screen
    """
    if 0 <= screen_pos[0] < SCREEN_WIDTH and 0 <= screen_pos[1] < SCREEN_HEIGHT:
        return screen_pos[0] + TILE_SCALE // 4, \
               screen_pos[1] + TILE_SCALE // 4


def get_item_placement_from_index(index_pos: tuple[int, int]) -> tuple[int, int]:
    """
    Returns the position on screen so that when an item is created
    at that position, it is centered inside its tile placement.\n
    :param index_pos: position in the tile map
    :return: eventual item position on screen
    """
    if 0 <= index_pos[0] < WORLD_WIDTH and 0 <= index_pos[1] < WORLD_HEIGHT:
        return index_pos[0] * TILE_SCALE + TILE_SCALE // 4, \
               index_pos[1] * TILE_SCALE + TILE_SCALE // 4


def is_inside_screen(rect: Rect) -> bool:
    """
    Returns true if a rectangle object can be seen on the screen, even partially.\n
    :param rect: rectangle object
    :return: if the rectangle can be seen
    """
    return (0 < rect.left < SCREEN_WIDTH or 0 < rect.right < SCREEN_WIDTH) and \
           (0 < rect.top < SCREEN_HEIGHT or 0 < rect.bottom < SCREEN_HEIGHT)


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)
