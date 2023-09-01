import pygame
from numpy import ndarray, zeros, around, float64, absolute, array, array_equal
from numpy.linalg import norm
from pygame import Surface, draw

from src.utils.constants import PLAYER_COLOR, GRAPPLE_THICKNESS, GRAPPLE_HEAD_RADIUS, GRAPPLE_ACCELERATION, \
    GRAPPLE_VECTOR_STEP, GRAPPLE_HEAD_VELOCITY
from src.utils.utils import world_to_screen, world_to_grid, scale_vec, pos_inside_grid, new_array


class Grapple:
    """
    Line that starts from the player and goes to a target position.
    A head can be fired from the player position to go to the target position, at a certain speed.
    The grapple provides an output velocity that applied to the player when it reached its target.
    """

    def __init__(self):
        # start position of the grapple (=player position) in world space
        self._start: ndarray = new_array()
        # end position of the grapple in world space
        self._end: ndarray = new_array()
        # position at which the head is fired
        self._head_start: ndarray = new_array()
        # actual grapple head position
        self._head: ndarray = new_array()
        # speed of the head
        self._head_velocity: ndarray = new_array()

        self._firing: bool = False

    @property
    def is_attached(self) -> bool:
        """
        The grapple is considered attached if its head as reached the end point aimed by the user.

        :return: If the grappled is attached or not
        """
        return array_equal(self._head, self._end)

    @property
    def acceleration(self) -> ndarray:
        """
        :return: acceleration provided by grapple, meant to be applied to user input velocity
        """
        v: ndarray = self._end - self._start
        if self._firing and norm(v) != 0:
            return scale_vec(v, GRAPPLE_ACCELERATION)
        return new_array()

    def fire(self, cave_map: ndarray, camera_offset: ndarray) -> None:
        self._set_firing(cave_map, camera_offset)

    def unfire(self) -> None:
        self._firing = False

    def _set_firing(self, cave_map: ndarray, camera_offset: ndarray) -> None:
        """
        Triggered when the user fire the grapple.
        It traces a line in the direction aimed by the user to set the end point the grapple must reach.
        The end point is fixed as soon as the line touches a solid tile.

        :param cave_map: map of solid tiles
        :param camera_offset: camera offset from world origin
        """
        self._firing = True

        end: ndarray = array(self._start).astype(float64)
        step: ndarray = array(pygame.mouse.get_pos()) - camera_offset - self._start

        if norm(step) != 0:
            step = scale_vec(step, GRAPPLE_VECTOR_STEP)
            inside_grid: bool = True
            end += step

            # increasing vector until it collides with a tile or goes out of screen
            while not self._colliding(end, cave_map) and inside_grid:
                end += step
                inside_grid = pos_inside_grid(end)

        # head velocity
        head_velocity: ndarray = zeros(2).astype(float64)
        v: ndarray = end - self._start
        if norm(v) != 0:
            head_velocity = scale_vec(v, GRAPPLE_HEAD_VELOCITY)

        self._end = end
        self._head_velocity = head_velocity
        self._head_start = self._start

    def update(self, player_center: ndarray, delta: float) -> None:
        self._start = player_center
        if self._firing:
            self._update_moving(delta)
        else:
            self._update_static()

    def _update_moving(self, delta: float) -> None:
        """
        Behavior of the grapple when the player is firing it.

        :param delta: delta between two frames
        """
        head: ndarray = self._head + self._head_velocity * delta
        diff: ndarray = absolute(self._end - self._head_start) - absolute(head - self._head_start)
        if diff[0] < 0 or diff[1] < 0:
            head = self._end
        self._head = head

    def _update_static(self) -> None:
        """
        Behavior of the grapple when the player is not firing it.
        It simply follows the player position and has no length.
        """
        self._head = self._start
        self._head_start = self._start

    @staticmethod
    def _colliding(point: ndarray, tile_grid: ndarray) -> bool:
        idx: ndarray = world_to_grid(point)
        return tile_grid[idx[0], idx[1]] is not None

    def display(self, player_alive: bool, screen: Surface, camera_offset: ndarray) -> None:
        if not player_alive:
            return
        self._draw_line(screen, camera_offset)
        self._draw_head(screen, camera_offset)

    def _draw_line(self, screen: Surface, camera_offset: ndarray) -> None:
        draw.line(
            screen,
            PLAYER_COLOR,
            world_to_screen(around(self._start), camera_offset),
            world_to_screen(around(self._head), camera_offset),
            GRAPPLE_THICKNESS
        )

    def _draw_head(self, screen: Surface, camera_offset: ndarray) -> None:
        draw.circle(
            screen,
            PLAYER_COLOR,
            world_to_screen(around(self._head), camera_offset),
            GRAPPLE_HEAD_RADIUS
        )
