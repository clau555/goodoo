from typing import Union

import pygame
from pygame.rect import Rect
from pygame.surface import Surface


class Displayable:

    def __init__(self, pos: tuple[int, int], size: tuple[int, int],
                 color: tuple[int, int, int] = (255, 0, 0),
                 sprite: str = None, sprite_to_scale: bool = True) -> None:

        self.rect: Rect = pygame.Rect(pos, size)
        self.__color: tuple[int, int, int] = color

        self.sprite: Union[Surface, None] = None
        if sprite:
            if sprite_to_scale:
                self.sprite = pygame.transform.scale(pygame.image.load(sprite), size)
            else:
                self.sprite = pygame.image.load(sprite)
        self.__original_sprite: Union[Surface, None] = self.sprite

    def get_color(self):
        return self.__color

    def rotate(self, angle: float, flipped: bool = False) -> None:
        if flipped:
            self.sprite = pygame.transform.flip(self.__original_sprite, True, False)
            self.sprite = pygame.transform.rotate(self.sprite, angle - 180)
        else:
            self.sprite = pygame.transform.rotate(self.__original_sprite, angle)

    def display(self) -> None:
        screen = pygame.display.get_surface()
        if self.sprite:
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, self.__color, self.rect)
