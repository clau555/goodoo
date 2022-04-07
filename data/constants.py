from typing import Tuple, List

from pygame.math import Vector2

RESOLUTIONS: List[Tuple[int, int]] = [(1920, 1080), (1280, 720), (960, 540)]
SCREEN_SIZE: Tuple[int, int] = RESOLUTIONS[2]

WORLD_WIDTH: int = 32       # world width in tiles number
WORLD_HEIGHT: int = 18      # world height in tiles number

FPS: int = 60

TILE_EDGE: int = SCREEN_SIZE[0] // WORLD_WIDTH    # tile edge length in pixels
TILE_SIZE: Tuple[int, int] = (TILE_EDGE, TILE_EDGE)
TILE_COLOR: Tuple[int, int, int] = (60, 60, 60)

GROUND_SIZE: Tuple[int, int] = (TILE_EDGE, TILE_EDGE // 10)
GROUND_COLOR: Tuple[int, int, int] = (100, 100, 100)

PLAYER_EDGE: int = 2 * TILE_EDGE // 3    # player edge length in pixels
PLAYER_SIZE: Tuple[int, int] = (PLAYER_EDGE, PLAYER_EDGE)
PLAYER_MAX_V: float = TILE_EDGE - 0.1
PLAYER_SPRITE: str = "resources/sprites/player.png"

GRAVITY: Vector2 = Vector2(0, PLAYER_MAX_V / 75)    # gravity acceleration in pixels

BEAM_STRENGTH: float = PLAYER_MAX_V / 5             # beam impulse velocity length
BEAM_DURATION: float = 0.2                          # beam duration in seconds
BEAM_DECREASE: float = 1 / (BEAM_DURATION * FPS)    # beam deterioration at each frame in percentage

WHITE: Tuple[int, int, int] = (250, 250, 250)
BLACK: Tuple[int, int, int] = (0, 0, 0)
BLUE: Tuple[int, int, int] = (0, 0, 250)
RED: Tuple[int, int, int] = (250, 0, 0)
