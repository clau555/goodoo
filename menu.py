import pygame


# ============================== OBJETS ==============================

from gl0bals import *
from classes.screen import *


# ==================================================================================================================================

def menu_initialize():

	global FONT, TITLE_FONT, clock, selection

	# ============================== INITIALISATION ==============================

	# ========== TEXTE

	pygame.font.init()
	FONT = pygame.font.Font("./ressources/FFFFORWA.TTF", 15)
	TITLE_FONT = pygame.font.Font("./ressources/FFFFORWA.TTF", 40)


	# ========== MUSIQUE / SON

	#pygame.mixer.music.load("./ressources/music/S.Rachmaninov - prelude op 23 no 5.wav")
	#sound_pickup = pygame.mixer.Sound("./ressources/sounds/pickup.wav")
	pygame.mixer.init()
	#pygame.mixer.music.play()


	# ========== HORLOGE

	clock = pygame.time.Clock()

	# ========== MENU
	selection = 0


# ==================================================================================================================================

def menu_body(screen):

	global selection


	# ======================================== EVENTS

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			Globals.launched = False

		elif event.type == pygame.KEYDOWN:
			# selection vers le bas
			if event.key == pygame.K_DOWN:
				selection += 1
			# selection vers le haut
			elif event.key == pygame.K_UP:
				selection -= 1
			# activation de la selection
			elif event.key == pygame.K_RETURN:
				if selection == 0:
					Globals.ecran = "select"
				elif selection == 1:
					Globals.ecran = "guide"
				elif selection == 2:
					Globals.launched = False

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

	if selection > 2:
		selection = 0
	elif selection < 0:
		selection = 2

# ==================================================================================================================================

def menu_display(screen):

	global FONT, TITLE_FONT, clock, selection

	# ======================================== DESSIN DES SURFACES

	# fond
	screen.surface.fill(Globals.BLACK)

	# titre
	title = TITLE_FONT.render("GOODOO", False, Globals.WHITE)
	screen.surface.blit(title, (2*Globals.RATIO, 2*Globals.RATIO) )

	# start
	if selection == 0:
		play_button = FONT.render("PLAY <-", False, Globals.WHITE)
	else:
		play_button = FONT.render("PLAY", False, Globals.WHITE)
	screen.surface.blit(play_button, (2*Globals.RATIO, 6*Globals.RATIO) )

	# rules
	if selection == 1:
		rules_button = FONT.render("GUIDE <-", False, Globals.WHITE)
	else:
		rules_button = FONT.render("GUIDE", False, Globals.WHITE)
	screen.surface.blit(rules_button, (2*Globals.RATIO, 7.5*Globals.RATIO) )

	# quit
	if selection == 2:
		quit_button = FONT.render("QUIT <-", False, Globals.WHITE)
	else:
		quit_button = FONT.render("QUIT", False, Globals.WHITE)
	screen.surface.blit(quit_button, (2*Globals.RATIO, 9*Globals.RATIO) )


	# actualisation de l'écran
	pygame.display.flip()

	
	# ========== MISE A JOUR

	Globals.counter += 1
	clock.tick(Globals.FPS)