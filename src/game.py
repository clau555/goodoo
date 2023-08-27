import sys
from threading import Timer
from typing import Sequence, Optional

import pygame
from numpy import ndarray, array, ndenumerate, zeros
from numpy.random import random_sample
from pygame.constants import K_ESCAPE, K_p, QUIT, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.event import post, Event
from pygame.surface import Surface

from src.display.background import Background
from src.display.camera import Camera
from src.display.jauge import display_jauge
from src.generation.generation import generate_world
from src.lava import Lava
from src.player.grapple import Grapple
from src.player.player import Player
from src.player.player_particle import PlayerParticle
from src.tile_particles.mushroom_particle import MushroomParticle
from src.tile_particles.tile_particle import TileParticle
from src.tiles.mushroom import Mushroom
from src.tiles.tile import Tile
from src.utils.constants import CURSOR_SPRITE, CURSOR_SIZE, OBSTACLE_PARTICLE_SPAWN_RATE, GAME_OVER_DURATION, \
    GRAY_LAYER, PAUSE_TEXT, SCREEN_SIZE, KEY_MAPS, LAVA_WARNING_DURATION, CAMERA_TARGET_OFFSET, PLAYER_INPUT_V, \
    PLAYER_PARTICLES_COLLISION_SPAWN_COUNT, PLAYER_PARTICLES_DEATH_SPAWN_COUNT, MUSHROOM_BUMP_PARTICLES_COUNT
from src.utils.events import MUSHROOM_BUMPED, PLAYER_DIES, PLAYER_WINS, LAVA_TRIGGERED
from src.utils.game_timer import GameTimer
from src.utils.utils import visible_grid, is_pressed, end_program


class Game:
    def __init__(self, keyboard_layout: str):
        self._keyboard_layout: str = keyboard_layout

        cave_map, decoration_map, player = generate_world()
        self._cave_map: ndarray = cave_map
        self._decoration_map: ndarray = decoration_map
        self._background_image: Background = Background()

        self._player: Player = player
        self._grapple: Grapple = Grapple()
        self._lava: Lava = Lava()

        self._camera: Camera = Camera(array(player.rect.center))
        self._screen: Surface = pygame.display.get_surface()

        self._tile_particles: list[TileParticle] = []
        self._player_particles: list[PlayerParticle] = []

        self._global_timer: GameTimer = GameTimer()
        self._over_timer: Timer = self._new_over_timer()
        self._warning_timer: Timer = Timer(LAVA_WARNING_DURATION, self._finish_game)
        self._is_running = True

    def run(self) -> None:
        while self._is_running:
            self._global_timer.update()
            self._update_from_events()
            self._update()
            self._display()

    def _finish_game(self) -> None:
        self._is_running = False

    # events -----------------------------------------------------------------------------------------------------------

    def _update_from_events(self) -> None:
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE and not self._over_timer.is_alive():
                    post(Event(PLAYER_DIES))
                elif event.key in KEY_MAPS[self._keyboard_layout]["pause"]:
                    _pause(self._screen)
                    self._global_timer.reset()

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                self._grapple.fire(self._cave_map, self._camera.offset)

            elif event.type == MOUSEBUTTONUP and event.button == 1:
                self._grapple.unfire()

            elif event.type == PLAYER_DIES or event.type == PLAYER_WINS:
                self._spawn_death_particles()
                self._player.kill()
                self._over_timer.start()

            elif event.type == MUSHROOM_BUMPED:
                self._spawn_mushroom_particles(event.dict["mushroom"])
                self._spawn_collision_particles()

            elif event.type == LAVA_TRIGGERED:
                self._background_image.start_warning()
                self._camera.start_shaking()

    def _new_over_timer(self) -> Timer:
        return Timer(GAME_OVER_DURATION, self._finish_game)

    def _restart_over_timer(self) -> None:
        self._over_timer.cancel()
        self._over_timer = self._new_over_timer()
        self._over_timer.start()

    def _spawn_death_particles(self) -> None:
        for _ in range(PLAYER_PARTICLES_DEATH_SPAWN_COUNT):
            self._spawn_player_particle()

    def _spawn_collision_particles(self) -> None:
        for _ in range(PLAYER_PARTICLES_COLLISION_SPAWN_COUNT):
            self._spawn_player_particle()

    def _spawn_player_particle(self) -> None:
        particle: PlayerParticle = PlayerParticle(self._player.world_position)
        self._player_particles.append(particle)

    def _spawn_mushroom_particles(self, mushroom: Mushroom) -> None:
        for _ in range(MUSHROOM_BUMP_PARTICLES_COUNT):
            position: ndarray = array(mushroom.rect.center) + (random_sample(2) - 0.5) * 20
            self._tile_particles.append(MushroomParticle(position))

    # update -----------------------------------------------------------------------------------------------------------

    def _update(self) -> None:
        delta: float = self._global_timer.delta

        input_velocity: ndarray = _key_input_velocity(self._grapple, self._keyboard_layout)
        input_velocity += self._grapple.acceleration

        self._update_tile_particles()
        self._update_player_particles(delta)

        camera_target: ndarray = self._player.rect.center + CAMERA_TARGET_OFFSET
        self._camera.update(camera_target, delta)

        self._lava.update(float(self._player.world_position[1]), delta)
        self._player.update(input_velocity, self._cave_map, delta)
        self._grapple.update(self._player.rect.center, delta)

        self._check_player_above_lava()
        self._check_win()

    def _update_tile_particles(self) -> None:
        for i, particle in enumerate(self._tile_particles):
            particle: TileParticle
            particle.update()
            if not particle.alive:
                index: int = self._tile_particles.index(particle)
                self._tile_particles.pop(index)

    def _update_player_particles(self, delta: float) -> None:
        for _, particle in enumerate(self._player_particles):
            particle: PlayerParticle
            particle.update(delta)
            if not particle.alive:
                index: int = self._player_particles.index(particle)
                self._player_particles.pop(index)

    def _check_player_above_lava(self) -> None:
        if self._player.rect.centery >= self._lava.y and not self._over_timer.is_alive():
            post(Event(PLAYER_DIES))

    def _check_win(self) -> None:
        if self._player.rect.centery <= 0 and not self._over_timer.is_alive():
            post(Event(PLAYER_WINS))

    # display ----------------------------------------------------------------------------------------------------------

    def _display(self) -> None:
        self._background_image.display(self._player.world_position, self._lava.y, self._camera.offset, self._screen)
        self._display_tile_maps(self._cave_map, self._decoration_map, self._screen, self._camera)

        self._grapple.display(self._player.alive, self._screen, self._camera.offset)
        self._player.display(self._screen, self._camera.offset, self._global_timer.time_elapsed)

        self._display_tile_particles()
        self._lava.display(self._screen, self._camera.offset, self._global_timer.time_elapsed)
        self._display_player_particles()

        display_jauge(self._player, self._lava, self._screen)
        self._display_cursor()

        pygame.display.flip()

    def _display_tile_maps(
            self,
            cave_map: ndarray,
            decoration_map: ndarray,
            screen: Surface,
            camera: Camera,
    ) -> None:
        """
        Displays the tiles of the tile_cave.
        When an obstacle is on screen, spawns its tile_particles randomly.

        :param cave_map: cave map data
        :param decoration_map: decoration map data
        :param camera: camera data
        :param screen: screen surface
        """
        visible_cave: ndarray = visible_grid(cave_map, camera.top_left)
        visible_decoration: ndarray = visible_grid(decoration_map, camera.top_left)

        # displaying all tile maps in one loop to reduce process time
        for (i, j), _ in ndenumerate(visible_cave):

            if visible_cave[i, j]:
                tile: Tile = visible_cave[i, j]
                self._spawn_random_tile_particle(tile)
                tile.display(screen, camera.offset)

            if visible_decoration[i, j]:
                tile: Tile = visible_decoration[i, j]
                tile.display(screen, camera.offset)

    def _spawn_random_tile_particle(self, tile: Tile) -> None:
        if random_sample() < OBSTACLE_PARTICLE_SPAWN_RATE:
            particle: Optional[TileParticle] = tile.create_particle(tile.rect.center)
            if particle is not None:
                self._tile_particles.append(particle)

    def _display_tile_particles(self) -> None:
        for i, particle in enumerate(self._tile_particles):
            particle: TileParticle
            particle.display(self._screen, self._camera.offset)

    def _display_player_particles(self) -> None:
        for _, particle in enumerate(self._player_particles):
            particle: PlayerParticle
            particle.display(self._screen, self._camera.offset)

    def _display_cursor(self) -> None:
        self._screen.blit(CURSOR_SPRITE, array(pygame.mouse.get_pos()) - CURSOR_SIZE / 2)


def _key_input_velocity(grapple: Grapple, keyboard_layout: str) -> ndarray:
    """
    Returns the velocity vector of the player according to the pressed keys.

    :param grapple: grapple object
    :param keyboard_layout: keyboard layout string
    :return: input velocity vector
    """
    keys: Sequence[bool] = pygame.key.get_pressed()
    input_velocity: ndarray = zeros(2).astype(float)

    if grapple.is_attached:
        if is_pressed("left", keys, keyboard_layout):
            input_velocity += array((-PLAYER_INPUT_V, 0))
        if is_pressed("right", keys, keyboard_layout):
            input_velocity += array((PLAYER_INPUT_V, 0))

    return input_velocity


def _pause(screen: Surface) -> None:
    """
    Pauses the game by blocking the main loop.
    Displays a pause screen and waits for the user to press the pause key again.
    Return the time at which the pause ends for delta time calculation.

    :param screen: main screen surface
    """
    screen.blit(GRAY_LAYER, (0, 0))

    x: int = SCREEN_SIZE[0] // 2 - PAUSE_TEXT.get_width() // 2
    y: int = SCREEN_SIZE[1] // 2 - PAUSE_TEXT.get_height() // 2
    screen.blit(PAUSE_TEXT, (x, y))

    pygame.display.flip()

    paused: bool = True
    while paused:
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    end_program()
                elif event.key == K_p:
                    paused = False

            elif event.type == pygame.QUIT:
                end_program()
