from typing import Tuple, List

import pygame.image
from numpy import array, ndarray
from pygame import Surface

from data.utils.math import tupint
from data.utils.screen import world_to_screen

TILE_IMG: Surface = pygame.image.load("resources/sprites/tile.png")
TILE_SIZE: ndarray = array((12, 12))
TILE_SPRITE_SIZE: ndarray = array((14, 14))
TILE_SPRITE: Surface = pygame.transform.scale(TILE_IMG, tupint(world_to_screen(TILE_SPRITE_SIZE)))
TILE_EDGE: int = world_to_screen(TILE_SIZE)[0]  # screen length of a tile rect

GROUND_IMG: Surface = pygame.image.load("resources/sprites/ground.png")
GROUND_SPRITE_SIZE: ndarray = array((16, 16))
GROUND_SPRITE: Surface = pygame.transform.scale(GROUND_IMG, tupint(world_to_screen(GROUND_SPRITE_SIZE)))

PILLAR_TOP_IMG: Surface = pygame.image.load("resources/sprites/pillar_top.png")
PILLAR_TOP_SPRITE_SIZE: ndarray = array((16, 16))
PILLAR_TOP_SPRITE: Surface = pygame.transform.scale(PILLAR_TOP_IMG, tupint(world_to_screen(PILLAR_TOP_SPRITE_SIZE)))

PILLAR_IMG: Surface = pygame.image.load("resources/sprites/pillar.png")
PILLAR_SPRITE_SIZE: ndarray = array((12, 12))
PILLAR_SPRITE: Surface = pygame.transform.scale(PILLAR_IMG, tupint(world_to_screen(PILLAR_SPRITE_SIZE)))

GOAL_IMAGES: List[Surface] = [
    pygame.image.load("resources/sprites/goal_1.png"),
    pygame.image.load("resources/sprites/goal_2.png"),
    pygame.image.load("resources/sprites/goal_3.png"),
]
GOAL_SIZE: ndarray = array((10, 10))
GOAL_SPRITES: List[Surface] = list(map(
    lambda img: pygame.transform.scale(img, tupint(world_to_screen(GOAL_SIZE))),
    GOAL_IMAGES
))

PLAYER_IMG: Surface = pygame.image.load("resources/sprites/player.png")
PLAYER_SIZE: ndarray = array((8, 8))
PLAYER_SPRITE: Surface = pygame.transform.scale(PLAYER_IMG, tupint(world_to_screen(PLAYER_SIZE)))
PLAYER_MAX_V: int = TILE_SIZE[0] - 1

FPS: int = 60
GRAVITY: ndarray = array((0, PLAYER_MAX_V / 75))

BEAM_STRENGTH: float = PLAYER_MAX_V / 4  # beam impulse velocity length
BEAM_DURATION: float = 0.3  # beam duration in seconds
BEAM_DECREASE: float = 1 / (BEAM_DURATION * FPS)
BEAM_VECTOR_STEP: float = TILE_SIZE[0] / 4

CURSOR_SPRITE: Surface = pygame.transform.scale(
    pygame.image.load("resources/sprites/cursor.png"), tupint(world_to_screen(PLAYER_SIZE))
)
CURSOR_SIZE: ndarray = array(CURSOR_SPRITE.get_size())

color = Tuple[int, int, int]
WHITE: color = (255, 255, 255)
BLACK: color = (0, 0, 0)
GREY: color = (128, 128, 128)
BLUE: color = (0, 0, 255)
RED: color = (250, 0, 0)
