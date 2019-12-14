import pygame


# ============================== OBJETS ==============================

from gl0bals import *
from classes.screen import *


# ==================================================================================================================================

def over_initialize():

	global FONT, TITLE_FONT, clock, selection, big_buttons

	# ============================== INITIALISATION ==============================

	# ========== TEXTE

	pygame.font.init()
	FONT = pygame.font.Font("./ressources/FFFFORWA.TTF", 15)
	TITLE_FONT = pygame.font.Font("./ressources/FFFFORWA.TTF", 40)


	# ========== HORLOGE

	clock = pygame.time.Clock()

	# ========== MENU

	selection = 1


# ==================================================================================================================================

def over_body(screen):

	global selection


	# ======================================== EVENTS

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			Globals.launched = False

		elif event.type == pygame.KEYDOWN:

			# selection

			if event.key == pygame.K_DOWN:
				selection += 1

			elif event.key == pygame.K_UP:
				selection -= 1

			# activation de la selection
			elif event.key == pygame.K_RETURN:
				# retour arrière
				if selection == 0:
					Globals.ecran = "select"
				# lancement d'un niveau
				elif selection == 1:
					Globals.ecran = "game"

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

	# ======================================== SELECTION

	if selection > 1:
		selection = 1
	elif selection < 0:
		selection = 0

# ==================================================================================================================================

def over_display(screen):

	global FONT, TITLE_FONT, clock, selection

	# ======================================== DESSIN DES SURFACES

	# fond
	screen.surface.fill(Globals.BLACK)

	# titre
	title = TITLE_FONT.render("GAME OVER", False, Globals.RED)
	screen.surface.blit(title, (1*Globals.RATIO, 1*Globals.RATIO) )

	# retour arrière
	if selection == 0:
		back_button = FONT.render("MENU <-", False, Globals.RED)
		retry_button = FONT.render("RETRY", False, Globals.WHITE)
	elif selection == 1:
		back_button = FONT.render("MENU", False, Globals.WHITE)
		retry_button = FONT.render("RETRY <-", False, Globals.WHITE)

	screen.surface.blit(back_button, (4*Globals.RATIO, 6*Globals.RATIO) )
	screen.surface.blit(retry_button, (4*Globals.RATIO, 8*Globals.RATIO) )

	# actualisation de l'écran
	pygame.display.flip()

	
	# ========== MISE A JOUR

	Globals.counter += 1
	clock.tick(Globals.FPS)