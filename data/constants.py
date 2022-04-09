from typing import Tuple, List

import pygame.image
from pygame import Surface
from pygame.math import Vector2


RESOLUTIONS: List[Tuple[int, int]] = [(1920, 1080), (1280, 720), (960, 540)]
SCREEN_SIZE: Tuple[int, int] = RESOLUTIONS[2]
WORLD_SIZE: Tuple[int, int] = 384, 216  # world size in pixels
GRID_SIZE: Tuple[int, int] = 32, 18  # world size in tiles
GRID_WIDTH: int = GRID_SIZE[0]
GRID_HEIGHT: int = GRID_SIZE[1]
PIX_TO_SCREEN: float = SCREEN_SIZE[0] / WORLD_SIZE[0]


def vec_to_screen(pos: Vector2) -> Tuple[int, int]:
    return int(pos.x * PIX_TO_SCREEN), int(pos.y * PIX_TO_SCREEN)


def tuple_to_screen(pos: Tuple[int, int]) -> Tuple[int, int]:
    return int(pos[0] * PIX_TO_SCREEN), int(pos[1] * PIX_TO_SCREEN)


def tuple_to_pix(pos: Tuple[int, int]) -> Vector2:
    return Vector2(pos[0] / PIX_TO_SCREEN, pos[1] / PIX_TO_SCREEN)


TILE_IMG: Surface = pygame.image.load("resources/sprites/tile.png")
TILE_SIZE: Vector2 = Vector2(12)
TILE_SPRITE: Surface = pygame.transform.scale(
    TILE_IMG, vec_to_screen(TILE_SIZE)
)
TILE_EDGE = vec_to_screen(TILE_SIZE)[0]

GROUND_IMG: Surface = pygame.image.load("resources/sprites/ground.png")
GROUND_SPRITE: Surface = pygame.transform.scale(
    GROUND_IMG, vec_to_screen(TILE_SIZE)
)

GRASS_IMG: Surface = pygame.image.load("resources/sprites/grass.png")
GRASS_SIZE: Vector2 = Vector2(16)
GRASS_SPRITE: Surface = pygame.transform.scale(
    GRASS_IMG, vec_to_screen(GRASS_SIZE)
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
