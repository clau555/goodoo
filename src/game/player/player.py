from copy import deepcopy

import pygame
from numpy import ndarray, array, around, ndenumerate, round
from pygame import Rect, Surface
from pygame.transform import flip

from src.game.tiles.tile import Tile
from src.utils.constants import GRAVITY, PLAYER_SPRITE, PLAYER_GROUND_SPRITES, PLAYER_MAX_V
from src.utils.utils import world_to_screen, animation_frame, world_to_grid, idx_inside_grid, moore_neighborhood, \
    clamp_vec, new_array


class Player:
    """
    Player is subject to physics and collision with tiles.
    He's influenced by an input velocity.
    """

    def __init__(self, position: ndarray, rect: Rect) -> None:
        self._position: ndarray = position  # in world space
        self._rect: Rect = rect
        self._velocity: ndarray = new_array()
        self._on_ground: bool = False
        self._alive: bool = True

    @property
    def world_position(self) -> ndarray:
        return self._position

    @property
    def rect(self) -> Rect:
        return self._rect

    @property
    def alive(self) -> bool:
        return self._alive

    def on_ground(self):
        return self._on_ground

    def kill(self):
        self._alive = False

    def update(self, input_velocity: ndarray, cave: ndarray, delta: float) -> None:
        """
        Moves the player according to the input velocity then collide with the tiles of the cave.
        If any collision occurs, the player is moved to the appropriate position, and its velocity is updated
        accordingly.

        :param input_velocity: velocity inputted by user
        :param cave: world tile grid
        :param delta: delta between two frames
        """
        if not self._alive:
            return None

        neighbor_tiles: ndarray = self._get_neighbor_tiles(cave)

        position: ndarray = deepcopy(self._position)
        rect: Rect = deepcopy(self._rect)
        velocity: ndarray = deepcopy(self._velocity)

        velocity += GRAVITY + input_velocity * delta
        velocity = clamp_vec(velocity, PLAYER_MAX_V)

        # x movement executes first
        position[0] += velocity[0]
        rect.x = round(position[0])

        # x collision and correction
        for _, tile in ndenumerate(neighbor_tiles):
            tile: Tile
            if tile and rect.colliderect(tile.rect):

                # tile can propulse player in opposite direction
                obstacle_impulse: float = tile.collided_with_player(float(velocity[0]))

                # collision correction
                if velocity[0] > 0:
                    rect.right = tile.rect.left
                    position[0] = rect.x
                    velocity[0] = obstacle_impulse
                    break
                if velocity[0] < 0:
                    rect.left = tile.rect.right
                    position[0] = rect.x
                    velocity[0] = obstacle_impulse
                    break

        # y movement executes second
        position[1] += velocity[1]
        rect.y = round(position[1])

        self._on_ground: bool = False

        # y collisions and correction
        for _, tile in ndenumerate(neighbor_tiles):
            tile: Tile
            if tile:

                # checking this because colliderect doesn't detect edge perfect collisions
                if rect.bottom == tile.rect.top:
                    self._on_ground = True

                if rect.colliderect(tile.rect):

                    # tile can propulse player in opposite direction
                    obstacle_impulse: float = tile.collided_with_player(float(velocity[1]))

                    # collision correction
                    if velocity[1] > 0:
                        rect.bottom = tile.rect.top
                        position[1] = rect.y
                        if obstacle_impulse:
                            velocity = array((velocity[0], obstacle_impulse))
                        else:
                            velocity = new_array()
                        self._on_ground = True
                        break
                    if velocity[1] < 0:
                        rect.top = tile.rect.bottom
                        position[1] = rect.y
                        velocity[1] = obstacle_impulse
                        break

        self._position = position
        self._rect = rect
        self._velocity = clamp_vec(velocity, PLAYER_MAX_V)

    def _get_neighbor_tiles(self, cave_map: ndarray) -> ndarray:
        """
        Returns player's neighbor tiles in a 3x3 region.

        :param cave_map: cave tile grid
        :return: neighbor tiles
        """
        player_idx: ndarray = world_to_grid(array(self._rect.center))
        if not idx_inside_grid(player_idx):
            raise ValueError("Player out of bounds")
        return moore_neighborhood(cave_map, player_idx)

    def display(self, screen: Surface, camera_offset: ndarray, time_elapsed: float) -> None:
        """
        Displays the player on the screen. The player is oriented towards the mouse.

        :param screen: main screen surface
        :param camera_offset: camera object
        :param time_elapsed: real time elapsed since start of the game
        """
        if not self._alive:
            return

        screen_pos: ndarray = world_to_screen(self._rect.topleft, camera_offset)

        # displaying ground sprite or jumping sprite
        if self._on_ground:
            sprite: Surface = animation_frame(PLAYER_GROUND_SPRITES, time_elapsed)
        else:
            sprite: Surface = PLAYER_SPRITE

        # flipping sprites depending on orientation (player always looks at the user mouse)
        if self._is_mouse_on_left(camera_offset):
            screen.blit(sprite, screen_pos)
        else:
            screen.blit(flip(sprite, True, False), screen_pos)

    def _is_mouse_on_left(self, camera_offset: ndarray):
        mouse_orientation: ndarray = around(self._rect.centerx + camera_offset[0]) - pygame.mouse.get_pos()[0]
        return mouse_orientation < 0
