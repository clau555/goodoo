"""
-- EN COURS
Changelog 5:
	Répartition des classes en fichiers
	Ajout des ennemies
"""

import pygame
import random


#========== OBJETS ==========

from gl0bals import *
from environnements import *
from screen import *
from block import *
from entity import *
from player import *
from enemy1 import *
from enemy2 import *


#========== INITIALISATION PYGAME ==========

pygame.init()

# FENETRE
screen = Screen()

# ENVIRONNEMENT
TAB = Environnements.TAB5 # tableau de 1 et 0 du niveau, cf envirronements.py
# créer tout les blocs de l'environnement
for i in range(0,len(TAB)):
	for j in range(0,len(TAB[0])):
		if TAB[i][j]==1:
			# est ajouté à la liste de tout les blocs
			Globals.blocks.append( Block( (j * Globals.RATIO , i * Globals.RATIO) ) )

# JOUEUR
player = Player(30.0,20.0)

# ENNEMIES
enemy0 = Enemy1(30.0, 25.0)
enemy1 = Enemy1(40.0, 0.0)
enemy2 = Enemy1(42.0, 0.0)
enemy3 = Enemy1(43.0, 0.0)
enemy4 = Enemy1(45.0, 0.0)
enemy5 = Enemy2(25.0, 0.0)

# MUSIQUE
#pygame.mixer.music.load("./ressources/music/S.Rachmaninov - prelude op 23 no 5.wav")


# HORLOGE
clock = pygame.time.Clock()


#========== CORPS DU PROGRAMME ==========

#pygame.mixer.music.play()
launched = True

while launched:


	# ========== EVENTS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			launched = False


	# ========== OUT OF BOUND
	if player.rect.y > screen.resolution[1]:
		launched = False


	keys = pygame.key.get_pressed()

	# ========== CONTROLE TOUCHES FENETRE
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


	# ========== JOUEUR

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


	# ========== ENNEMIES 1

	for enemy in Globals.enemies1:

		# déplacement gauche
		if enemy.rect.x > player.rect.x:
			enemy.move(-enemy.v_fixed, 0)

		# déplacement droit
		if enemy.rect.x < player.rect.x:
			enemy.move(enemy.v_fixed, 0)

		# saut
		if enemy.onground and not enemy.isjump:
			enemy.isjump = True
			enemy.vy_index = len(enemy.vy)//random.randint(3,6) # rang de vélocité d'impulsion initiale
		if enemy.isjump:
			enemy.jump()

		# gravité
		if not enemy.isjump:
			enemy.gravity()

	# ========== ENNEMIES 2

	for enemy in Globals.enemies2:

		# déplacement gauche
		if enemy.rect.x > player.rect.x:
			enemy.last_move = "left"
			enemy.move(-enemy.v_fixed, 0)

		# déplacement droit
		if enemy.rect.x < player.rect.x:
			enemy.last_move = "right"
			enemy.move(enemy.v_fixed, 0)

		# gravité
		if not enemy.isjump:
			enemy.gravity()

	# ========== ENNEMIES 3

	# vide


	# ========== DESSIN DES SURFACES

	# fond
	screen.surface.fill(Globals.BLACK)

	# blocs du décor
	for block in Globals.blocks:
		pygame.draw.rect(screen.surface, Globals.WHITE, block.rect)

	# ennemis type 1
	for enemy in Globals.enemies1:
		enemy.animation("right")
		screen.surface.blit(enemy.sprite, (enemy.rect.x, enemy.rect.y) )
		#pygame.draw.rect(screen.surface, Globals.RED, enemy.rect) # hitbox

	# ennemis type 2
	for enemy in Globals.enemies2:
		enemy.animation(enemy.last_move)
		screen.surface.blit(enemy.sprite, (enemy.rect.x, enemy.rect.y) )
		#pygame.draw.rect(screen.surface, Globals.RED, enemy.rect) # hitbox

	# joueur
	player.animation(player.last_move)
	screen.surface.blit(player.sprite, (player.rect.x, player.rect.y) )
	#pygame.draw.rect(screen.surface, Globals.PURPLE, player.blockcollide) # bloc de collision
	#pygame.draw.rect(screen.surface, Globals.RED, player.rect) # hitbox

	# actualisation de l'écran
	pygame.display.flip()


	# ========== MISE A JOUR

	Globals.counter += 1
	clock.tick(Globals.FPS)


pygame.quit()