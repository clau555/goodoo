import pygame
import random
from gl0bals import *
from entity import *
from block import *


class Enemy(Entity):

	def __init__(self, x, y):

		super().__init__(
						x, # x initial
						y, # y initial
						0.6, # largeur
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité x
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité y
						random.uniform(0.01, 0.2), # vélocité fixée
						[ pygame.image.load("./ressources/enemy1/1.png"), pygame.image.load("./ressources/enemy1/2.png") ], # sprites à droite
						[ pygame.image.load("./ressources/enemy1/1.png"), pygame.image.load("./ressources/enemy1/2.png") ] # sprites à gauche
						)

		Globals.enemies.append(self)