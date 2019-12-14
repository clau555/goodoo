import pygame
import random
from gl0bals import *
from classes.entity import *
from classes.block import *


class Enemy1(Entity):

	def __init__(self, x, y):

		super().__init__(
						x, # x initial
						y, # y initial
						0.6, # largeur
						0.6, # hauteur
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité x
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité y
						random.uniform(0.05, 0.18), # vélocité fixée
						[ pygame.image.load("./ressources/enemy1/1.png"), pygame.image.load("./ressources/enemy1/2.png") ], # sprites de droite
						[ pygame.image.load("./ressources/enemy1/1.png"), pygame.image.load("./ressources/enemy1/2.png") ] # sprites de gauche
						)

		Globals.enemies.append(self)
		Globals.enemies1.append(self)