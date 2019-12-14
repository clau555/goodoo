import pygame
import random
from gl0bals import *
from classes.entity import *
from classes.block import *


class Enemy2(Entity):

	def __init__(self, x, y):

		super().__init__(
						x, # x initial
						y, # y initial
						1.0, # largeur
						1.5, # hauteur
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité x
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité y
						0.05, # vélocité fixée
						[ pygame.image.load("./ressources/enemy2/1.png") ], # sprites de droite
						[ pygame.image.load("./ressources/enemy2/2.png") ] # sprites de gauche
						)

		Globals.enemies.append(self)
		Globals.enemies2.append(self)