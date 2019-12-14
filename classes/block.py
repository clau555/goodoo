import pygame
from gl0bals import *

class Block():

	def __init__(self, pos):
		self.rect = pygame.Rect((pos[0], pos[1]),(Globals.RATIO,Globals.RATIO))
		self.sprite = pygame.image.load("./ressources/block/1.png")