import sys
import time

import pygame

from config import SCREEN_HEIGHT, SCREEN_WIDTH, FPS
from game import Game


def main(level_file_name: str = None) -> None:
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Impulsive Goo")

    game = Game(level_file_name)

    last_time = time.time()

    while True:

        delta_time = time.time() - last_time
        delta_time *= FPS
        last_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game.update_and_display(delta_time)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        sys.exit("not enough arguments")
