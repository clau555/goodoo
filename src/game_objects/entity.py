from typing import Union

import pygame
from pygame.math import Vector2

from src.game_objects.bar import Bar
from src.game_objects.displayable import Displayable
from src.game_objects.projectile import Projectile
from src.game_objects.bonus import Bonus
from src.game_objects.collectable import Collectable
from src.game_objects.cursor import Cursor
from src.game_objects.tile import Tile
from src.game_objects.weapon import Weapon
from src.constants import GRAVITY_MAX, TILE_SCALE


class Entity(Displayable):
    """
    An entity is a displayable object which has physics.\n
    It is affected by gravity and collides with tiles.\n
    Its movements are determined by its input variables (left, right etc...).\n
    An entity can grab a weapon object and use it, and has health points.\n
    """

    MAX_HEALTH: int = 10
    HIT_DELAY: float = 100.

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], sprite: str = None,
                 velocity_max: tuple[int, int] = (TILE_SCALE // 10, TILE_SCALE // 3.5),
                 sprite_to_scale: bool = True) -> None:

        super().__init__(pos, size, sprite=sprite, sprite_to_scale=sprite_to_scale)

        self.__velocity_max: Vector2 = pygame.Vector2(velocity_max)
        self.__velocity: Vector2 = pygame.Vector2(0, 0)

        self.__direction: Vector2 = pygame.Vector2(0, 0)
        self.__angle: float = self.__direction.angle_to(Vector2(1, 0))

        self.__on_ground: bool = False

        self.__weapon: Union[Weapon, None] = None
        self.__coil: bool = False

        self.__health: int = self.MAX_HEALTH
        self.__hit: bool = False
        self.__hit_timer: float = self.HIT_DELAY

        self.__cooldown_bar: Bar = Bar((self.rect.centerx, self.rect.centery + self.rect.width), (255, 255, 255))
        self.__health_bar: Bar = Bar((self.rect.centerx, self.rect.centery - self.rect.width), (255, 0, 0))

        self.right: bool = False
        self.left: bool = False
        self.up: bool = False
        self.down: bool = False
        self.pick: bool = False
        self.action: bool = False

    @property
    def direction(self) -> Vector2:
        return self.__direction

    @property
    def weapon(self) -> Weapon:
        return self.__weapon

    @property
    def health(self) -> int:
        return self.__health

    def __weapon_update(self) -> None:
        """
        Updates the position and orientation of the wielded weapon.
        """

        if self.__direction.length() > 1:

            # weapon position update
            self.__weapon.rect.center = self.rect.center + self.__direction.normalize() * self.rect.width * (4 / 3)

            # direction and angle
            if self.__direction.x < 0:
                self.__weapon.rotate_sprite(self.__angle, True)
            elif self.__direction.x > 0:
                self.__weapon.rotate_sprite(self.__angle)

    def __bars_update(self):
        """
        Updates the position, orientation and state of the health bar and cooldown bar.
        """

        # cooldown bar
        self.__cooldown_bar.rect.center = (self.rect.centerx, self.rect.centery + self.rect.height)
        if self.__weapon:
            self.__cooldown_bar.progress = (pygame.time.get_ticks() - self.__weapon.counter) / 1000 \
                                           / self.__weapon.cooldown
        # health bar
        self.__health_bar.rect.center = (self.rect.centerx, self.rect.centery - self.rect.height)
        self.__health_bar.progress = self.__health / self.MAX_HEALTH

    def update(self, direction_pos: tuple[int, int], tiles: list[Tile],
               items: list[Collectable], projectiles: list[Projectile],
               cursor: Union[Cursor, None], delta_time: float) -> None:
        # FIXME entity falls off a tile too soon when it's near the right screen edge
        # FIXME weapon action is possible when target position is at the very center of the entity
        # TODO block weapon movement when direction_pos is on the entity?

        # y control movements
        if self.up and self.__on_ground:
            self.__velocity.y -= self.__velocity_max.y

        # gravity
        self.__velocity.y += 1 if self.__velocity.y <= GRAVITY_MAX else 0

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

            # weapon action is possible if the targeted position isn't near the weapon and the entity
            if not (self.rect.centerx < direction_pos[0] < self.__weapon.rect.centerx or
                    self.rect.centery < direction_pos[1] < self.__weapon.rect.centery) \
                    and not (self.rect.centerx > direction_pos[0] > self.__weapon.rect.centerx or
                             self.rect.centery > direction_pos[1] > self.__weapon.rect.centery) \
                    and self.__direction.length() > 0:

                # the weapon action is true if its cooldown is finished
                if self.action and self.__weapon.weapon_action(projectiles):
                    # recoil physic
                    recoil: Vector2 = -1 * self.__direction
                    recoil.scale_to_length(self.__weapon.recoil)
                    self.__velocity += recoil
                    self.__coil = True

                cursor.enable()

            # if the targeted position does not permit an action,
            # the cursor become "disabled"
            # TODO should be disabled when cooldown is running
            else:
                cursor.disable()

        # projectiles collision and effect
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect) and not self.__hit:
                self.__velocity += projectile.get_strength()
                self.__coil = True
                self.__health -= 1
                self.__hit = True
                projectile.alive = False

        if self.__hit:
            self.__hit_timer -= delta_time
            if self.__hit_timer <= 0:
                self.__hit = False

        # x axis movement execution
        self.rect.x += int(self.__velocity.x * delta_time)

        # x axis collisions
        for tile in tiles:
            if self.rect.colliderect(tile.rect):

                # right collision
                if self.__velocity.x > 0:
                    self.rect.right = tile.rect.left

                # left collision
                elif self.__velocity.x < 0:
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
                elif self.__velocity.y < 0:
                    self.rect.top = tile.rect.bottom

                # setting vertical velocity above zero
                # to avoid not colliding with the ground on
                # the next frame even if the entity is on it
                self.__velocity.y = 0.1

        if self.__weapon:
            # weapon position update
            self.__weapon_update()

        # bars update
        self.__bars_update()

        # item picking
        for item in items:
            if self.rect.colliderect(item.rect) and item.available and (self.pick or item.auto_grab):

                if type(item) is Weapon and item != self.__weapon:
                    item: Weapon  # converting item type to Weapon otherwise it's still considered as Collectable
                    self.__weapon = item  # the entity owns the weapon
                    item.weapon_update_counter()  # cooldown counter init

                elif type(item) is Bonus:
                    item: Bonus  # converting item type to Bonus otherwise it's still considered as Collectable
                    # adding health to the entity while not exceeding the maximum health
                    self.__health += item.value
                    self.__health = self.MAX_HEALTH if self.__health > self.MAX_HEALTH else self.__health

                item.available = False  # the item will be removed from the map

    def display(self) -> None:

        # sprite flipping depending on orientation
        if self.__direction.length() > 1:
            if self.__direction.x < 0:
                self.flip_sprite()
            elif self.__direction.x > 0:
                self.reset_sprite()

        # blinks when hit
        if not (self.__hit and self.__hit_timer % 10 < 5):
            super(Entity, self).display()

        # owned weapon and cooldown display
        if self.__weapon:
            self.__weapon.display()
            self.__cooldown_bar.display()

        self.__health_bar.display()
