import pygame
import random
from block import Block
from globals import *

class Enemy(Block):

	def __init__(self, x, y):

		enemies.append(self)

		self.width = 0.6

		# ne servent qu'à l'initialisation
		self.x = x
		self.y = y

		self.rect = pygame.Rect((self.x*ratio, self.y*ratio), (self.width*ratio,self.width*ratio)) # hitbox

		self.vx = list([(i / 20.0) - 1 for i in range(0, 40)]) # plage des vitesses en x
		self.vy = list([(i / 20.0) - 1 for i in range(0, 40)]) # plage des vitesses en y
		self.vx_index = len(self.vx)//2 # rang de la plage de vitesse en x, permet l'accélération
		self.vy_index = len(self.vy)//2 # rang de la plage de vitesse en y, permet l'accélération
		self.v_fixed = random.uniform(0.05, 0.2) # vélocité fixée lors des déplacements gauche/droite de l'utilisateur
		print(self.v_fixed)

		self.sprites = [ pygame.image.load("./ressources/enemy1/1.png"),
						pygame.image.load("./ressources/enemy1/2.png")]
		self.animation_counter = 0
		self.sprite = self.sprites[self.animation_counter] # sprite courant

		self.isjump = False
		self.onground = False
		self.iscollide = False
		self.blockcollide = pygame.Rect( (0, 0) , (0, 0) )

		self.animation_counter = 0
		


	def move(self, vx, vy):
		"""Bouge chaque axe séparemment"""

		if vx != 0:
			self.move_single_axis(vx, 0)
		if vy != 0:
			self.move_single_axis(0, vy)



	def move_single_axis(self, vx, vy):
		"""Bouge en fonction de vx et vy"""

		# initialise les collisions
		self.iscollide = False
		self.blockcollide = pygame.Rect( (0, 0) , (0, 0) )


		# bouge le rect
		self.rect.x += vx*ratio
		self.rect.y += vy*ratio

		# Si collision avec un bloc, se repositionne
		for block in blocks:
			if self.rect.colliderect(block.rect):

				self.blockcollide = block.rect # sauvegarde du bloc en collision
				self.iscollide = True

				if vx > 0:
					self.rect.right = self.blockcollide.left
				if vx < 0:
					self.rect.left = self.blockcollide.right
				if vy > 0:
					self.rect.bottom = self.blockcollide.top
					self.onground = True
				if vy < 0:
					self.rect.top = self.blockcollide.bottom
					self.isjump = False
					self.vy_index = len(self.vy)//2



	def gravity(self):

		self.onground = False

		self.move_single_axis(0, self.vy[self.vy_index])
		self.vy_index += 1

		# on ramène la vélocité à 0 si collision avec le sol
		if self.onground:
			self.vy_index = len(self.vy)//2

		# blocage de la vélocité si à son maximum
		if (self.vy_index >= len(self.vy)-1):
			self.vy_index = len(self.vy)-1



	def jump(self):

		self.move_single_axis(0, self.vy[self.vy_index])
		self.vy_index += 1

		if (self.vy_index >= len(self.vy)//2):
			self.vy_index = len(self.vy)//2
			self.isjump = False



	def animation(self):
		"""Oriente le sprite joueur selon son dernier mouvement"""

		# passe au sprite suivant toute les 20 images
		if counter%20 == 0:
			self.animation_counter += 1
		# revient au premier sprite une fois le 2e sprite passé
		if self.animation_counter >= len(self.sprites):
			self.animation_counter = 0

		# dessine le sprite
		self.sprite = self.sprites[self.animation_counter]