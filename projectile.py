import pygame
import math
from gl0bals import *
from screen import *

class Projectile():

	def __init__(self, x, y, x_aim, y_aim):
		self.x = x
		self.y = y
		self.width = 0.5 * Globals.RATIO
		self.rect = pygame.Rect((self.x, self.y), (self.width,self.width)) # hitbox
		#self.sprites = [pygame.image.load("./ressources/projectile/1.jpg"), pygame.image.load("./ressources/projectile/1.jpg")]
		self.x_aim = x_aim
		self.y_aim = y_aim
		self.vx_direct = self.x_aim - self.x
		self.vy_direct = self.y_aim - self.y
		self.dist = math.sqrt((self.vx_direct)**2 + (self.vy_direct)**2)
		self.v_fixed = 0.2 * Globals.RATIO
		self.coef = self.dist / self.v_fixed
		self.vx = self.vx_direct / self.coef
		self.vy = self.vy_direct / self.coef

		self.sprites = [pygame.image.load("./ressources/projectile/1.png"), pygame.image.load("./ressources/projectile/2.png")]
		self.animation_counter = 0
		self.sprite = self.sprites [self.animation_counter]


		Globals.projectiles.append(self)


	def move_single_axis(self):
		self.rect.x += self.vx

		self.rect.y += self.vy


	def animation(self):
		"""Oriente le sprite joueur selon son dernier mouvement"""

		# passe au sprite suivant toute les 30 images
		if Globals.counter%10 == 0:
			self.animation_counter += 1
		# revient au premier sprite une fois le 2e sprite passé
		if self.animation_counter >= len(self.sprites):
			self.animation_counter = 0

		self.sprite = self.sprites[self.animation_counter]