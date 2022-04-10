from typing import Tuple, List

import pygame.image
from pygame import Surface
from pygame.math import Vector2

from data.utils.screen import vec_to_screen, SCREEN_SIZE

TILE_IMG: Surface = pygame.image.load("resources/sprites/tile.png")
TILE_SIZE: Vector2 = Vector2(12)
TILE_SPRITE_SIZE: Vector2 = Vector2(14)
TILE_SPRITE: Surface = pygame.transform.scale(
    TILE_IMG, vec_to_screen(TILE_SPRITE_SIZE)
)
TILE_EDGE = vec_to_screen(TILE_SIZE)[0]  # screen length of a tile rect

GROUND_IMG: Surface = pygame.image.load("resources/sprites/ground.png")
GROUND_SPRITE_SIZE: Vector2 = Vector2(16)
GROUND_SPRITE: Surface = pygame.transform.scale(
    GROUND_IMG, vec_to_screen(GROUND_SPRITE_SIZE)
)

PILLAR_TOP_IMG: Surface = pygame.image.load("resources/sprites/pillar_top.png")
PILLAR_TOP_SPRITE_SIZE: Vector2 = Vector2(16)
PILLAR_TOP_SPRITE: Surface = pygame.transform.scale(
    PILLAR_TOP_IMG, vec_to_screen(PILLAR_TOP_SPRITE_SIZE)
)

PILLAR_IMG: Surface = pygame.image.load("resources/sprites/pillar.png")
PILLAR_SPRITE_SIZE: Vector2 = Vector2(12)
PILLAR_SPRITE: Surface = pygame.transform.scale(
    PILLAR_IMG, vec_to_screen(PILLAR_SPRITE_SIZE)
)

GOAL_IMAGES: List[Surface] = [
    pygame.image.load("resources/sprites/goal_1.png"),
    pygame.image.load("resources/sprites/goal_2.png"),
    pygame.image.load("resources/sprites/goal_3.png"),
]
GOAL_SIZE: Vector2 = Vector2(10)
GOAL_SPRITES: List[Surface] = list(map(
    lambda img: pygame.transform.scale(img, vec_to_screen(GOAL_SIZE)),
    GOAL_IMAGES
))

PLAYER_IMG: Surface = pygame.image.load("resources/sprites/player.png")
PLAYER_SIZE: Vector2 = Vector2(8)
PLAYER_SPRITE: Surface = pygame.transform.scale(
    PLAYER_IMG, vec_to_screen(PLAYER_SIZE)
)
PLAYER_MAX_V: int = TILE_SIZE.x - 1

FPS: int = 60
GRAVITY: Vector2 = Vector2(0, PLAYER_MAX_V / 75)

BEAM_STRENGTH: float = PLAYER_MAX_V / 4  # beam impulse velocity length
BEAM_DURATION: float = 0.3  # beam duration in seconds
BEAM_DECREASE: float = 1 / (BEAM_DURATION * FPS)
BEAM_VECTOR_STEP: float = TILE_SIZE.x / 4

CURSOR_SPRITE: Surface = pygame.image.load("resources/sprites/cursor.png")
CURSOR_SIZE: Tuple[int, int] = CURSOR_SPRITE.get_size()  # cursor size on screen

WHITE: Tuple[int, int, int] = (255, 255, 255)
BLACK: Tuple[int, int, int] = (0, 0, 0)
GREY: Tuple[int, int, int] = (128, 128, 128)
BLUE: Tuple[int, int, int] = (0, 0, 255)
RED: Tuple[int, int, int] = (250, 0, 0)
