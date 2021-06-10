SCREEN_WIDTH: int = 1280  # screen width in pixels
SCREEN_HEIGHT: int = 720  # screen height in pixels
SCREEN_CENTER: tuple[int, int] = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # on-screen center position
WORLD_WIDTH: int = 32  # number of tile for the in-game world width
WORLD_HEIGHT: int = 18  # number of tiles for the in-game world height
TILE_SCALE: int = SCREEN_WIDTH // WORLD_WIDTH  # size of a tile in pixels
GRAVITY_MAX: int = TILE_SCALE // 3  # maximum gravitational velocity of an entity
FPS: int = 60  # frame per second
