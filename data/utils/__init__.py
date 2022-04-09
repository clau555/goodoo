from typing import Tuple

import pygame.image
from pygame import Surface
from pygame.math import Vector2

from data.utils.screen import vec_to_screen, SCREEN_SIZE

TILE_IMG: Surface = pygame.image.load("resources/sprites/tile.png")
TILE_SIZE: Vector2 = Vector2(12)
TILE_SPRITE: Surface = pygame.transform.scale(
    TILE_IMG, vec_to_screen(TILE_SIZE)
)
TILE_EDGE = vec_to_screen(TILE_SIZE)[0]

GROUND_IMG: Surface = pygame.image.load("resources/sprites/ground.png")
GROUND_SIZE: Vector2 = Vector2(16)
GROUND_SPRITE: Surface = pygame.transform.scale(
    GROUND_IMG, vec_to_screen(GROUND_SIZE)
)

GOAL_IMG: Surface = pygame.image.load("resources/sprites/test.png")
GOAL_SIZE: Vector2 = Vector2(10)
GOAL_SPRITE: Surface = pygame.transform.scale(
    GOAL_IMG, vec_to_screen(GOAL_SIZE)
)

PLAYER_IMG: Surface = pygame.image.load("resources/sprites/player.png")
PLAYER_SIZE: Vector2 = Vector2(8)
PLAYER_SPRITE: Surface = pygame.transform.scale(
    PLAYER_IMG, vec_to_screen(PLAYER_SIZE)
)
PLAYER_MAX_V: int = TILE_SIZE.x - 1

FPS: int = 60
GRAVITY: Vector2 = Vector2(0, PLAYER_MAX_V / 75)

BEAM_STRENGTH: float = PLAYER_MAX_V / 5  # beam impulse velocity length
BEAM_DURATION: float = 0.2  # beam duration in seconds
BEAM_DECREASE: float = 1 / \
       (BEAM_DURATION * FPS)  # beam deterioration at each frame in percentage

BEAM_VECTOR_STEP: float = TILE_SIZE.x / 4
BEAM_MAX_VECTOR_STEP: int = int(
    Vector2(SCREEN_SIZE).length() / BEAM_VECTOR_STEP
)

CURSOR_SPRITE: Surface = pygame.image.load("resources/sprites/cursor.png")
CURSOR_SIZE: Tuple[int, int] = CURSOR_SPRITE.get_size()  # cursor size on screen

WHITE: Tuple[int, int, int] = (255, 255, 255)
BLACK: Tuple[int, int, int] = (0, 0, 0)
BLUE: Tuple[int, int, int] = (0, 0, 255)
RED: Tuple[int, int, int] = (250, 0, 0)
