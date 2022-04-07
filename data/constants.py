from typing import Tuple

SCREEN_WIDTH: int = 1920    # screen width in pixels
SCREEN_HEIGHT: int = 1080   # screen height in pixels
SCREEN_SIZE: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)

WORLD_WIDTH: int = 32       # world width in tiles number
WORLD_HEIGHT: int = 18      # world height in tiles number

FPS: int = 60

TILE_EDGE: int = SCREEN_WIDTH // WORLD_WIDTH    # tile edge length in pixels
TILE_SIZE: Tuple[int, int] = (TILE_EDGE, TILE_EDGE)
TILE_COLOR: Tuple[int, int, int] = (60, 60, 60)

GROUND_SIZE: Tuple[int, int] = (TILE_EDGE, TILE_EDGE // 10)
GROUND_COLOR: Tuple[int, int, int] = (100, 100, 100)

PLAYER_EDGE: int = 2 * TILE_EDGE // 3    # player edge length in pixels
PLAYER_SIZE: Tuple[int, int] = (PLAYER_EDGE, PLAYER_EDGE)
PLAYER_MAX_V: float = TILE_EDGE - 0.1
PLAYER_INPUT_VX: float = PLAYER_MAX_V / 10  # velocity when moving in x direction
PLAYER_INPUT_VY: float = PLAYER_MAX_V / 3.2   # velocity impulsion when jumping
PLAYER_SPRITE: str = "resources/sprites/player.png"

GRAVITY: float = PLAYER_MAX_V / 50    # gravity acceleration in pixels
FRICTION: float = PLAYER_MAX_V / 2    # x-axis friction acceleration in pixels

WHITE: Tuple[int, int, int] = (250, 250, 250)
BLUE: Tuple[int, int, int] = (0, 0, 250)
