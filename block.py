import pygame
from globals import * 

class Block():


	def __init__(self, pos):

		self.rect = pygame.Rect((pos[0], pos[1]),(ratio,ratio))
