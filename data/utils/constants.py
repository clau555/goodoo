from typing import List

from numpy import array, ndarray
from pygame import Surface, Rect
from pygame.image import load
from pygame.transform import scale

# screen
ICON: Surface = load("resources/icon.png")
SCREEN_SIZE: ndarray = array((384, 216))
SCREEN_RECT: Rect = Rect(0, 0, *SCREEN_SIZE)

# tile
TILE_EDGE: int = 12  # tile edge size in pixels
TILE_SIZE: ndarray = array((TILE_EDGE, TILE_EDGE))
TILE_IMG: Surface = load("resources/sprites/tile.png")
TILE_SPRITE: Surface = scale(TILE_IMG, TILE_SIZE)

# world grid
GRID_SIZE: ndarray = array((32, 512))  # world size in tiles
GRID_WIDTH: int = GRID_SIZE[0]
GRID_HEIGHT: int = GRID_SIZE[1]
WORLD_RIGHT: int = GRID_WIDTH * TILE_EDGE
WORLD_BOTTOM: int = GRID_HEIGHT * TILE_EDGE

# grid generation
NOISE_DENSITY: float = 0.48  # wall density during noise generation
AUTOMATON_ITERATION: int = 4  # number of automaton steps during generation
PLAYER_SPAWN_HEIGHT: int = GRID_HEIGHT - 3

# screen dimension in terms of tiles
SCREEN_GRID_SIZE: ndarray = array((SCREEN_SIZE[0] // TILE_EDGE, SCREEN_SIZE[1] // TILE_EDGE))

# goal tile
GOAL_SIZE: ndarray = array((10, 10))
GOAL_IMAGES: List[Surface] = [
    load("resources/sprites/goal_1.png"),
    load("resources/sprites/goal_2.png"),
    load("resources/sprites/goal_3.png"),
]
GOAL_SPRITES: List[Surface] = list(
    map(lambda img: scale(img, GOAL_SIZE), GOAL_IMAGES)
)

# player
PLAYER_SIZE: ndarray = array((8, 8))
PLAYER_IMG: Surface = load("resources/sprites/player_1.png")
PLAYER_SPRITE: Surface = scale(PLAYER_IMG, PLAYER_SIZE)
PLAYER_MAX_V: int = TILE_EDGE - TILE_EDGE // 6

# cursor
CURSOR_SIZE: ndarray = array((6, 6))
CURSOR_IMG: Surface = load("resources/sprites/cursor.png")
CURSOR_SPRITE: Surface = scale(CURSOR_IMG, CURSOR_SIZE)

# physics
FPS: int = 60
GRAVITY: ndarray = array((0, PLAYER_MAX_V / 75))
ANIMATION_SPEED: float = 0.1
CAMERA_SPEED: float = 0.08
SHAKE_AMPLITUDE: int = 50

# beam
BEAM_DURATION: float = 0.3  # beam duration in seconds
BEAM_DECREASE: float = 1 / (BEAM_DURATION * FPS)
BEAM_VECTOR_STEP: float = TILE_EDGE / 3
BEAM_INIT_STRENGTH: float = TILE_EDGE / 10  # beam impulse velocity length
BEAM_MAX_STRENGTH: float = TILE_EDGE / 4

# bonus
BONUS_SIZE: ndarray = array((4, 4))
BONUS_IMG: Surface = load("resources/sprites/bonus.png")
BONUS_SPRITE: Surface = scale(BONUS_IMG, BONUS_SIZE)
BONUS_REPARTITION: int = GRID_HEIGHT // 10  # height space between bonuses
BONUS_STRENGTH: float = TILE_EDGE / 20  # bonus in beam strength given by bonus

# lava
LAVA_IMAGES: List[Surface] = [load("resources/sprites/lava.png")]
LAVA_SPRITES: List[Surface] = list(
    map(lambda img: scale(img, TILE_SIZE), LAVA_IMAGES)
)
LAVA_INIT_SPEED: float = TILE_EDGE / 10
LAVA_TRIGGER_HEIGHT: int = GRID_HEIGHT - BONUS_REPARTITION - 5
LAVA_WARNING_DURATION: int = 150  # number of frames the screen must shake when triggering lava

# background
BACKGROUND_IMG: Surface = load("resources/sprites/background.png")
BACKGROUND_SPRITE: Surface = scale(BACKGROUND_IMG, SCREEN_SIZE)
BACKGROUND_LAVA_IMG: Surface = load("resources/sprites/background_lava.png")
BACKGROUND_LAVA_SPRITE: Surface = scale(BACKGROUND_LAVA_IMG, SCREEN_SIZE)
BACKGROUND_LAVA_DISTANCE: int = SCREEN_SIZE[1] * 2
