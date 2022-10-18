from dataclasses import replace

from numpy import array, ndarray, around
from pygame import draw
from pygame.rect import Rect
from pygame.surface import Surface

from src.model.constants import LAVA_SPEED, GRID_WIDTH, LAVA_SPRITES, TILE_EDGE, SCREEN_SIZE, TILE_SIZE, \
    LAVA_TRIGGER_HEIGHT, LAVA_COLOR
from src.model.dataclasses import Camera, Lava, Player
from src.model.utils import animation_frame, world_to_grid


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
    draw.rect(screen, LAVA_COLOR, lava_rect)

    # clipping lava rect position on tile grid...
    grid_pos: ndarray = world_to_grid(lava_rect.topleft + array((0, 1)) - camera.offset)  # converts to grid space
    screen_pos: ndarray = grid_pos * TILE_SIZE + camera.offset  # converts back to screen space

    # ...to display lava sprites along the grid on the x-axis
    for i in range(GRID_WIDTH + 1):
        screen.blit(
            animation_frame(LAVA_SPRITES, timer),
            around((screen_pos[0] + TILE_EDGE * i, lava_rect.y - 1))
        )


def update_lava(lava: Lava, player: Player, delta: float) -> Lava:
    """
    Updates lava's height and triggered state.

    :param lava: lava data
    :param player: player data
    :param delta: delta between two frames
    :return: updated lava data
    """
    lava_: Lava = lava

    # lava is triggered when player reached a certain height
    if not lava_.triggered and player.pos[1] <= LAVA_TRIGGER_HEIGHT * TILE_EDGE:
        lava_ = replace(lava_, triggered=True)

    # lava is moving up
    if lava_.triggered:
        height: float = lava_.height - LAVA_SPEED * delta
        lava_ = replace(lava_, height=height)

    return lava_
