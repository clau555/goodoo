# -*- coding : utf-8 -*-

import pygame
import math
from global_variables import *

class Mist():

	def __init__(self, x, y):

		self.x = x * Globals.RATIO # x initial
		self.y = y * Globals.RATIO # y initial
		self.width = 1.0 * Globals.RATIO
		self.rect = pygame.Rect((self.x, self.y), (self.width,self.width)) # hitbox

		self.sprites = [pygame.image.load("./ressources/mist/1.png"), pygame.image.load("./ressources/mist/2.png")]
		self.animation_counter = 0
		self.sprite = self.sprites[self.animation_counter]
		
		Globals.mists.append(self)


	def animation(self):

		# passe au sprite suivant
		if Globals.counter%5 == 0:
			self.animation_counter += 1
		# revient au premier sprite une fois le 2e sprite passé
		if self.animation_counter >= len(self.sprites):
			self.animation_counter = 0

		self.sprite = self.sprites[self.animation_counter]


	def display(self, screen):
		self.animation()
		#pygame.draw.rect(screen.surface, Globals.PURPLE, self.rect) # hitbox
		screen.surface.blit(self.sprite, (self.rect.x, self.rect.y) )