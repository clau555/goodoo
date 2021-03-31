import pygame
from pygame.rect import Rect
from pygame.surface import Surface


class Displayable:

    def __init__(self, pos: tuple[int, int], size: tuple[int, int],
                 sprite: str = None, color: tuple[int, int, int] = (255, 0, 0)) -> None:
        self.rect: Rect = pygame.Rect(pos, size)
        self.sprite: Surface = pygame.transform.scale(pygame.image.load(sprite), size) if sprite else None
        self.color: tuple[int, int, int] = color

    def display(self) -> None:
        screen = pygame.display.get_surface()
        if self.sprite:
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, self.color, self.rect)
