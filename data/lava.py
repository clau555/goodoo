from dataclasses import replace

from numpy import array, ndarray, around
from pygame import draw
from pygame.rect import Rect
from pygame.surface import Surface

from data.constants import LAVA_SPEED, GRID_WIDTH, LAVA_SPRITES, TILE_EDGE, SCREEN_SIZE, TILE_SIZE, GRID_HEIGHT, \
    LAVA_TRIGGER_HEIGHT, FONT, WHITE
from data.dataclasses import Camera, Lava, Player
from data.utils import animation_frame, world_to_grid


def display_lava(lava: Lava, screen: Surface, camera: Camera, timer: float) -> None:
    """
    Displays lava on screen.

    :param lava: lava data
    :param screen: screen surface
    :param camera: camera data
    :param timer: game timer
    """
    height_offset: ndarray = around(lava.height + camera.offset[1])  # needs to be rounded to match display
    lava_rect = Rect(
        0,
        height_offset,
        SCREEN_SIZE[0],
        SCREEN_SIZE[1] - height_offset
    )
    draw.rect(screen, (254, 56, 7), lava_rect)

    # clipping lava rect position on tile grid...
    grid_pos: ndarray = world_to_grid(lava_rect.topleft + array((0, 1)) - camera.offset)  # converts to grid space
    screen_pos: ndarray = grid_pos * TILE_SIZE + camera.offset  # converts back to screen space

    # ...to display lava sprites along the grid on the x-axis
    for i in range(GRID_WIDTH + 1):
        screen.blit(
            animation_frame(LAVA_SPRITES, timer),
            around((screen_pos[0] + TILE_EDGE * i, lava_rect.y - 1))
        )


def display_lava_counter(lava: Lava, player: Player, screen: Surface) -> None:
    """
    Displays lava counter on screen.

    :param lava: lava data
    :param player: player data
    :param screen: screen surface
    """

    # lava distance relative to player in number of tiles
    lava_distance: int = int((lava.height - player.rect.y) // TILE_EDGE)

    if lava_distance <= GRID_HEIGHT - LAVA_TRIGGER_HEIGHT:
        lava_distance_surf: Surface = FONT.render(str(lava_distance), False, WHITE)
        lava_distance_surf.set_alpha(255 - lava_distance / (GRID_HEIGHT - LAVA_TRIGGER_HEIGHT) * 255)

        lava_distance_rect: Rect = lava_distance_surf.get_rect()
        lava_distance_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - SCREEN_SIZE[1] // 8)

        screen.blit(lava_distance_surf, lava_distance_rect)


def update_lava(lava: Lava, delta: float) -> Lava:
    """
    Increases continuously lava's height.

    :param lava: lava data
    :param delta: delta between two frames
    :return: updated lava rectangle
    """
    height: float = lava.height - LAVA_SPEED * delta
    return replace(lava, height=height)


def set_lava_triggered(lava: Lava) -> Lava:
    """
    Sets lava's triggered state at True.

    :param lava: lava data
    :return: updated lava data
    """
    return replace(lava, triggered=True)
