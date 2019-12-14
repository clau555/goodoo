import pygame
from gl0bals import *
from classes.popup import *

class Weapon:

	def __init__(self, x, y):

		self.x = x
		self.y = y
		self.width = 1.0 * Globals.RATIO
		self.rect = pygame.Rect((self.x*Globals.RATIO, self.y*Globals.RATIO), (self.width,self.width)) # hitbox
		self.sprite = pygame.image.load("./ressources/weapon/1.png")

		self.popup = Popup(self.rect.x, self.rect.y, 'PICK ME', 'weapon' )