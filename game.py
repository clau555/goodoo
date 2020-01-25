# -*- coding : utf-8 -*-

import pygame
import random

from gl0bals import *
from classes.screen import *
from classes.block import *
from classes.entity import *
from classes.player import *
from classes.enemy1 import *
from classes.enemy2 import *
from classes.enemy3 import *
from classes.weapon import *
from classes.projectile import *
from classes.mist import *
from classes.level1 import *
from classes.level2 import *
from classes.level3 import *
from classes.level4 import *
from classes.level5 import *
from classes.level6 import *

# ==================================================================================================================================

class Game:

	def __init__(self):

		# niveau
		if Globals.level == 1:
			self.level = Level1()
		elif Globals.level == 2:
			self.level = Level2()
		elif Globals.level == 3:
			self.level = Level3()
		elif Globals.level == 4:
			self.level = Level4()
		elif Globals.level == 5:
			self.level = Level5()
		elif Globals.level == 6:
			self.level = Level6()

		self.TAB = self.level.TAB # tableau de 1 et 0 du niveau
		self.player = self.level.player # initialisation du joueur
		self.weapon = self.level.weapon # initialisation de l'arme

		# création des blocs du niveau
		for i in range(0,len(self.TAB)):
			for j in range(0,len(self.TAB[0])):
				if self.TAB[i][j]==1:
					# est ajouté à la liste de tout les blocs
					Globals.blocks.append( Block( (j * Globals.RATIO , i * Globals.RATIO) ) )

		# horloge
		Globals.counter = 0
		self.clock = pygame.time.Clock()

		# jeu
		self.over = False
		self.victory = False
		self.wave = 0

# ==================================================================================================================================

	def body(self, screen):

		# INITIALISATION
		pygame.init()
		player = self.level.player
		weapon = self.level.weapon

		# EVENTS
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Globals.launched = False

		keys = pygame.key.get_pressed()

		# FENETRE
		screen.update(keys)

		# VAGUES
		for i in range(0, len(self.level.waves)):
			# début de la transition
			if self.wave == i and Globals.enemies == []:
				Globals.transition_counter -= 1
				weapon = None
				player.weaponized = False
				# brouillard indicateur des positions ennemies
				if Globals.transition_counter == Globals.TRANSITION -1:
					self.level.pre_waves[i](self.level)
				# initialisation de la nouvelle vague
				elif Globals.transition_counter <= 0:
					self.wave = i+1
					self.level.waves[i](self.level)
					Globals.mists = []
					Globals.transition_counter = Globals.TRANSITION

		# ENNEMIES
		for enemy in Globals.enemies:

			enemy.update(player)

			# joueur touché
			if player.rect.colliderect(enemy.rect) and not player.hurted:
				player.heart -= 1
				player.hurted = True
				player.invincible_counter = player.INVINCIBLE

			# out of bounds
			if not enemy.alive or enemy.rect.top > screen.resolution[1]:
				del Globals.enemies[Globals.enemies.index(enemy)]

		# PROJECTILES
		for projectile in Globals.projectiles:
			projectile.update(player, screen)

		# JOUEUR
		player.update(keys, screen)

		# ARME
		if weapon != None:
			weapon.update(player)

		# POPUPS
		for popup in Globals.popups:
			popup.update(player, weapon)

		# GAME OVER

		# défaite
		if ((Globals.m == 0 and Globals.s == 0) or (not player.alive)) and not self.victory:
			self.over = True

		# victoire
		elif self.wave == len(self.level.waves) and Globals.enemies == []:
			Globals.transition_counter -= 1
			if Globals.transition_counter <= 0:
				self.victory = True

		# défaite d'un niveau
		if self.over:
			Globals.ecran = "game_over"
			Globals.m = 5
			Globals.s = 0
			Globals.transition_counter = Globals.TRANSITION
		# victoire d'un niveau
		elif self.victory:
			Globals.ecran = "game_victory"
			Globals.m = 5
			Globals.s = 0
			Globals.transition_counter = Globals.TRANSITION

	# ==================================================================================================================================

	def display(self, screen):

		player = self.level.player
		weapon = self.level.weapon

		# fond
		#screen.surface.fill(Globals.BLACK)
		screen.surface.blit(screen.background, (0,0))

		# blocs
		for block in Globals.blocks:
			block.display(screen)

		# ennemis
		for enemy in Globals.enemies:
			if enemy.alive:
				enemy.display(screen)

		# arme
		if weapon != None and weapon.alive and not player.weaponized:
			weapon.display(screen)

		# brouillard
		for mist in Globals.mists:
			mist.display(screen)

		# joueur
		player.display(screen)

		# projectiles
		for projectile in Globals.projectiles:
			projectile.display(screen)

		# popups
		for popup in Globals.popups:
			popup.display(screen, player, weapon)

		# texte
		fps_text = Globals.FONT.render(f"FPS : { int(self.clock.get_fps()) }", False, Globals.LIGHT_GRAY)
		wave_text = Globals.FONT.render(f"WAVE : { self.wave }", False, Globals.LIGHT_GRAY)
		heart_text = Globals.FONT.render(f"HEART : { player.heart }", False, Globals.RED)
		chrono_text = Globals.FONT.render(chronometre(), False, Globals.RED)
		#screen.surface.blit(fps_text, (5, 5) )
		#screen.surface.blit(wave_text, (5, 30) )
		#screen.surface.blit(heart_text, (5, 55) )
		screen.surface.blit(chrono_text, ( 3 * Globals.RATIO, 0.5 * Globals.RATIO) )

		# MISE A JOUR
		pygame.display.flip() # actualisation de l'écran
		Globals.counter += 1
		self.clock.tick(Globals.FPS)

# ==================================================================================================================================

def chronometre():

	if Globals.counter %60 == 0:
		if Globals.s == 0:
			Globals.s = 59
			Globals.m -= 1
		elif Globals.m == 0 and Globals.s == 0:
			Globals.s = 0
			Globals.m = 0
		else:
			Globals.s -= 1

	res = str(Globals.m) + ':' + str(Globals.s)
	return res