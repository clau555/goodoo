# -*- coding : utf-8 -*-

import pygame
from global_variables import *

class Screen():

	def __init__(self):

		self.resolution = Globals.RESOLUTION
		self.surface = pygame.display.set_mode((self.resolution))
		self.fullscreen = False
		self.icon = pygame.image.load("ressources/icon.jpg")
		pygame.display.set_icon(self.icon) # icône de la fenêtre
		pygame.display.set_caption("Goodoo") # titre de la fenêtre
		self.background_game = pygame.image.load("ressources/backgrounds/game.jpg").convert()
		self.background_menu = pygame.image.load("ressources/backgrounds/menu.jpg").convert()
		self.background_over = pygame.image.load("ressources/backgrounds/over.jpg").convert()
		self.background_victory = pygame.image.load("ressources/backgrounds/victory.jpg").convert()
		self.guide = pygame.image.load("ressources/backgrounds/guide.jpg").convert()

	def update(self, keys):

		# quitter
		if keys[pygame.K_ESCAPE]:
			Globals.launched = False

		# plein écran
		if keys[pygame.K_F11] and self.fullscreen==False:
			self.surface = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
			pygame.mouse.set_visible(False)
			self.fullscreen = True
		elif keys[pygame.K_F11] and self.fullscreen==True:
			self.surface = pygame.display.set_mode(self.resolution)
			pygame.mouse.set_visible(True)
			self.fullscreen = False