import sys
import time

import pygame
from pygame.time import Clock

from src.game_objects.game import Game
from src.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS


def main(level_file_name: str = None) -> None:
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                            pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Impulsive Goo")
    pygame.mouse.set_visible(False)

    game: Game = Game(level_file_name)
    clock: Clock = pygame.time.Clock()
    last_time: float = time.time()

    while True:

        inputs: dict[str, bool] = {
            "left": False,
            "right": False,
            "up": False,
            "down": False,
            "action": False,
            "pick": False
        }

        # events
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                # user event inputs
                if event.key == pygame.K_z or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    inputs["up"] = True
                if event.key == pygame.K_r or event.key == pygame.K_LSHIFT:
                    inputs["pick"] = True

                # quit shortcut
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                # debug
                elif event.key == pygame.K_ASTERISK:
                    game.toggle_debug()

            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # user movement inputs
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_q] or keys[pygame.K_LEFT]) and not (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            inputs["left"] = True
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not (keys[pygame.K_q] or keys[pygame.K_LEFT]):
            inputs["right"] = True

        # left click detection
        if pygame.mouse.get_pressed(3)[0]:
            inputs["action"] = True

        # delta time update
        delta_time: float = (time.time() - last_time) * FPS
        last_time: float = time.time()

        # game update and display update
        if delta_time <= 2.:
            game.update_and_display(inputs, delta_time)
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        sys.exit("not enough arguments")
