import pygame


# ============================== OBJETS ==============================

from gl0bals import *
from classes.screen import *


# ==================================================================================================================================

def guide_initialize():

	global FONT, TITLE_FONT, clock

	# ============================== INITIALISATION ==============================

	# ========== TEXTE

	pygame.font.init()
	FONT = pygame.font.Font("./ressources/FFFFORWA.TTF", 15)
	TITLE_FONT = pygame.font.Font("./ressources/FFFFORWA.TTF", 40)

	# ========== HORLOGE

	clock = pygame.time.Clock()


# ==================================================================================================================================

def guide_body(screen):

	global FONT, TITLE_FONT, clock

	# ======================================== EVENTS

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			Globals.launched = False

		elif event.type == pygame.KEYDOWN:
			# activation de la selection
			if event.key == pygame.K_RETURN:
				Globals.ecran = "menu"
				
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

def guide_display(screen):

	global FONT, TITLE_FONT, clock

	# ======================================== DESSIN DES SURFACES

	# fond
	screen.surface.blit(screen.guide, (0,0))

	# titre
	title = TITLE_FONT.render("GUIDE", False, Globals.WHITE)
	screen.surface.blit(title, (1*Globals.RATIO, 1*Globals.RATIO) )

	# retour arrière
	back_button = FONT.render("BACK <-", False, Globals.WHITE)
	screen.surface.blit(back_button, (1*Globals.RATIO, 4*Globals.RATIO) )


	# actualisation de l'écran
	pygame.display.flip()

	
	# ========== MISE A JOUR

	Globals.counter += 1
	clock.tick(Globals.FPS)