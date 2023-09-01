from numpy import ndarray, around, array
from pygame import Surface, Rect, draw
from pygame.event import Event, post

from src.utils.constants import GRID_HEIGHT, SCREEN_SIZE, GRID_WIDTH, TILE_EDGE, TILE_SIZE, LAVA_SPRITES, \
    LAVA_SPEED, LAVA_TRIGGER_HEIGHT, LAVA_COLOR
from src.utils.events import LAVA_TRIGGERED
from src.utils.utils import world_to_grid, animation_frame


class Lava:
    """
    Rectangle that rises up through the map when player reaches a certain height.
    The game ends if it reaches the player.
    """

    def __init__(self):
        self._y: float = GRID_HEIGHT * TILE_EDGE
        self._triggered: bool = False

    @property
    def y(self):
        return self._y

    def update(self, player_y: float, delta: float) -> None:
        """
        Updates lava's height and triggered state.

        :param player_y: player's y coordinates in world space
        :param delta: delta between two frames
        """
        # lava is triggered when player reached a certain height
        if not self._triggered and self._is_player_above_trigger(player_y):
            self._triggered = True
            self._fire_triggered_event()

        # lava is moving up
        if self._triggered:
            self._y -= LAVA_SPEED * delta

    @staticmethod
    def _is_player_above_trigger(player_y: float) -> bool:
        return player_y <= LAVA_TRIGGER_HEIGHT * TILE_EDGE

    @staticmethod
    def _fire_triggered_event() -> None:
        triggered: Event = Event(LAVA_TRIGGERED)
        post(triggered)

    def display(self, screen: Surface, camera_offset: ndarray, time_elapsed: float) -> None:
        """
        Displays lava on screen.

        :param screen: screen surface
        :param camera_offset: camera object
        :param time_elapsed: real time elapsed since start of the game
        """
        height_offset: float = float(around(self._y + camera_offset[1]))  # needs to be rounded to match display
        width: float = float(SCREEN_SIZE[0])
        height: float = float(SCREEN_SIZE[1] - height_offset)

        lava_rect = Rect(0, height_offset, width, height)
        draw.rect(screen, LAVA_COLOR, lava_rect)

        # clipping lava rect position on tile grid...
        world_position: ndarray = lava_rect.topleft + array((0, 1)) - camera_offset
        grid_position: ndarray = world_to_grid(world_position)
        screen_position: ndarray = grid_position * TILE_SIZE + camera_offset

        # ...to display lava sprites along the grid on the x-axis
        for i in range(GRID_WIDTH + 1):
            screen.blit(
                animation_frame(LAVA_SPRITES, time_elapsed),
                around((screen_position[0] + TILE_EDGE * i, lava_rect.y - 1))
            )
