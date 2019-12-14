import pygame


# ============================== OBJETS ==============================

from gl0bals import *
from classes.screen import *


# ==================================================================================================================================

def victory_initialize():

	global FONT, TITLE_FONT, clock

	# ============================== INITIALISATION ==============================

	# ========== TEXTE

	pygame.font.init()
	FONT = pygame.font.Font("./ressources/FFFFORWA.TTF", 15)
	TITLE_FONT = pygame.font.Font("./ressources/FFFFORWA.TTF", 40)


	# ========== HORLOGE

	clock = pygame.time.Clock()


# ==================================================================================================================================

def victory_body(screen):


	# ======================================== EVENTS

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			Globals.launched = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				Globals.ecran = "select"

	keys = pygame.key.get_pressed()

	# ======================================== FENETRE

	# quitter
	if keys[pygame.K_ESCAPE]:
		Globals.launched = False

	# plein écran
	if keys[pygame.K_F11] and screen.fullscreen==False:
		screen.surface = pygame.display.set_mode(screen.resolution, pygame.FULLSCREEN)
		pygame.mouse.set_visible(False)
		screen.fullscreen = True
	elif keys[pygame.K_F11] and screen.fullscreen==True:
		screen.surface = pygame.display.set_mode(screen.resolution)
		pygame.mouse.set_visible(True)
		screen.fullscreen = False


# ==================================================================================================================================

def victory_display(screen):

	global FONT, TITLE_FONT, clock

	# ======================================== DESSIN DES SURFACES

	# fond
	screen.surface.fill(Globals.BLACK)

	# titre
	title = TITLE_FONT.render("VICTORY", False, Globals.WHITE)
	screen.surface.blit(title, (1*Globals.RATIO, 1*Globals.RATIO) )

	# retour arrière
	back_button = FONT.render("MENU <-", False, Globals.WHITE)

	screen.surface.blit(back_button, (4*Globals.RATIO, 6*Globals.RATIO) )

	# actualisation de l'écran
	pygame.display.flip()

	
	# ========== MISE A JOUR

	Globals.counter += 1
	clock.tick(Globals.FPS)