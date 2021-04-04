import copy
from typing import Union

import pygame
from pygame.math import Vector2

from bar import Bar
from constants import GRAVITY, TILE_SCALE
from displayable import Displayable
from projectile import Projectile
from tile import Tile
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
        self.__on_ground: bool = False

        self.__weapon: Union[Weapon, None] = None
        self.__coil: bool = False

        self.__cooldown_bar: Bar = Bar((self.rect.x, self.rect.y))

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

    def get_weapon(self) -> Weapon:
        return self.__weapon

    def update(self, direction_pos: tuple[int, int], tiles: list[Tile],
               weapons: list[Weapon], projectiles: list[Projectile], delta_time: float) -> None:
        # FIXME entity falls off a tile too soon when it's near the right screen edge
        # TODO projectile collision

        self.__velocity.xy = (0, 0) if not self.__has_gravity else self.__velocity.xy

        # y control movements
        if self.__has_gravity:
            if self.up and self.__on_ground:
                self.__velocity.y -= self.__velocity_max.y * TILE_SCALE / 12
        else:
            if self.up and not self.down:
                self.__velocity.y -= self.__velocity_max.y
            elif self.down and not self.up:
                self.__velocity.y += self.__velocity_max.y

        # gravity
        if self.__has_gravity:
            self.__velocity.y += 1 if self.__velocity.y <= GRAVITY else 0

        # friction
        if -1 < self.__velocity.x < 1:
            self.__velocity.x = 0
            self.__coil = False
        elif self.__velocity.x > 0:
            self.__velocity.x -= 1
        elif self.__velocity.x < 0:
            self.__velocity.x += 1

        # x control movements (overrides friction)
        if not self.__coil:
            if self.left and not self.right:
                self.__velocity.x = -self.__velocity_max.x
            elif self.right and not self.left:
                self.__velocity.x = self.__velocity_max.x

        # direction and angle
        self.__direction = (Vector2(direction_pos) - self.rect.center)
        self.__angle = self.__direction.angle_to(Vector2(1, 0))

        # owned weapon action
        if self.__weapon:
            if self.action \
                    and not(self.rect.centerx <= direction_pos[0] <= self.__weapon.rect.centerx or
                            self.rect.centery <= direction_pos[1] <= self.__weapon. rect.centery) \
                    and not (self.rect.centerx >= direction_pos[0] >= self.__weapon.rect.centerx or
                             self.rect.centery >= direction_pos[1] >= self.__weapon.rect.centery):
                if self.__weapon.action(projectiles):
                    # if cooldown is finished
                    # recoil physic
                    recoil: Vector2 = copy.deepcopy(-1 * self.__direction)
                    recoil.scale_to_length(self.__weapon.get_recoil())
                    self.__velocity += recoil
                    self.__coil = True

        # x axis movement execution
        self.rect.x += int(self.__velocity.x * delta_time)

        # x axis collisions
        for tile in tiles:
            if self.rect.colliderect(tile.rect):

                # right collision
                if self.__velocity.x > 0:
                    self.rect.right = tile.rect.left

                # left collision
                if self.__velocity.x < 0:
                    self.rect.left = tile.rect.right

                self.__velocity.x = 0

        # y axis movement execution
        self.rect.y += int(self.__velocity.y * delta_time)

        self.__on_ground = False

        # y axis collisions
        for tile in tiles:
            if self.rect.colliderect(tile.rect):

                # bottom collision
                if self.__velocity.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.__on_ground = True

                # top collision
                if self.__velocity.y < 0:
                    self.rect.top = tile.rect.bottom

                self.__velocity.y = 0

        if self.__weapon:
            # weapon position update
            self.__weapon_update()

        # cooldown bar update
        self.__bar_update()

        # item grabbing
        for weapon in weapons:
            if self.rect.colliderect(weapon.rect) and weapon.is_available() and weapon != self.__weapon and self.pick:
                self.__weapon = weapon
                weapon.set_available(False)
                weapon.update_counter()  # cooldown counter init

    def __weapon_update(self) -> None:
        if self.__direction.length() > 1:
            self.__weapon.rect.center = self.rect.center + self.__direction.normalize() * self.rect.width * (4 / 3)

            # direction and angle
            if self.__direction.x < 0:
                self.__weapon.rotate_sprite(self.__angle, True)
            elif self.__direction.x > 0:
                self.__weapon.rotate_sprite(self.__angle)

    def __bar_update(self):
        self.__cooldown_bar.rect.center = (self.rect.centerx, self.rect.centery + self.rect.height)
        if self.__weapon:
            self.__cooldown_bar.set_progress((pygame.time.get_ticks() - self.__weapon.get_cooldown_counter()) / 1000
                                             / self.__weapon.get_cooldown())

    def display(self) -> None:

        if self.__direction.length() > 1:
            if self.__direction.x < 0:
                self.flip_sprite()
            elif self.__direction.x > 0:
                self.reset_sprite()

        super(Entity, self).display()

        if self.__weapon:
            self.__weapon.display()
            self.__cooldown_bar.display()
