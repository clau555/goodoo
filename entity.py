import math
from typing import Union

import pygame
from pygame.math import Vector2

from constants import GRAVITY, COLLISION_TOLERANCE, TILE_SCALE
from displayable import Displayable
from tile import Tile
from projectile import Projectile
from weapon import Weapon


class Entity(Displayable):

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], sprite: str = None,
                 velocity_max: tuple[int, int] = (int(TILE_SCALE * 0.075), int(TILE_SCALE * 0.075)),
                 has_gravity: bool = True, sprite_to_scale: bool = True) -> None:

        super().__init__(pos, size, sprite=sprite, sprite_to_scale=sprite_to_scale)

        self.__velocity_max: Vector2 = pygame.Vector2(velocity_max)
        self.__velocity: Vector2 = pygame.Vector2(0, 0)

        self.__direction: Vector2 = pygame.Vector2(0, 0)
        self.__angle: float = self.__direction.angle_to(Vector2(1, 0))

        self.__has_gravity: bool = has_gravity
        self.__is_on_ground: bool = False

        self.__weapon: Union[Weapon, None] = None

        self.right: bool = False
        self.left: bool = False
        self.up: bool = False
        self.down: bool = False
        self.pick: bool = False
        self.action: bool = False

    def get_direction(self) -> Vector2:
        return self.__direction

    def has_weapon(self) -> bool:
        return True if self.__weapon else False

    def update(self, direction_pos: tuple[int, int], tiles: list[Tile],
               weapons: list[Weapon], projectiles: list[Projectile], delta_time: float) -> None:
        # FIXME entity falls off a tile too soon when it's near the right screen edge

        self.__velocity.xy = (0, 0) if not self.__has_gravity else self.__velocity
        self.__velocity.x = 0

        # movements from controls

        if self.left and not self.right:
            self.__velocity.x = -self.__velocity_max.x
        elif self.right and not self.left:
            self.__velocity.x = self.__velocity_max.x

        if self.__has_gravity:
            if self.up and self.__is_on_ground:
                self.__velocity.y -= TILE_SCALE / 4
        else:
            if self.up and not self.down:
                self.__velocity.y = -self.__velocity_max.y
            elif self.down and not self.up:
                self.__velocity.y = self.__velocity_max.y

        # gravity
        if self.__has_gravity:
            self.__velocity.y += 1 if self.__velocity.y <= GRAVITY else 0

        # x axis movement execution
        self.rect.x += int(self.__velocity.x * delta_time)

        # x axis collisions
        for tile in tiles:
            if self.rect.colliderect(tile.rect):

                # right collision
                if abs(self.rect.right - tile.rect.left) < COLLISION_TOLERANCE:
                    self.rect.right = tile.rect.left
                    self.__velocity.x = 0

                # left collision
                if abs(self.rect.left - tile.rect.right) < COLLISION_TOLERANCE:
                    self.rect.left = tile.rect.right
                    self.__velocity.x = 0

        # y axis movement execution
        self.rect.y += int(self.__velocity.y * delta_time)

        self.__is_on_ground = False

        # y axis collisions
        for tile in tiles:
            if self.rect.colliderect(tile.rect):

                # bottom collision
                if abs(self.rect.bottom - tile.rect.top) < COLLISION_TOLERANCE:
                    self.rect.bottom = tile.rect.top
                    self.__velocity.y = 0
                    self.__is_on_ground = True

                # top collision
                if abs(self.rect.top - tile.rect.bottom) < COLLISION_TOLERANCE:
                    self.rect.top = tile.rect.bottom
                    self.__velocity.y = 0

        # direction and angle
        self.__direction = (Vector2(direction_pos) - self.rect.center)
        self.__angle = self.__direction.angle_to(Vector2(1, 0))

        # item grabbing
        for weapon in weapons:
            if self.rect.colliderect(weapon.rect) and weapon.is_available and weapon != self.__weapon and self.pick:
                self.__weapon = weapon
                weapon.is_available = False

        # owned weapon update
        if self.__weapon:
            self.__weapon_update()
            if self.action:
                self.__weapon.action(self.__angle, projectiles)

    def __weapon_update(self) -> None:
        if self.__direction.length() > 1:
            offset: Vector2 = Vector2(self.rect.width * (4 / 3) * math.cos(math.radians(self.__angle)),
                                      -self.rect.width * (4 / 3) * math.sin(math.radians(self.__angle)))
            self.__weapon.rect.center = self.rect.center + offset

            # direction and angle
            if self.__direction.x < 0:
                self.__weapon.rotate_sprite(self.__angle, True)
            elif self.__direction.x > 0:
                self.__weapon.rotate_sprite(self.__angle)

    def display(self) -> None:

        if self.__direction.x < 0:
            self.flip_sprite()
        elif self.__direction.x > 0:
            self.reset_sprite()

        super(Entity, self).display()

        if self.__weapon:
            self.__weapon.display()
