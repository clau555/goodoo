import pygame
import random
from environnements import *

"""
-- EN COURS
Changelog 5:
	Ajoute des ennemies
"""


#========== INITIALISATION VARIABLES GLOBALES ==========

from mother import Mother

fps = 60 # images/boucles par seconde
ratio = 20 # ratio écran / grille
counter = 0 # compteur de boucle

# COULEURS
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)
green = (0,255,0)
cyan = (0,255,255)
blue = (0,0,255)
purple = (255,0,255)



#========== OBJETS ==========

from screen import Screen



from block import Block



from player import Player



class Enemy():

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


#========== INITIALISATION PYGAME ==========

pygame.init()

# FENETRE
screen = Screen()

# ENVIRONNEMENT


# JOUEUR
player = Player(30.0,20.0)


# ENNEMIES
enemies = []
enemy0 = Enemy(30.0, 25.0)
enemy1 = Enemy(40.0,0.0)
enemy2 = Enemy(40.0,0.0)
enemy3 = Enemy(40.0,0.0)
enemy4 = Enemy(40.0,0.0)

# MUSIQUE
#pygame.mixer.music.load("./ressources/music/S.Rachmaninov - prelude op 23 no 5.wav")


# HORLOGE
clock = pygame.time.Clock()


#========== CORPS DU PROGRAMME ==========

#pygame.mixer.music.play()
launched = True

while launched:


	# EVENTS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			launched = False


	# OUT OF BOUND
	if player.rect.y > screen.resolution[1]:
		launched = False

	keys = pygame.key.get_pressed()


	# CONTROLE TOUCHES FENETRE
	if keys[pygame.K_ESCAPE]:
		launched = False
	if keys[pygame.K_F11] and screen.fullscreen==False:
		screen.surface = pygame.display.set_mode(screen.resolution, pygame.FULLSCREEN)
		pygame.mouse.set_visible(False)
		screen.fullscreen = True
	elif keys[pygame.K_F11] and screen.fullscreen==True:
		screen.surface = pygame.display.set_mode(screen.resolution)
		pygame.mouse.set_visible(True)
		screen.fullscreen = False


	# JOUEUR

	# déplacement gauche
	if keys[pygame.K_LEFT]:
		if not(keys[pygame.K_RIGHT]):
			player.last_move = "left"
		player.move(-player.v_fixed, 0)

	# déplacement droit
	if keys[pygame.K_RIGHT]:
		if not(keys[pygame.K_LEFT]):
			player.last_move = "right"
		player.move(player.v_fixed, 0)

	# saut
	if keys[pygame.K_SPACE] and player.onground and not player.isjump:
		player.isjump = True
		player.vy_index = len(player.vy)//6 # rang de vélocité d'impulsion initiale
	if player.isjump:
		player.jump()

	# gravité
	if not player.isjump:
		player.gravity()


	# ENNEMIE

	for enemy in enemies:

		# déplacement gauche
		if enemy.rect.x > player.rect.x:
			enemy.move(-enemy.v_fixed, 0)

		# déplacement droit
		if enemy.rect.x < player.rect.x:
			enemy.move(enemy.v_fixed, 0)

		# saut
		if enemy.onground and not enemy.isjump:
			enemy.isjump = True
			enemy.vy_index = len(enemy.vy)//6 # rang de vélocité d'impulsion initiale
		if enemy.isjump:
			enemy.jump()

		# gravité
		if not enemy.isjump:
			enemy.gravity()


	# DESSIN DES SURFACES

	screen.surface.fill(black)

	# dessine tout les blocs de la liste blocks
	for block in blocks:
		pygame.draw.rect(screen.surface, white, block.rect)

	# dessine le joueur
	#pygame.draw.rect(screen.surface, purple, player.blockcollide) # bloc de collision
	#pygame.draw.rect(screen.surface, red, player.rect) # hitbox
	player.animation(player.last_move)
	screen.surface.blit(player.sprite, (player.rect.x, player.rect.y) )

	# dessine les ennemis
	for enemy in enemies:
		#pygame.draw.rect(screen.surface, red, enemy.rect)
		enemy.animation()
		screen.surface.blit(enemy.sprite, (enemy.rect.x, enemy.rect.y) )

	pygame.display.flip() # actualisation de l'écran


	counter += 1
	clock.tick(fps)


pygame.quit()