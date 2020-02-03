# -*- coding : utf-8 -*-

import pygame
import random
from global_variables import *
from classes.entity import *
from classes.block import *
from classes.projectile import *


class Enemy2(Entity):

	def __init__(self, x, y):

		super().__init__(
						(x , y), # position initiale
						(1.0 , 1.5), # dimensions
						list([(i / 100.0)+0.01 for i in range(0, 5)]), # plage de vélocités x
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité y
						[ pygame.image.load("./ressources/enemy2/1.png") ], # sprites de droite
						[ pygame.image.load("./ressources/enemy2/2.png") ] # sprites de gauche
						)
		Globals.enemies.append(self)
		

	def update(self, player):

		# déplacement gauche
		if Globals.counter%480 <= 120:
			self.last_move = "left"
			self.x_speeds_index += 1
			if self.x_speeds_index >= len(self.x_speeds):
				self.x_speeds_index = len(self.x_speeds) - 1
			self.move(-self.x_speeds[self.x_speeds_index], 0)

		# déplacement droit
		elif 240 < Globals.counter%480 <= 360 :
			self.last_move = "right"
			self.x_speeds_index += 1
			if self.x_speeds_index >= len(self.x_speeds):
				self.x_speeds_index = len(self.x_speeds) - 1
			self.move(self.x_speeds[self.x_speeds_index], 0)

		else:
			self.x_speeds_index = 0

		# gravité
		if not self.jumping:
			self.gravity()

		# tir
		if Globals.counter%180 == 0 and self.alive:
			Projectile(self.rect.x, self.rect.y, player.rect.x + player.width/2, player.rect.y + player.height/2,self)


	def display(self, screen):
			self.animation(self.last_move)
			#pygame.draw.rect(screen.surface, Globals.RED, self.rect) # hitbox
			screen.surface.blit(self.sprite, (self.rect.x, self.rect.y) )
