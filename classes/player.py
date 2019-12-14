import pygame
from gl0bals import *
from classes.entity import *
from classes.block import *
from classes.popup import *


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

		self.weaponized = False # vrai si possède l'arme (weapon)
		self.hit_rect = None # zone de dégât d'une frappe
		self.hit_sprite_right = pygame.image.load("./ressources/hit/1.png")
		self.hit_sprite_left = pygame.image.load("./ressources/hit/2.png")

		self.COOLDOWN = 10 # temps de recharge d'une frappe
		self.cooldown_counter = 0

		self.HEART = 5 # barre de vie
		self.heart = self.HEART
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
				enemy.killed = True