# -*- coding : utf-8 -*-

import pygame

from gl0bals import *
from classes.screen import *


class Guide:

	def __init__(self):
		pass


	def body(self, screen):

		# EVENTS
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				Globals.launched = False

			elif event.type == pygame.KEYDOWN:
				# activation de la selection
				if event.key == pygame.K_RETURN:
					Globals.ecran = "menu"
					
		# FENETRE
		keys = pygame.key.get_pressed()
		screen.update(keys)


	def display(self, screen):

		# fond
		screen.surface.blit(screen.guide, (0,0))

		# titre
		title = Globals.TITLE_FONT.render("GUIDE", False, Globals.WHITE)
		screen.surface.blit(title, (1*Globals.RATIO, 1*Globals.RATIO) )

		# retour arrière
		back_button = Globals.FONT.render("BACK <-", False, Globals.WHITE)
		screen.surface.blit(back_button, (1*Globals.RATIO, 4*Globals.RATIO) )

		# MISE A JOUR
		pygame.display.flip()
		Globals.counter += 1