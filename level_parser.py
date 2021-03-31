import sys

from PIL import Image

from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SCALE, WORLD_WIDTH, WORLD_HEIGHT
from player import Player
from tile import Tile


def pixel_comparison(pixel: tuple[int, int, int], color: tuple[int, int, int], margin: int = 30) -> bool:
    pixel_margin = (margin, margin, margin)
    return color[0] - pixel_margin[0] <= pixel[0] <= color[0] + pixel_margin[0] and \
           color[1] - pixel_margin[1] <= pixel[1] <= color[1] + pixel_margin[1] and \
           color[2] - pixel_margin[2] <= pixel[2] <= color[2] + pixel_margin[2]


def level_from_image(file_name: str) -> tuple[Player, list[list[Tile]]]:
    im: Image = Image.open(file_name).convert('RGB')

    if im.size[0] != WORLD_WIDTH or im.size[1] != WORLD_HEIGHT:
        sys.exit("level map file is at size {} instead of {}"
                 .format(im.size, (int(SCREEN_WIDTH / TILE_SCALE), int(SCREEN_HEIGHT / TILE_SCALE))))

    world: list[list[Tile]] = []
    player: Player = Player((0, 0))
    player_spawn = False

    for i in range(im.size[0]):
        line: list[Tile] = []
        for j in range(im.size[1]):
            current_pixel = im.getpixel((i, j))

            if pixel_comparison(current_pixel, (0, 0, 255)) and not player_spawn:
                player.rect.x = i * TILE_SCALE
                player.rect.y = j * TILE_SCALE
                player_spawn = True
            if pixel_comparison(current_pixel, (255, 255, 255)):
                line.append(Tile((i * TILE_SCALE, j * TILE_SCALE)))
            else:
                line.append(None)

        world.append(line)

    for i in range(len(world)):
        for j in range(len(world[i])):
            if world[i][j] is not None and j > 0 and world[i][j - 1] is None:
                world[i][j].is_at_top = True

    if not player_spawn:
        sys.exit("no player spawn point set inside the map")

    return player, world
