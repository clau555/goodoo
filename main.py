"""
-- EN COURS
Changelog 6:
	Corrections diverses
	Amélioration IA
	Ennemies 3 et 4?
	Transition vagues
	Niveaux 1, 2 et 3
	Menu et sélections niveau
"""

import pygame
import random


# ============================== OBJETS ==============================

from gl0bals import *
from levels import *
from screen import *
from block import *
from entity import *
from player import *
from enemy1 import *
from enemy2 import *
from enemy3 import *
from weapon import *
from projectile import *

# ============================== INITIALISATION ==============================

pygame.init()


# ========== FENETRE

screen = Screen()


# ========== NIVEAU

# selection du niveau
if Globals.level == 0:
	from level0 import *
	level = Level0()
elif Globals.level == 2: # /!\ n'existe pas
	from level2 import *
	level = Level2()
elif Globals.level == 3: # /!\ n'existe pas
	from level3 import *
	level = Level3()

TAB = level.TAB # tableau de 1 et 0 du niveau
player = level.player # initialisation du joueur
weapon = level.weapon # initialisation de l'arme

# créer tout les blocs de l'environnement
for i in range(0,len(TAB)):
	for j in range(0,len(TAB[0])):
		if TAB[i][j]==1:
			# est ajouté à la liste de tout les blocs
			Globals.blocks.append( Block( (j * Globals.RATIO , i * Globals.RATIO) ) )


# ========== TEXTE

pygame.font.init()
FONT = pygame.font.SysFont("", 30)


# ========== MUSIQUE

#pygame.mixer.music.load("./ressources/music/S.Rachmaninov - prelude op 23 no 5.wav")


# ========== HORLOGE

clock = pygame.time.Clock()


# ============================== CORPS ==============================

#pygame.mixer.music.play()
over = False
launched = True
wave = 1

# première vague
level.Wave1()
player = level.player
weapon = level.weapon

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


	# ========== VAGUES

	if wave == 1 and Globals.enemies == []:
		wave = 2
		level.Wave2()
		player = level.player
		weapon = level.weapon

	elif wave == 2 and Globals.enemies == []:
		wave = 3
		level.Wave3()
		player = level.player
		weapon = level.weapon


	# ========== ENNEMIES (GLOBAL)

	for enemy in Globals.enemies:

		if player.rect.colliderect(enemy.rect):
			over = True

		if enemy.killed or enemy.rect.top > screen.resolution[1]:

			del Globals.enemies[Globals.enemies.index(enemy)]

			if enemy in Globals.enemies1:
				del Globals.enemies1[Globals.enemies1.index(enemy)]

			elif enemy in Globals.enemies2:
				del Globals.enemies2[Globals.enemies2.index(enemy)]

			elif enemy in Globals.enemies3:
				del Globals.enemies3[Globals.enemies3.index(enemy)]


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
			Projectile(enemy.rect.x, enemy.rect.y, player.rect.x, player.rect.y + 1.0*Globals.RATIO)


	#=========== PROJECTILES

	for projectile in Globals.projectiles:
		projectile.move_single_axis()
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

	# changement d'apparence du joueur
	if player.rect.colliderect(weapon.rect) and not player.weaponized:
		player.weaponized = True
		player.sprites_right = [ pygame.image.load("./ressources/goodoo_gold/1.png"),
								pygame.image.load("./ressources/goodoo_gold/2.png") ]
		player.sprites_left = [ pygame.image.load("./ressources/goodoo_gold/3.png"),
								pygame.image.load("./ressources/goodoo_gold/4.png") ]


	# ========== DESSIN DES SURFACES

	# fond
	screen.surface.fill(Globals.BLACK)
	#screen.surface.blit(screen.sprite, (0,0)) # /!\ Chute de fps


	# blocs
	for block in Globals.blocks:
		pygame.draw.rect(screen.surface, Globals.WHITE, block.rect) # hitbox
		#screen.surface.blit(block.sprite, (block.rect.x, block.rect.y) )


	# ennemis
	for enemy in Globals.enemies:
		if not enemy.killed :
			enemy.animation(enemy.last_move)
			#pygame.draw.rect(screen.surface, Globals.RED, enemy.rect) # hitbox
			screen.surface.blit(enemy.sprite, (enemy.rect.x, enemy.rect.y) )


	# arme
	if not player.weaponized:
		#pygame.draw.rect(screen.surface, Globals.YELLOW, weapon.rect) # hitbox
		screen.surface.blit(weapon.sprite, (weapon.rect.x, weapon.rect.y) )


	# joueur
	player.animation(player.last_move)
	#pygame.draw.rect(screen.surface, Globals.RED, player.rect) # hitbox
	screen.surface.blit(player.sprite, (player.rect.x, player.rect.y) )
	#pygame.draw.rect(screen.surface, Globals.PURPLE, player.blockcollide) # bloc de collision


	# arme
	if player.cooldown == player.COOLDOWN and player.last_move == "right":
		screen.surface.blit(player.hit_sprite_right, (player.rect.x, player.rect.y - Globals.RATIO) )
	elif player.cooldown == player.COOLDOWN and player.last_move == "left":
		screen.surface.blit(player.hit_sprite_left, (player.rect.x - Globals.RATIO, player.rect.y - Globals.RATIO) )


	#projectiles
	for projectile in Globals.projectiles:
		projectile.animation()
		#pygame.draw.rect(screen.surface, Globals.RED, projectile.rect) # hitbox
		screen.surface.blit(projectile.sprite, (projectile.rect.x, projectile.rect.y) )

	#texte
	fps_text = FONT.render(f"{ int(clock.get_fps()) } FPS", False, Globals.RED)
	screen.surface.blit(fps_text, (0, 0) )


	# actualisation de l'écran
	pygame.display.flip()


	# ========== MISE A JOUR

	Globals.counter += 1
	clock.tick(Globals.FPS)


pygame.quit()