from typing import Union

import pygame
from pygame.rect import Rect
from pygame.surface import Surface


class Displayable:
    """
    A displayable object stores the informations
    needed to be displayed on a pygame surface.\n
    """

    def __init__(self, pos: tuple[int, int], size: tuple[int, int],
                 color: tuple[int, int, int] = (255, 0, 0),
                 sprite: str = None, sprite_to_scale: bool = True) -> None:

        self.rect: Rect = pygame.Rect(pos, size)
        self.__color: tuple[int, int, int] = color
        self.__display: bool = True

        self.__sprite: Union[Surface, None] = None
        if sprite:
            if sprite_to_scale:
                self.__sprite = pygame.transform.scale(pygame.image.load(sprite), size)
            else:
                self.__sprite = pygame.image.load(sprite)
        self.__original_sprite: Union[Surface, None] = self.__sprite

    def get_color(self) -> tuple[int, int, int]:
        return self.__color

    def reset_sprite(self) -> None:
        self.__sprite = self.__original_sprite

    def flip_sprite(self) -> None:
        self.__sprite = pygame.transform.flip(self.__original_sprite, True, False)

    def set_display(self, display: bool) -> None:
        self.__display = display

    def rotate_sprite(self, angle: float, flipped: bool = False) -> None:
        if flipped:
            self.__sprite = pygame.transform.flip(self.__original_sprite, True, False)
            self.__sprite = pygame.transform.rotate(self.__sprite, angle - 180)
        else:
            self.__sprite = pygame.transform.rotate(self.__original_sprite, angle)

    def display(self) -> None:
        if self.__display:
            screen = pygame.display.get_surface()
            if self.__sprite:
                screen.blit(self.__sprite, (self.rect.x, self.rect.y))
            else:
                pygame.draw.rect(screen, self.__color, self.rect)
