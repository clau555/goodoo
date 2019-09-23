#codin:utf-8
import pygame
import time

pygame.init()

"""
Changelog :
	Fenêtre de 1000x600px
	Plein écran (curseur caché) sur F11
	Quitter sur Echap
	Joueur dirigé par touches directionelles
	Joueur animé selon boucle et direction
	Joueur stoppé par bords de la fenêtre
"""


"""############INITIALISATIONS VARIBALES############"""

#écran
screen_width = 1000
screen_height = 600
screen_resolution = (screen_width, screen_height)
fullscreen = False

#joueur
x = 460 #coords x
y = 260 #coords y
player_width = 40 #longueur du côté
velocity = 5 #vélocité
animation_counter = 0 #compteur animation
left = False
right = False

#autre
white = (255,255,255)
black = (0,0,0)
counter = 0 #compteur de boucle de rafraichissement

clock = pygame.time.Clock() #ne sert à rien pour l'instant


"""############INITIALISATIONS SURFACES############"""

#FENETRE
pygame.display.set_caption("Goodoo")
screen = pygame.display.set_mode(screen_resolution)
icon = pygame.image.load("goodoo1.png")
pygame.display.set_icon(icon)

#JOUEUR
player_right = (pygame.image.load("goodoo1.png"), pygame.image.load("goodoo2.png"))
player_left = (pygame.image.load("goodoo3.png"), pygame.image.load("goodoo4.png"))
screen.blit(player_right[0],(500,100))


#ENVIRONNEMENT

#néant

#PREMIERE ACTUALISATION
pygame.display.flip()

"""############FONCTIONS############"""

def player_animation():

	global animation_counter

	if counter%30 == 0: #toute les 30 images
		animation_counter += 1

	if animation_counter == 2:
		animation_counter = 0

	if right :
		screen.blit(player_right[animation_counter],(x,y))

	elif left :
		screen.blit(player_left[animation_counter],(x,y))

	else:
		screen.blit(player_right[animation_counter],(x,y))


def screen_keys():

	global launched, fullscreen, screen

	if keys[pygame.K_ESCAPE]:
		launched = False

	
	if keys[pygame.K_F11] and fullscreen==False:
		screen = pygame.display.set_mode(screen_resolution, pygame.FULLSCREEN)
		pygame.mouse.set_visible(False)
		fullscreen = True

	elif keys[pygame.K_F11] and fullscreen==True:
		screen = pygame.display.set_mode(screen_resolution)
		pygame.mouse.set_visible(True)
		fullscreen = False


def player_keys():

	global x, y, right, left

	if keys[pygame.K_LEFT] and x >= velocity:
		left = True
		right = False
		x -= velocity

	if keys[pygame.K_RIGHT] and x < screen_width - player_width:
		right = True
		left = False
		x += velocity

	if keys[pygame.K_UP] and y >= velocity:
		y -= velocity

	if keys[pygame.K_DOWN] and y < screen_height - player_width:
		y += velocity


"""############CORPS############"""

launched = True

while launched:

	#EVENTS

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			launched = False

	#CONTROLE DES TOUCHES

	keys = pygame.key.get_pressed()
	screen_keys()
	player_keys()

	#ACTUALISATION VARIABLES

	counter += 1

	#ACTUALISATION SURFACES

	screen.fill(black)
	player_animation()
	pygame.display.flip() #rafraichit l'écran
	time.sleep(.016) #60 fps

pygame.quit()
