import pygame
from gl0bals import *
from classes.screen import *

class Entity:

	def __init__(self, x:float, y:float, width:float, height:float, vx:float, vy:float, v_fixed:float, sprites_right:list, sprites_left:list):

		# ne servent qu'à l'initialisation
		self.x = x * Globals.RATIO
		self.y = y * Globals.RATIO
		
		self.width = width * Globals.RATIO
		self.height = height * Globals.RATIO

		self.rect = pygame.Rect((self.x, self.y), (self.width,self.height)) # hitbox

		self.vx = vx # plage des vitesses en x
		self.vy = vy # plage des vitesses en y

		self.vx_index = len(self.vx)//2 # rang de la plage de vitesse en x, permet l'accéléGlobals.RATIOn
		self.vy_index = len(self.vy)//2 # rang de la plage de vitesse en y, permet l'accéléGlobals.RATIOn
		self.v_fixed = v_fixed # vélocité fixée lors des déplacements gauche/droite de l'utilisateur

		self.sprites_right = sprites_right
		self.sprites_left = sprites_left
		# conversion des sprites (pb de fps sinon)
		for sprite in sprites_right:
			sprite.convert()
		for sprite in sprites_left:
			sprite.convert()

		self.animation_counter = 0
		self.sprite = self.sprites_right[self.animation_counter] # sprite courant
		self.last_move = "right"
		
		self.isjump = False
		self.onground = False
		self.iscollide = False
		self.blockcollide = None
		self.killed = False


	def move(self, vx, vy):
		"""Bouge chaque axe séparemment"""

		if vx != 0:
			self.move_single_axis(vx, 0)
		if vy != 0:
			self.move_single_axis(0, vy)



	def move_single_axis(self, vx, vy):
		"""Bouge le rectangle de l'entitée en fonction de vx et vy
		
		[description]
		
		Arguments:
			vx {float} -- distance à parcourir en x
			vy {float} -- distance à parcourir en y
		"""

		# initialise les collisions
		self.iscollide = False
		self.blockcollide = pygame.Rect( (0, 0) , (0, 0) )


		# bouge le rect
		self.rect.x += vx*Globals.RATIO
		self.rect.y += vy*Globals.RATIO

		# Si collision avec un bloc, se repositionne
		for block in Globals.blocks:
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

		# out of bounds
		if self.rect.left <= 0:
			self.rect.left = 0
		elif self.rect.right >= Globals.RESOLUTION[0]:
			self.rect.right = Globals.RESOLUTION[0]



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



	def animation(self, last_move):
		"""Oriente le sprite joueur selon son dernier mouvement"""

		# passe au sprite suivant toute les 30 images
		if Globals.counter%30 == 0:
			self.animation_counter += 1
		# revient au premier sprite une fois le 2e sprite passé
		if self.animation_counter >= len(self.sprites_right):
			self.animation_counter = 0

		# oriente le sprite
		if last_move=="right" :
			self.sprite = self.sprites_right[self.animation_counter]

		elif last_move=="left" :
			self.sprite = self.sprites_left[self.animation_counter]