import pygame
from environnements import *
from globals import *

"""
-- EN COURS
Changelog 5:
	Ajoute des ennemies
"""

#========== OBJETS ==========

from screen import Screen



from block import Block



from player import Player



from enemys import Enemy


#========== INITIALISATION PYGAME ==========

pygame.init()

# FENETRE
screen = Screen()

# ENVIRONNEMENT

# créer tout les blocs de l'environnement
for i in range(0,len(tab)):
	for j in range(0,len(tab[0])):
		if tab[i][j]==1:
			blocks.append( Block( (j*ratio , i*ratio) ) ) # est ajouté à la liste de tout les blocs

# JOUEUR

player = Player(30.0,20.0)


# ENNEMIES

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