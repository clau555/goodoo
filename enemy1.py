# -*- coding : utf-8 -*-

import pygame
import random
from global_variables import *
from classes.entity import *
from classes.block import *


class Enemy1(Entity):

	def __init__(self, x, y):

		super().__init__(
						(x , y), # position initiale
						(0.6 , 0.6), # dimensions
						None, # plages de vélocités en x inutile ici
						list([(i / 20.0) - 1 for i in range(0, 40)]), # plages de vélocités en y
						[ pygame.image.load("./ressources/enemy1/1.png"), pygame.image.load("./ressources/enemy1/2.png") ], # sprites de droite
						[ pygame.image.load("./ressources/enemy1/1.png"), pygame.image.load("./ressources/enemy1/2.png") ] # sprites de gauche
						)
		Globals.enemies.append(self)


	def update(self, player):

		# déplacement gauche
		if self.rect.x > player.rect.x:
			self.move(-random.uniform(0.05, 0.1), 0) # vitesse aléatoire

		# déplacement droit
		if self.rect.x < player.rect.x:
			self.move(random.uniform(0.05, 0.1), 0) # vitesse aléatoire

		# saut
		if self.on_ground and not self.jumping:
			self.jumping = True
			self.y_speeds_index = len(self.y_speeds)//random.randint(3,6) # rang de vélocité d'impulsion initiale
		if self.jumping:
			self.jump()

		# gravité
		if not self.jumping:
			self.gravity()


	def display(self, screen):
			self.animation(self.last_move)
			#pygame.draw.rect(screen.surface, Globals.RED, self.rect) # hitbox
			screen.surface.blit(self.sprite, (self.rect.x, self.rect.y) )