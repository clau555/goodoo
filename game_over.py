# -*- coding : utf-8 -*-

import pygame

from gl0bals import *
from classes.screen import *


class GameOver:

	def __init__(self):
		self.selection = 1


	def body(self, screen):

		# EVENTS
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				Globals.launched = False

			elif event.type == pygame.KEYDOWN:

				# selection

				if event.key == pygame.K_DOWN:
					self.selection += 1

				elif event.key == pygame.K_UP:
					self.selection -= 1

				# activation de la selection
				elif event.key == pygame.K_RETURN:
					# retour arrière
					if self.selection == 0:
						Globals.ecran = "select"
					# lancement d'un niveau
					elif self.selection == 1:
						Globals.ecran = "game"

		#  FENETRE
		keys = pygame.key.get_pressed()
		screen.update(keys)

		# SELECTION
		if self.selection > 1:
			self.selection = 1
		elif self.selection < 0:
			self.selection = 0


	def display(self, screen):

		# fond
		#screen.surface.fill(Globals.BLACK)
		screen.surface.blit(screen.background_over, (0,0))

		# titre
		title = Globals.TITLE_FONT.render("GAME OVER", False, Globals.RED)
		screen.surface.blit(title, (1*Globals.RATIO, 1*Globals.RATIO) )

		# retour arrière
		if self.selection == 0:
			back_button = Globals.FONT.render("MENU <-", False, Globals.RED)
			retry_button = Globals.FONT.render("RETRY", False, Globals.WHITE)
		elif self.selection == 1:
			back_button = Globals.FONT.render("MENU", False, Globals.WHITE)
			retry_button = Globals.FONT.render("RETRY <-", False, Globals.WHITE)

		screen.surface.blit(back_button, (4*Globals.RATIO, 6*Globals.RATIO) )
		screen.surface.blit(retry_button, (4*Globals.RATIO, 8*Globals.RATIO) )
		
		# MISE A JOUR
		pygame.display.flip()
		Globals.counter += 1