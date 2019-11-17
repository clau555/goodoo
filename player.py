import pygame
from gl0bals import *
from entity import *
from block import *


class Player(Entity):

	def __init__(self, x, y):

		super().__init__(
						x, # x initial
						y, # y initial
						1.0, # largeur
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité x
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité y
						0.2, # vélocité fixée
						[ pygame.image.load("./ressources/goodoo_white/1.png"),
						pygame.image.load("./ressources/goodoo_white/2.png") ], # sprites à droite
						[ pygame.image.load("./ressources/goodoo_white/3.png"),
						pygame.image.load("./ressources/goodoo_white/4.png") ] # sprites à gauche
						)