import pygame
from gl0bals import *
from entity import *
from block import *


class Player(Entity):

	def __init__(self, x, y):

		super().__init__(
						x, # x initial
						y, # y initial
						1.0, # largeur
						1.0, # hauteur
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité x
						list([(i / 20.0) - 1 for i in range(0, 40)]), # vélocité y
						0.2, # vélocité fixée
						[ pygame.image.load("./ressources/goodoo_white/1.png"), pygame.image.load("./ressources/goodoo_white/2.png") ], # sprites de droite
						[ pygame.image.load("./ressources/goodoo_white/3.png"), pygame.image.load("./ressources/goodoo_white/4.png") ] # sprites de gauche
						)

		self.weaponized = False
		self.hit_rect = None
		self.hit_sprite_right = pygame.image.load("./ressources/hit/1.png")
		self.hit_sprite_left = pygame.image.load("./ressources/hit/2.png")
		self.cooldown = 0
		self.COOLDOWN = 10


	def hit(self):

		self.cooldown = 30

		# oriente la zone de frappe
		if self.last_move=="right" :
			self.hit_rect = pygame.Rect((self.rect.x, self.rect.y - Globals.RATIO), (2*self.width, 2*self.height))

		elif self.last_move=="left" :
			self.hit_rect = pygame.Rect((self.rect.x - Globals.RATIO, self.rect.y - Globals.RATIO), (2*self.width, 2*self.height))
		
		# tue les ennemies dans la zone
		for enemy in Globals.enemies:

			if self.hit_rect.colliderect(enemy.rect):
				enemy.killed = True
	"""
	def hit_animation(self, last_move):

		# passe au sprite suivant toute les 2 images
		if Globals.counter%2 == 0:
			self.animation_counter += 1
		# revient au premier sprite une fois le 2e sprite passé
		if self.animation_counter >= len(self.sprites_right):
			self.animation_counter = 0

		# oriente le sprite
		if last_move=="right" :
			self.sprite = self.sprites_right[self.animation_counter]

		elif last_move=="left" :
			self.sprite = self.sprites_left[self.animation_counter]
	"""