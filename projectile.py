import pygame
from gl0bals import *
from screen import *

class Projectile():

	def __init__(self, x, y, x_aim, y_aim):
		self.x = x
		self.y = y
		self.rect = pygame.Rect((self.x*Globals.RATIO, self.y*Globals.RATIO), (0.4,0.4)) # hitbox
		[pygame.image.load("./ressources/projectile.jpg")]
		



		Globals.projectiles.append(self)

	def move_single_axis(self,vx,vy):
		self.rect.x += vx*Globals.RATIO
		self.rect.y += vy*Globals.RATIO

	def out_of_bound(self, x, y):
		res = False
		if x > 1280 or x < 0 or y < 0 or y > 720:
			res = True
		print(res)


