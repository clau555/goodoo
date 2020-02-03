# -*- coding : utf-8 -*-

import pygame
import math
from global_variables import *

class Big_button():

	def __init__(self, x, y, sprite):

		self.x = x * Globals.RATIO # x initial
		self.y = y * Globals.RATIO # y initial
		self.width = 64 * Globals.RATIO * 4
		self.height = 36 * Globals.RATIO * 4
		self.rect = pygame.Rect((self.x, self.y), (self.width, self.height)) # hitbox

		self.sprite = sprite