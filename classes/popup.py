import pygame
from gl0bals import *

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