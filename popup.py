# -*- coding : utf-8 -*-

import pygame
from global_variables import *

class Popup():

	def __init__(self, x, y, text, type):

		self.x = x # x initial
		self.y = y # y initial

		self.FONT = pygame.font.Font("./ressources/FFFFORWA.TTF", 10)
		self.string = text
		self.text = self.FONT.render(text, True, Globals.LIGHT_GRAY)

		self.type = type
		self.TTL = Globals.TRANSITION * 1.5

		Globals.popups.append(self)


	def animation(self):

		if Globals.counter % 10 == 0:
			self.text = self.FONT.render(self.string, False, Globals.RED)

		elif Globals.counter % 5 == 0:
			self.text = self.FONT.render(self.string, False, Globals.LIGHT_GRAY)

	def update(self, player, weapon):

		if self.TTL > 0:
			self.TTL -= 1
		
		if self.type == "player":
			self.x = player.rect.x - 1.5 * Globals.RATIO
			self.y = player.rect.y - 1 * Globals.RATIO

		if self.type == "weapon" and weapon != None:
			self.x = weapon.rect.x - 1 * Globals.RATIO
			self.y = weapon.rect.y - 1 * Globals.RATIO
		elif self.type == "weapon" and player.weaponized:
			self.TTL = 0
		
		if self.TTL == 0:
			del Globals.popups[Globals.popups.index(self)]

	def display(self, screen, player, weapon):
		self.animation()
		if self.type == 'weapon' and weapon != None:
			screen.surface.blit(self.text, (self.x, self.y) )
		elif self.type != 'weapon':
			screen.surface.blit(self.text, (self.x, self.y) )