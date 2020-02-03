# -*- coding : utf-8 -*-

import pygame

from global_variables import *
from classes.popup import *

class Weapon:

	def __init__(self, x, y):

		self.x = x
		self.y = y
		self.width = 1.0 * Globals.RATIO
		self.rect = pygame.Rect((self.x*Globals.RATIO, self.y*Globals.RATIO), (self.width,self.width)) # hitbox
		self.sprite = pygame.image.load("./ressources/weapon/1.png")

		self.alive = True

		self.popup = Popup(self.rect.x, self.rect.y, 'PICK ME', 'weapon' )

	def update(self, player):
		# attrapage de l'arme par le joueur
		if player.rect.colliderect(self.rect):
			player.weaponized = True
			if player.popup.TTL > 0:
				del Globals.popups[Globals.popups.index(player.popup)]
			player.popup = Popup( player.rect.x - 1.5 * Globals.RATIO, player.rect.y - 1 * Globals.RATIO, "   PRESS X", 'player' )
			self.popup.TTL = 0
			self.alive = False
			self = None

	def display(self, screen):
		#pygame.draw.rect(screen.surface, Globals.YELLOW, self.rect) # hitbox
		screen.surface.blit(self.sprite, (self.rect.x, self.rect.y) )
