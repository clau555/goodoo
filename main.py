"""
-- EN COURS
Changelog 5:
	Répartition des classes en fichiers
	Ennemies 1 et 2
	Projectiles
	Vagues
	Arme
	Frappe du joueur
"""

import pygame
import random


# ========== OBJETS ==========

from gl0bals import *
from levels import *
from screen import *
from block import *
from entity import *
from player import *
from enemy1 import *
from enemy2 import *
from weapon import *
from projectile import *

# ========== INITIALISATION ==========

pygame.init()

# FENETRE
screen = Screen()

# NIVEAU
TAB = Levels.TAB5 # tableau de 1 et 0 du niveau, cf envirronements.py
# créer tout les blocs de l'environnement
for i in range(0,len(TAB)):
	for j in range(0,len(TAB[0])):
		if TAB[i][j]==1:
			# est ajouté à la liste de tout les blocs
			Globals.blocks.append( Block( (j * Globals.RATIO , i * Globals.RATIO) ) )

# VAGUES
def Wave1():

	global player, weapon

	# JOUEUR
	player = Player(19.0, 17.0)

	# ENNEMIES
	Enemy1(16.0, 33.0)
	Enemy1(18.0, 33.0)
	Enemy1(20.0, 33.0)
	Enemy1(22.0, 33.0)
	Enemy1(24.0, 33.0)
	Enemy2(35.0, 32.0)

	# ARME
	weapon = Weapon(44.0, 16.0)

def Wave2():

	global player, weapon

	# JOUEUR
	player.weaponized = False
	player.sprites_right = [ pygame.image.load("./ressources/goodoo_white/1.png"),
							pygame.image.load("./ressources/goodoo_white/2.png") ]
	player.sprites_left = [ pygame.image.load("./ressources/goodoo_white/3.png"),
							pygame.image.load("./ressources/goodoo_white/4.png") ]

	# ENNEMIES
	Enemy2(20.0, 32.0)
	Enemy2(24.0, 32.0)
	Enemy2(28.0, 32.0)
	Enemy2(32.0, 32.0)
	Enemy2(36.0, 32.0)
	Enemy2(40.0, 32.0)

	# ARME
	weapon = Weapon(19.0, 16.0)

def Wave3():

	global player, weapon

	# JOUEUR
	player.weaponized = False
	player.sprites_right = [ pygame.image.load("./ressources/goodoo_white/1.png"),
							pygame.image.load("./ressources/goodoo_white/2.png") ]
	player.sprites_left = [ pygame.image.load("./ressources/goodoo_white/3.png"),
							pygame.image.load("./ressources/goodoo_white/4.png") ]

	# ENNEMIES
	Enemy2(37.0, 5.0)
	Enemy2(42.0, 32.0)
	Enemy2(28.0, 32.0)
	Enemy2(32.0, 32.0)
	Enemy2(46.0, 3.0)
	Enemy2(11.0, 1.0)

	# ARME
	weapon = Weapon(47.0, 3.0)

# MUSIQUE
#pygame.mixer.music.load("./ressources/music/S.Rachmaninov - prelude op 23 no 5.wav")

# HORLOGE
clock = pygame.time.Clock()


# ========== CORPS ==========

#pygame.mixer.music.play()
over = False
launched = True
wave = 1
Wave1()

while launched:


	# ========== EVENTS

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			launched = False
	

	keys = pygame.key.get_pressed()

	# ========== FENETRE

	# quitter
	if keys[pygame.K_ESCAPE]:
		launched = False

	# plein écran
	if keys[pygame.K_F11] and screen.fullscreen==False:
		screen.surface = pygame.display.set_mode(screen.resolution, pygame.FULLSCREEN)
		pygame.mouse.set_visible(False)
		screen.fullscreen = True
	elif keys[pygame.K_F11] and screen.fullscreen==True:
		screen.surface = pygame.display.set_mode(screen.resolution)
		pygame.mouse.set_visible(True)
		screen.fullscreen = False


	# ========== ENNEMIES (GLOBAL)

	for enemy in Globals.enemies:
		if enemy.killed:
			del Globals.enemies[Globals.enemies.index(enemy)]


	# ========== VAGUES

	if wave == 1 and Globals.enemies == []:
		wave = 2
		Wave2()
	elif wave == 2 and Globals.enemies == []:
		wave = 3
		Wave3()


	# ========== ENNEMIES 1

	for enemy in Globals.enemies1:

		# déplacement gauche
		if enemy.rect.x > player.rect.x:
			enemy.move(-random.uniform(0.05, 0.2), 0) # vitesse aléatoire

		# déplacement droit
		if enemy.rect.x < player.rect.x:
			enemy.move(random.uniform(0.05, 0.2), 0) # vitesse aléatoire

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
		if Globals.counter%480 <= 120:
			enemy.last_move = "left"
			enemy.move(-enemy.v_fixed, 0)

		# déplacement droit
		if 240 < Globals.counter%480 <= 360 :
			enemy.last_move = "right"
			enemy.move(enemy.v_fixed, 0)

		# gravité
		if not enemy.isjump:
			enemy.gravity()

		# tir
		if Globals.counter%180 == 0 and not enemy.killed:
			Projectile(enemy.rect.x, enemy.rect.y, player.rect.x + 0.5*Globals.RATIO, player.rect.y + 1.0*Globals.RATIO)


	#=========== PROJECTILES

	for projectile in Globals.projectiles:
		projectile.move_single_axis()
		projectile.animation()
		if projectile.rect.x > screen.resolution[0] or projectile.rect.x < 0 or projectile.rect.y < 0 or projectile.rect.y > screen.resolution[1]:
			del Globals.projectiles[Globals.projectiles.index(projectile)]


	# ========== JOUEUR

	# out of bound
	if player.rect.y > screen.resolution[1]:
		launched = False

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

	# taper
	if player.weaponized and keys[pygame.K_x] and player.cooldown == 0:
		player.hit()
		player.cooldown = player.COOLDOWN + 1
	if player.cooldown != 0:
		player.cooldown -= 1


	# ========== ARME

	if player.rect.colliderect(weapon.rect) and not player.weaponized:
		player.weaponized = True
		player.sprites_right = [ pygame.image.load("./ressources/goodoo_gold/1.png"),
								pygame.image.load("./ressources/goodoo_gold/2.png") ]
		player.sprites_left = [ pygame.image.load("./ressources/goodoo_gold/3.png"),
								pygame.image.load("./ressources/goodoo_gold/4.png") ]


	# ========== GAME OVER

	for enemy in Globals.enemies:
		if player.rect.colliderect(enemy.rect):
			over = True


	# ========== DESSIN DES SURFACES

	# fond
	screen.surface.fill(Globals.BLACK)


	# blocs
	for block in Globals.blocks:
		pygame.draw.rect(screen.surface, Globals.WHITE, block.rect)
		#screen.surface.blit(block.sprite, (block.rect.x, block.rect.y) )


	# ennemis
	for enemy in Globals.enemies:
		if not enemy.killed :
			enemy.animation(enemy.last_move)
			screen.surface.blit(enemy.sprite, (enemy.rect.x, enemy.rect.y) )
			#pygame.draw.rect(screen.surface, Globals.RED, enemy.rect) # hitbox


	# arme
	if not player.weaponized:
		screen.surface.blit(weapon.sprite, (weapon.rect.x, weapon.rect.y) )
		#pygame.draw.rect(screen.surface, Globals.YELLOW, weapon.rect) # hitbox


	# joueur
	player.animation(player.last_move)
	screen.surface.blit(player.sprite, (player.rect.x, player.rect.y) )
	#pygame.draw.rect(screen.surface, Globals.PURPLE, player.blockcollide) # bloc de collision
	#pygame.draw.rect(screen.surface, Globals.RED, player.rect) # hitbox

	if player.cooldown == player.COOLDOWN and player.last_move == "right":
		screen.surface.blit(player.hit_sprite_right, (player.rect.x, player.rect.y - Globals.RATIO) )

	elif player.cooldown == player.COOLDOWN and player.last_move == "left":
		screen.surface.blit(player.hit_sprite_left, (player.rect.x - Globals.RATIO, player.rect.y - Globals.RATIO) )

	#projectiles
	for projectile in Globals.projectiles:
		#pygame.draw.rect(screen.surface, Globals.RED, projectile.rect) # hitbox
		screen.surface.blit(projectile.sprite, (projectile.rect.x, projectile.rect.y) )


	# actualisation de l'écran
	pygame.display.flip()


	# ========== MISE A JOUR

	Globals.counter += 1
	clock.tick(Globals.FPS)


pygame.quit()