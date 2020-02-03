# -*- coding : utf-8 -*-

import pygame

from global_variables import *
from classes.screen import *


class Menu():

	def __init__(self):
		self.selection = 0


	def body(self, screen):

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				Globals.launched = False

			# sélection des boutons
			elif event.type == pygame.KEYDOWN:
				# selection vers le bas
				if event.key == pygame.K_DOWN:
					self.selection += 1
				# selection vers le haut
				elif event.key == pygame.K_UP:
					self.selection -= 1
				# activation de la selection
				elif event.key == pygame.K_RETURN:
					if self.selection == 0:
						Globals.ecran = "select"
					elif self.selection == 1:
						Globals.ecran = "guide"
					elif self.selection == 2:
						Globals.launched = False

		keys = pygame.key.get_pressed()

		# FENETRE
		screen.update(keys)

		# SELECTION
		if self.selection > 2:
			self.selection = 0
		elif self.selection < 0:
			self.selection = 2


	def display(self, screen):

		# fond
		#screen.surface.fill(Globals.BLACK)
		screen.surface.blit(screen.background_menu, (0,0))

		# titre
		title = Globals.TITLE_FONT.render("GOODOO", False, Globals.WHITE)
		screen.surface.blit(title, (2*Globals.RATIO, 2*Globals.RATIO) )

		# start
		if self.selection == 0:
			play_button = Globals.FONT.render("PLAY <-", False, Globals.WHITE)
		else:
			play_button = Globals.FONT.render("PLAY", False, Globals.WHITE)
		screen.surface.blit(play_button, (2*Globals.RATIO, 6*Globals.RATIO) )

		# rules
		if self.selection == 1:
			rules_button = Globals.FONT.render("GUIDE <-", False, Globals.WHITE)
		else:
			rules_button = Globals.FONT.render("GUIDE", False, Globals.WHITE)
		screen.surface.blit(rules_button, (2*Globals.RATIO, 7.5*Globals.RATIO) )

		# quit
		if self.selection == 2:
			quit_button = Globals.FONT.render("QUIT <-", False, Globals.RED)
		else:
			quit_button = Globals.FONT.render("QUIT", False, Globals.WHITE)
		screen.surface.blit(quit_button, (2*Globals.RATIO, 9*Globals.RATIO) )


		# actualisation de l'écran
		pygame.display.flip()

		
		# ========== MISE A JOUR

		Globals.counter += 1