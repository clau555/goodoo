# -*- coding : utf-8 -*-

import pygame
from global_variables import *
from classes.screen import *

class Entity:

	def __init__(self, pos_init, dimension, x_speeds, y_speeds, sprites_right, sprites_left):

		self.pos_init = ( pos_init[0] * Globals.RATIO , pos_init[1] * Globals.RATIO )
		self.width = dimension[0] * Globals.RATIO
		self.height = dimension[1] * Globals.RATIO

		self.rect = pygame.Rect( self.pos_init , (self.width , self.height) ) # hitbox

		self.x_speeds = x_speeds # plage des vitesses en x
		self.y_speeds = y_speeds # plage des vitesses en y

		self.x_speeds_index = 0 # rang de la plage de vitesse en x, permet l'accélération
		self.y_speeds_index = len(self.y_speeds)//2 # rang de la plage de vitesse en y, permet l'accélération

		self.sprites_right = sprites_right
		self.sprites_left = sprites_left
		# conversion des sprites
		for sprite in sprites_right:
			sprite.convert()
		for sprite in sprites_left:
			sprite.convert()

		self.animation_counter = 0
		self.sprite = self.sprites_right[self.animation_counter] # sprite courant
		self.last_move = "right"
		
		self.jumping = False
		self.on_ground = False
		self.colliding = False
		self.colliding_block = None
		self.alive = True


	def move(self, vx, vy):

		if vx != 0:
			self.move_single_axis(vx, 0)
		if vy != 0:
			self.move_single_axis(0, vy)



	def move_single_axis(self, vx, vy):

		# initialise les collisions
		self.colliding = False
		self.colliding_block = pygame.Rect( (0, 0) , (0, 0) )

		# bouge le rect
		self.rect.x += vx*Globals.RATIO
		self.rect.y += vy*Globals.RATIO

		# Si collision avec un bloc, se repositionne
		for block in Globals.blocks:
			if self.rect.colliderect(block.rect):

				self.colliding_block = block.rect
				self.colliding = True

				if vx > 0:
					self.rect.right = self.colliding_block.left
				if vx < 0:
					self.rect.left = self.colliding_block.right
				if vy > 0:
					self.rect.bottom = self.colliding_block.top
					self.on_ground = True
				if vy < 0:
					self.rect.top = self.colliding_block.bottom
					self.jumping = False
					self.y_speeds_index = len(self.y_speeds)//2

		# out of bounds
		if self.rect.left <= 0:
			self.rect.left = 0
		elif self.rect.right >= Globals.RESOLUTION[0]:
			self.rect.right = Globals.RESOLUTION[0]



	def gravity(self):

		self.on_ground = False

		self.move_single_axis(0, self.y_speeds[self.y_speeds_index])
		self.y_speeds_index += 1

		# ramène la vélocité à 0 si collision avec le sol
		if self.on_ground:
			self.y_speeds_index = len(self.y_speeds)//2

		# blocage de la vélocité si à son maximum
		if (self.y_speeds_index >= len(self.y_speeds)-1):
			self.y_speeds_index = len(self.y_speeds)-1



	def jump(self):

		self.move_single_axis(0, self.y_speeds[self.y_speeds_index])
		self.y_speeds_index += 1

		if (self.y_speeds_index >= len(self.y_speeds)//2):
			self.y_speeds_index = len(self.y_speeds)//2
			self.jumping = False



	def animation(self, last_move):

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