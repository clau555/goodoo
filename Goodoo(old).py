#codin:utf-8
import pygame
from environnements import *

pygame.init()

"""
Changelog 2:
	Fenêtre de 1280x720px
	Environnement en grille 64x36 blocs
	1 bloc = 20 px
	Grille de 64x36 blocs
	Nouvelle taille du joueur (1 bloc)
"""

"""############INITIALISATIONS VARIBALES############"""

#ECRAN
screen_width = 1280
screen_height = 720
screen_resolution = (screen_width, screen_height)
fullscreen = False

#GRILLE
x_len = 64
y_len = 36
ratio = 20				#(ratio écran/grille)

#JOUEUR
x = 45.0				#coords x
y = 17.0				#coords y
player_width = 1		#longueur d'un côté
velocity = 0.2			#vélocité (0.2 bloc/f = 4px/f)
animation_counter = 0	#compteur animation
left = False
right = False

#COULEURS
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

#TEXTE
consolas_font = pygame.font.SysFont("consolas",20)

#AUTRE
counter = 0 #compteur de boucle de rafraichissement

clock = pygame.time.Clock()


"""############INITIALISATIONS SURFACES############"""

#FENETRE
pygame.display.set_caption("Goodoo")
screen = pygame.display.set_mode(screen_resolution)
icon = pygame.image.load("./img/icon.jpg")
pygame.display.set_icon(icon)

#JOUEUR
player_right = (pygame.image.load("img/goodoo_white/goodoo1.png"), pygame.image.load("img/goodoo_white/goodoo2.png"))
player_left = (pygame.image.load("img/goodoo_white/goodoo3.png"), pygame.image.load("img/goodoo_white/goodoo4.png"))
screen.blit(player_right[0],(x,y))

player_rect = pygame.Rect((x*ratio,y*ratio), (player_width*ratio,player_width*ratio))


#ENVIRONNEMENT
tab = tab0
block = pygame.Surface((20, 20))
block.fill(white)
environnement = pygame.image.load("tab0.png")
screen.blit(environnement,(0,0))

#PREMIERE ACTUALISATION
pygame.display.flip()


"""############FONCTIONS###########"""

def screen_keys():
	"""
	Ferme la fenêtre sur echap.
	Met en plein écran sur F11.
	"""

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


def tab_draw(tab):
	"""
	Dessine les rectangles du niveau selon un tableau de 0 et 1.
	"""

	for i in range(0,y_len):
		for j in range(0,x_len):
			if tab[i][j]==1:
				screen.blit(block,(j*ratio,i*ratio))


def player_keys():
	"""
	Incrémente les coordonées du joueur en fonction des touches pressées.
	"""

	global x, y, right, left

	if keys[pygame.K_LEFT] and x > 0:
		left = True
		right = False
		x -= velocity

	if keys[pygame.K_RIGHT] and x < x_len - player_width:
		right = True
		left = False
		x += velocity

	if keys[pygame.K_UP] and y >= velocity:
		y -= velocity

	if keys[pygame.K_DOWN] and y < y_len - player_width:
		y += velocity


def neighbour_blocks(tab, x, y):
	"""
	Renvoie une liste des blocs voisins au joueur.
	"""

	blocks = list()

	for j in range(int(y+player_width//2)-1, int(y+player_width//2)+2, 1):
		for i in range(int(x+player_width//2)-1, int(x+player_width//2)+2, 1):

			if j < y_len and i < x_len:		#on vérifie que j et i ne soient pas en dehors de la grille
				if tab[j][i] == 1:
					topleft = i*ratio, j*ratio

					pygame.draw.rect(screen, red, pygame.Rect((topleft), (ratio,ratio)))

					blocks.append(pygame.Rect((topleft), (ratio,ratio)))

	return blocks


def player_collision(tab, x, y):
	"""
	Booléen vrai si le joueur touche un bloc plein.
	"""

	for block in neighbour_blocks(tab, x, y):
		if player_rect.colliderect(block):
			return True
	return False


def player_animation():

	global animation_counter

	if counter%30 == 0: #toute les 30 images
		animation_counter += 1

	if animation_counter == 2:
		animation_counter = 0

	if right :
		screen.blit(player_right[animation_counter],(x*ratio,y*ratio))

	elif left :
		screen.blit(player_left[animation_counter],(x*ratio,y*ratio))

	else:
		screen.blit(player_right[animation_counter],(x*ratio,y*ratio))


"""############CORPS############"""

launched = True

while launched:

	#EVENTS

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			launched = False

	#ACTUALISATION VARIABLES
	counter += 1

	x_old = x
	y_old = y


	#CONTROLE DES TOUCHES
	keys = pygame.key.get_pressed()
	screen_keys()

	player_keys()
	player_rect.x = x*ratio
	player_rect.y = y*ratio


	#TEXTE POUR DEV
	coord = "x : {x} y : {y}".format(x=int(x), y=int(y))
	text = consolas_font.render(coord, True, red)


	#ACTUALISATION SURFACES
	screen.fill(black)
	tab_draw(tab)
	neighbour_blocks(tab, x, y)
	player_collision(tab, x, y)

	player_animation()
	#pygame.draw.rect(screen, red, player_rect)		#actif pour voir hitbox

	screen.blit(text, (10,550))


	pygame.display.flip() #rafraichit l'écran

	clock.tick(60) #60 fps

pygame.quit()
