import pygame
from environnements import *
from mother import Mother

class Block(Mother):


	def __init__(self, pos):

		Mother.__init__(self)
		self.rect = pygame.Rect((pos[0], pos[1]),(self.ratio,self.ratio))
