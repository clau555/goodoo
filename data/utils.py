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


def neighbor_objects(pos: tuple[int, int], object_map: list[list]) -> list:
    """
    Returns the existing neighbor objects of a given position on screen.\n
    These objects are stored in the object_map argument, in which each index corresponds to a tile position.\n
    These objects can be for example tiles or items.\n
    The neighbors include at most the 8 surrounding tiles of the position and the tile on the given position itself.\n
    :param pos: position on screen
    :param object_map: 2D array map storing all objects
    :return: neighbor objects
    """
    tile_pos: tuple[int, int] = (clamp(pos[0], 0, SCREEN_WIDTH) // TILE_SCALE,
                                 clamp(pos[1], 0, SCREEN_HEIGHT) // TILE_SCALE)
    objects: list = []
    for i in range(tile_pos[0] - 1, tile_pos[0] + 2):
        for j in range(tile_pos[1] - 1, tile_pos[1] + 2):
            if 0 <= i < len(object_map) and 0 <= j < len(object_map[j]) and \
                    object_map[i][j] is not None:
                objects.append(object_map[i][j])
    return objects
