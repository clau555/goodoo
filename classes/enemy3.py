import pygame
import random
from gl0bals import *
from classes.entity import *
from classes.block import *


class Enemy3(Entity):

	def __init__(self, x, y):

		super().__init__(
						x, # x initial
						y, # y initial
						2.5, # largeur
						2.5, # hauteur
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité x
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité y
						0.05, # vélocité fixée
						[ pygame.image.load("./ressources/enemy3/1.png"), pygame.image.load("./ressources/enemy3/2.png"),
						pygame.image.load("./ressources/enemy3/3.png"), pygame.image.load("./ressources/enemy3/4.png") ], # sprites de droite
						[ pygame.image.load("./ressources/enemy3/5.png"), pygame.image.load("./ressources/enemy3/6.png"),
						pygame.image.load("./ressources/enemy3/7.png"), pygame.image.load("./ressources/enemy3/8.png"), ] # sprites de gauche
						)

		Globals.enemies.append(self)
		Globals.enemies3.append(self)

	def animation(self, last_move):
		"""Oriente le sprite joueur selon son dernier mouvement"""

		# passe au sprite suivant toute les 10 images (0.2 sec)
		if Globals.counter%10 == 0:
			self.animation_counter += 1
		# revient au premier sprite une fois le 2e sprite passé
		if self.animation_counter >= len(self.sprites_right):
			self.animation_counter = 0

		# oriente le sprite
		if last_move=="right" :
			self.sprite = self.sprites_right[self.animation_counter]

		elif last_move=="left" :
			self.sprite = self.sprites_left[self.animation_counter]