# -*- coding : utf-8 -*-

import pygame
from global_variables import *

class Block():

	def __init__(self, pos):
		self.rect = pygame.Rect((pos[0], pos[1]),(Globals.RATIO,Globals.RATIO))
		self.sprite = pygame.image.load("./ressources/block/1.png")

	def display(self, screen):
		pygame.draw.rect(screen.surface, Globals.WHITE, self.rect) # hitbox
		#screen.surface.blit(self.sprite, (self.rect.x, self.rect.y) )