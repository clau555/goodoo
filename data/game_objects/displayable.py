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

        self.__rect: Rect = pygame.Rect(pos, size)
        self.__color: tuple[int, int, int] = color
        self.__visible: bool = True

        self.__sprite_to_scale: bool = sprite_to_scale

        self.__sprite: Union[Surface, None] = None
        self.__original_sprite: Union[Surface, None] = None
        if sprite:
            self.set_sprite(sprite)

    @property
    def rect(self) -> Rect:
        return self.__rect

    @property
    def color(self) -> tuple[int, int, int]:
        return self.__color

    @property
    def visible(self) -> bool:
        return self.__visible

    @visible.setter
    def visible(self, visible: bool) -> None:
        self.__visible = visible

    def set_sprite(self, sprite: str) -> None:
        if self.__sprite_to_scale:
            self.__sprite = pygame.transform.scale(pygame.image.load(sprite), self.__rect.size)
        else:
            self.__sprite = pygame.image.load(sprite)
        self.__original_sprite = self.__sprite

    def reset_sprite(self) -> None:
        self.__sprite = self.__original_sprite

    def flip_sprite(self) -> None:
        self.__sprite = pygame.transform.flip(self.__original_sprite, True, False)

    def rotate_sprite(self, angle: float, original_rect: rect, flipped: bool = False) -> None:
        if flipped:
            self.flip_sprite()
            self.__sprite = pygame.transform.rotate(self.__sprite, angle - 180.)
        else:
            self.__sprite = pygame.transform.rotate(self.__original_sprite, angle)

        # rotating a sprite changes its rectangle in size, so its position is changed too.
        # we correct this by replacing the new rectangle to its original position.
        self.__rect = self.__sprite.get_rect()
        self.__rect.center = original_rect.center

    def display(self) -> None:
        if self.__visible:
            screen = pygame.display.get_surface()
            if self.__sprite:
                screen.blit(self.__sprite, (self.rect.x, self.rect.y))
            else:
                pygame.draw.rect(screen, self.__color, self.rect)
