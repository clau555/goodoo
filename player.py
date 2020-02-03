# -*- coding : utf-8 -*-

import pygame
from global_variables import *
from classes.entity import *
from classes.block import *
from classes.popup import *
from classes.projectile import *


class Player(Entity):

	def __init__(self, x, y):

		super().__init__(
						(x , y), # position initiale
						(1.0 , 1.0), # dimensions
						list([(i / 100.0) + 0.1 for i in range(0, 20)]), # plage de vélocités x
						list([(i / 20.0) - 1 for i in range(0, 40)]), # plage de vélocités y
						[ pygame.image.load("./ressources/goodoo_white/1.png"), pygame.image.load("./ressources/goodoo_white/2.png") ], # sprites de droite
						[ pygame.image.load("./ressources/goodoo_white/3.png"), pygame.image.load("./ressources/goodoo_white/4.png") ] # sprites de gauche
						)

		self.weaponized = False # vrai si possède l'arme (weapon)
		self.hit_rect = None # zone de dégât d'une frappe
		self.hit_sprite_right = pygame.image.load("./ressources/hit/1.png")
		self.hit_sprite_left = pygame.image.load("./ressources/hit/2.png")

		self.COOLDOWN = 10 # temps de recharge d'une frappe
		self.cooldown_counter = 0

		self.heart = 5 # barre de vie
		self.heart_sprite = [ pygame.image.load("./ressources/heart/5.png"), pygame.image.load("./ressources/heart/4.png"),
							pygame.image.load("./ressources/heart/3.png"), pygame.image.load("./ressources/heart/2.png"),
							pygame.image.load("./ressources/heart/1.png"), pygame.image.load("./ressources/heart/0.png") ]

		self.INVINCIBLE = 180 # temps d'invicibilité après être touché
		self.invincible_counter = 0
		self.hurted = False # vrai si touché

		self.popup = Popup(self.rect.x, self.rect.y, "YOU'RE HERE", 'player' )


	def hit(self):

		decalage = 0.3*Globals.RATIO

		# oriente la zone de frappe
		if self.last_move=="right" :
			self.hit_rect = pygame.Rect((self.rect.x, self.rect.y - Globals.RATIO), (2*self.width + decalage, 2*self.height))

		elif self.last_move=="left" :
			self.hit_rect = pygame.Rect((self.rect.x - Globals.RATIO - decalage, self.rect.y - Globals.RATIO), (2*self.width + decalage, 2*self.height))
		
		# tue les ennemies dans la zone
		for enemy in Globals.enemies:

			if self.hit_rect.colliderect(enemy.rect):
				enemy.alive = False


	def update(self, keys, screen):

		# déplacement gauche
		if keys[pygame.K_LEFT]:
			if not(keys[pygame.K_RIGHT]):
				self.last_move = "left"
			self.x_speeds_index += 1
			if self.x_speeds_index >= len(self.x_speeds):
				self.x_speeds_index = len(self.x_speeds) - 1
			self.move(-self.x_speeds[self.x_speeds_index], 0)

		# déplacement droit
		elif keys[pygame.K_RIGHT]:
			if not(keys[pygame.K_LEFT]):
				self.last_move = "right"
			self.x_speeds_index += 1
			if self.x_speeds_index >= len(self.x_speeds):
				self.x_speeds_index = len(self.x_speeds) - 1
			self.move(self.x_speeds[self.x_speeds_index], 0)

		# aucun déplacement
		else:
			self.x_speeds_index = 0

		# saut
		if keys[pygame.K_SPACE] and self.on_ground and not self.jumping:
			self.jumping = True
			self.y_speeds_index = len(self.y_speeds)//6 # rang de vélocité d'impulsion initiale
		if self.jumping:
			self.jump()

		#gateling
		if keys[pygame.K_w]:
			pygame.mouse.set_visible(True)
			Projectile(self.rect.x, self.rect.y, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],self)

		# gravité
		if not self.jumping:
			self.gravity()

		# frappe
		if self.weaponized and keys[pygame.K_x] and self.cooldown_counter == 0:
			self.hit()
			self.cooldown_counter = self.COOLDOWN + 1
		if self.cooldown_counter > 0:
			self.cooldown_counter -= 1

		# touché
		if self.hurted and self.invincible_counter > 0:
			self.invincible_counter -= 1
		elif self.hurted and self.invincible_counter == 0:
			self.hurted = False

		# game over
		if self.heart <= 0 or self.rect.y > screen.resolution[1]:
			self.alive = False

		# animation
		if self.weaponized:
			self.sprites_right = [ pygame.image.load("./ressources/goodoo_gold/1.png"),
									pygame.image.load("./ressources/goodoo_gold/2.png") ]
			self.sprites_left = [ pygame.image.load("./ressources/goodoo_gold/3.png"),
									pygame.image.load("./ressources/goodoo_gold/4.png") ]
		else:
			self.sprites_right = [ pygame.image.load("./ressources/goodoo_white/1.png"),
									pygame.image.load("./ressources/goodoo_white/2.png") ]
			self.sprites_left = [ pygame.image.load("./ressources/goodoo_white/3.png"),
									pygame.image.load("./ressources/goodoo_white/4.png") ]
		self.animation(self.last_move)


	def display(self, screen):

		#pygame.draw.rect(screen.surface, Globals.RED, self.rect) # hitbox
		if not self.hurted:
			screen.surface.blit(self.sprite, (self.rect.x, self.rect.y) )
		elif self.hurted and Globals.counter % 4 == 0:
			screen.surface.blit(self.sprite, (self.rect.x, self.rect.y) )
		#pygame.draw.rect(screen.surface, Globals.PURPLE, self.blockcollide) # bloc de collision
		screen.surface.blit(self.heart_sprite[self.heart], (0.5 * Globals.RATIO, 0.5 * Globals.RATIO) )

		# frappe
		if self.cooldown_counter == self.COOLDOWN and self.last_move == "right":
			screen.surface.blit(self.hit_sprite_right, (self.rect.x, self.rect.y - Globals.RATIO) )
		elif self.cooldown_counter == self.COOLDOWN and self.last_move == "left":
			screen.surface.blit(self.hit_sprite_left, (self.rect.x - Globals.RATIO, self.rect.y - Globals.RATIO) )
