# -*- coding : utf-8 -*-

import pygame
import random
from global_variables import *
from classes.entity import *
from classes.block import *
from classes.projectile import *


class Enemy3(Entity):

	def __init__(self, x, y):

		super().__init__(
						(x , y), # position initiale
						(2.5 , 2.5), # dimensions
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité x
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité y
						[ pygame.image.load("./ressources/enemy3/1.png"), pygame.image.load("./ressources/enemy3/2.png"),
						pygame.image.load("./ressources/enemy3/3.png"), pygame.image.load("./ressources/enemy3/4.png") ], # sprites de droite
						[ pygame.image.load("./ressources/enemy3/5.png"), pygame.image.load("./ressources/enemy3/6.png"),
						pygame.image.load("./ressources/enemy3/7.png"), pygame.image.load("./ressources/enemy3/8.png"), ] # sprites de gauche
						)
		Globals.enemies.append(self)


	def animation(self, last_move):

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


	def update(self, player):

		# tir horizontal
		if Globals.counter%40 == 0 and player.rect.top >= self.rect.top and player.rect.bottom <= self.rect.bottom:
			# tir à gauche
			if (player.rect.right <= self.rect.left):
				Projectile(self.rect.x + self.width/2, self.rect.y + self.width/2, self.rect.x, self.rect.y + self.width/2,self)
			# tir à droite
			elif (player.rect.left >= self.rect.right):
				Projectile(self.rect.x + self.width/2, self.rect.y + self.width/2, self.rect.x + self.width, self.rect.y + self.width/2,self)
		# tir polydirectionnel
		elif Globals.counter%180 == 0:
			Projectile(self.rect.x + self.width/2, self.rect.y + self.width/2, self.rect.x, self.rect.y,self)
			Projectile(self.rect.x + self.width/2, self.rect.y + self.width/2, self.rect.x + self.width/2, self.rect.y,self)
			Projectile(self.rect.x + self.width/2, self.rect.y + self.width/2, self.rect.x + self.width, self.rect.y,self)
			Projectile(self.rect.x + self.width/2, self.rect.y + self.width/2, self.rect.x + self.width, self.rect.y + self.width/2,self)
			Projectile(self.rect.x + self.width/2, self.rect.y + self.width/2, self.rect.x + self.width, self.rect.y + self.width,self)
			Projectile(self.rect.x + self.width/2, self.rect.y + self.width/2, self.rect.x + self.width /2, self.rect.y + self.width,self)
			Projectile(self.rect.x + self.width/2, self.rect.y + self.width/2, self.rect.x, self.rect.y + self.width,self)
			Projectile(self.rect.x + self.width/2, self.rect.y + self.width/2, self.rect.x, self.rect.y + self.width/2,self)

		# orentation vers le joueur
		if self.rect.x + self.width/2 < player.rect.x:
			self.last_move = "right"
		elif self.rect.x + self.width/2 >= player.rect.x:
			self.last_move = "left"


	def display(self, screen):
			self.animation(self.last_move)
			#pygame.draw.rect(screen.surface, Globals.RED, self.rect) # hitbox
			screen.surface.blit(self.sprite, (self.rect.x, self.rect.y) )
