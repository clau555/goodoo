import pygame
from gl0bals import *

class Screen():

	def __init__(self):

		self.resolution = Globals.RESOLUTION
		self.surface = pygame.display.set_mode((self.resolution))
		self.fullscreen = False
		self.icon = pygame.image.load("ressources/icon.jpg")
		pygame.display.set_icon(self.icon) # icône de la fenêtre
		pygame.display.set_caption("Goodoo") # titre de la fenêtre
		self.background = pygame.image.load("ressources/background.jpg").convert()
		self.guide = pygame.image.load("ressources/guide.jpg").convert()