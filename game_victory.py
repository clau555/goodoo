# -*- coding : utf-8 -*-

import pygame

from gl0bals import *
from classes.screen import *


class GameVictory:

	def __init__(self):
		pass


	def body(self, screen):

		# EVENTS
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				Globals.launched = False

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					Globals.ecran = "select"

		# FENETRE
		keys = pygame.key.get_pressed()
		screen.update(keys)


	def display(self, screen):

		# fond
		#screen.surface.fill(Globals.BLACK)
		screen.surface.blit(screen.background_victory, (0,0))

		# titre
		title = Globals.TITLE_FONT.render("VICTORY", False, Globals.WHITE)
		screen.surface.blit(title, (1*Globals.RATIO, 1*Globals.RATIO) )

		# retour arrière
		back_button = Globals.FONT.render("MENU <-", False, Globals.WHITE)

		screen.surface.blit(back_button, (4*Globals.RATIO, 6*Globals.RATIO) )
		
		# MISE A JOUR
		pygame.display.flip()
		Globals.counter += 1