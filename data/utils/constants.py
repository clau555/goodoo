from typing import List

import pygame.image
from numpy import array, ndarray
from pygame import Surface, Rect

# screen
# TODO render on 384x216 only
RESOLUTIONS: ndarray = array(((1920, 1080), (1280, 720), (960, 540), (384, 216)))
SCREEN_SIZE: ndarray = RESOLUTIONS[0]  # select resolution
SCREEN_RECT: Rect = Rect(0, 0, *SCREEN_SIZE)

# tile
TILE_EDGE: int = SCREEN_SIZE[0] // 32  # tile edge size in pixels
TILE_SIZE: ndarray = array((TILE_EDGE, TILE_EDGE))
TILE_IMG: Surface = pygame.image.load("resources/sprites/tile.png")
TILE_SPRITE: Surface = pygame.transform.scale(TILE_IMG, TILE_SIZE)

# world grid
GRID_SIZE: ndarray = array((32, 512))  # world size in tiles
GRID_WIDTH: int = GRID_SIZE[0]
GRID_HEIGHT: int = GRID_SIZE[1]
WORLD_RIGHT: int = GRID_WIDTH * TILE_EDGE
WORLD_BOTTOM: int = GRID_HEIGHT * TILE_EDGE

# grid generation
AUTOMATON_ITERATION: int = 4  # number of automaton steps during generation
NOISE_DENSITY: float = 0.48  # wall density during noise generation

# screen dimension in terms of tiles
SCREEN_GRID_SIZE: ndarray = array((SCREEN_SIZE[0] // TILE_EDGE, SCREEN_SIZE[1] // TILE_EDGE))

# goal tile
GOAL_SIZE: ndarray = TILE_SIZE
GOAL_IMAGES: List[Surface] = [
    pygame.image.load("resources/sprites/goal_1.png"),
    pygame.image.load("resources/sprites/goal_2.png"),
    pygame.image.load("resources/sprites/goal_3.png"),
]
GOAL_SPRITES: List[Surface] = list(
    map(lambda img: pygame.transform.scale(img, GOAL_SIZE), GOAL_IMAGES)
)

# player
PLAYER_SIZE: ndarray = TILE_SIZE * 3/4
PLAYER_IMG: Surface = pygame.image.load("resources/sprites/player.png")
PLAYER_SPRITE: Surface = pygame.transform.scale(PLAYER_IMG, PLAYER_SIZE)
PLAYER_MAX_V: int = TILE_EDGE - TILE_EDGE // 6

# cursor
CURSOR_SIZE: ndarray = TILE_SIZE * 3/4
CURSOR_IMG: Surface = pygame.image.load("resources/sprites/cursor.png")
CURSOR_SPRITE: Surface = pygame.transform.scale(CURSOR_IMG, CURSOR_SIZE)

# physics
FPS: int = 60
GRAVITY: ndarray = array((0, PLAYER_MAX_V / 75))
CAMERA_SPEED: float = 0.3
ANIMATION_SPEED: float = 0.1

# beam
BEAM_DURATION: float = 0.3  # beam duration in seconds
BEAM_DECREASE: float = 1 / (BEAM_DURATION * FPS)
BEAM_VECTOR_STEP: float = TILE_EDGE / 3
BEAM_INIT_STRENGTH: float = TILE_EDGE / 10  # beam impulse velocity length
BEAM_MAX_STRENGTH: float = TILE_EDGE / 4

# bonus
BONUS_SIZE: ndarray = TILE_SIZE / 2
BONUS_IMG: Surface = pygame.image.load("resources/sprites/bonus.png")
BONUS_SPRITE: Surface = pygame.transform.scale(BONUS_IMG, BONUS_SIZE)
BONUS_REPARTITION: int = GRID_HEIGHT // 10  # height space between bonuses
BONUS_STRENGTH: float = TILE_EDGE / 20  # bonus in beam strength given by bonus

# lava
LAVA_IMAGES: List[Surface] = [pygame.image.load("resources/sprites/lava.png")]
LAVA_SPRITES: List[Surface] = list(
    map(lambda img: pygame.transform.scale(img, TILE_SIZE), LAVA_IMAGES)
)
LAVA_INIT_SPEED: float = TILE_EDGE / 50

# background
BACKGROUND_IMG: Surface = pygame.image.load("resources/sprites/background.png")
BACKGROUND_SPRITE: Surface = pygame.transform.scale(BACKGROUND_IMG, SCREEN_SIZE)
BACKGROUND_LAVA_IMG: Surface = pygame.image.load("resources/sprites/background_lava.png")
BACKGROUND_LAVA_SPRITE: Surface = pygame.transform.scale(BACKGROUND_LAVA_IMG, SCREEN_SIZE)
BACKGROUND_LAVA_DISTANCE: float = SCREEN_SIZE[1] * 1.5
