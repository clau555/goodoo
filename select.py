import pygame


# ============================== OBJETS ==============================

from gl0bals import *
from classes.screen import *
from classes.big_button import *


# ==================================================================================================================================

def select_initialize():

	global FONT, TITLE_FONT, clock, selection, big_buttons, levels_titles

	# ============================== INITIALISATION ==============================

	# ========== TEXTE

	pygame.font.init()
	FONT = pygame.font.Font("./ressources/FFFFORWA.TTF", 15)
	TITLE_FONT = pygame.font.Font("./ressources/FFFFORWA.TTF", 40)


	# ========== HORLOGE

	clock = pygame.time.Clock()

	# ========== MENU
	
	big_button1 = Big_button(8, 10, pygame.image.load("./ressources/levels_img/tab1.jpg"))
	big_button2 = Big_button(26, 10, pygame.image.load("./ressources/levels_img/tab2.jpg"))
	big_button3 = Big_button(44, 10, pygame.image.load("./ressources/levels_img/tab3.jpg"))
	big_button4 = Big_button(8, 25, pygame.image.load("./ressources/levels_img/tab4.jpg"))
	big_button5 = Big_button(26, 25, pygame.image.load("./ressources/levels_img/tab5.jpg"))
	big_button6 = Big_button(44, 25, pygame.image.load("./ressources/levels_img/tab6.jpg"))
	big_buttons = [ big_button1, big_button2, big_button3, big_button4, big_button5, big_button6 ]

	level1_title = FONT.render("001", False, Globals.WHITE)
	level2_title = FONT.render("002", False, Globals.WHITE)
	level3_title = FONT.render("003", False, Globals.WHITE)
	level4_title = FONT.render("004", False, Globals.WHITE)
	level5_title = FONT.render("005", False, Globals.WHITE)
	level6_title = FONT.render("006", False, Globals.WHITE)
	levels_titles = [ level1_title, level2_title, level3_title, level4_title, level5_title, level6_title ]

	selection = 1


# ==================================================================================================================================

def select_body(screen):

	global selection


	# ======================================== EVENTS

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			Globals.launched = False

		elif event.type == pygame.KEYDOWN:

			# selection

			if event.key == pygame.K_RIGHT:
				selection += 1

			elif event.key == pygame.K_LEFT:
				selection -= 1

			elif event.key == pygame.K_UP or event.key == pygame.K_UP:
				selection = 0

			elif event.key == pygame.K_DOWN and selection == 0:
				selection = 1

			# activation de la selection
			elif event.key == pygame.K_RETURN:
				# retour arrière
				if selection == 0:
					Globals.ecran = "menu"
				# lancement d'un niveau
				else :
					if selection == 1:
						Globals.level = 1
					elif selection == 2:
						Globals.level = 2
					elif selection == 3:
						Globals.level = 3
					elif selection == 4:
						Globals.level = 4
					elif selection == 5:
						Globals.level = 5
					elif selection == 6:
						Globals.level = 6
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

	if selection > 6:
		selection = 6
	elif selection < 0:
		selection = 0

# ==================================================================================================================================

def select_display(screen):

	global FONT, TITLE_FONT, clock, selection, big_buttons, levels_titles

	# ======================================== DESSIN DES SURFACES

	# fond
	screen.surface.fill(Globals.BLACK)
	
	# gros bouttons
	i = 0
	for button in big_buttons:
		screen.surface.blit(button.sprite, (button.rect.x, button.rect.y) )
		screen.surface.blit( levels_titles[i], (button.rect.x, button.rect.y - 1.5*Globals.RATIO ) )
		i += 1

	# titre
	title = TITLE_FONT.render("LEVEL SELECTION", False, Globals.WHITE)
	screen.surface.blit(title, (1*Globals.RATIO, 1*Globals.RATIO) )


	# retour arrière
	if selection == 0:
		back_button = FONT.render("BACK <-", False, Globals.WHITE)
	else:
		back_button = FONT.render("BACK", False, Globals.WHITE)
	screen.surface.blit(back_button, (1*Globals.RATIO, 4*Globals.RATIO) )

	# sélection
	select_button = FONT.render("<- START ->", False, Globals.WHITE)
	if selection == 1:
		screen.surface.blit(select_button, (8*Globals.RATIO, 18*Globals.RATIO) )
	elif selection == 2:
		screen.surface.blit(select_button, (26*Globals.RATIO, 18*Globals.RATIO) )
	elif selection == 3:
		screen.surface.blit(select_button, (44*Globals.RATIO, 18*Globals.RATIO) )
	elif selection == 4:
		screen.surface.blit(select_button, (8*Globals.RATIO, 33*Globals.RATIO) )
	elif selection == 5:
		screen.surface.blit(select_button, (26*Globals.RATIO, 33*Globals.RATIO) )
	elif selection == 6:
		screen.surface.blit(select_button, (44*Globals.RATIO, 33*Globals.RATIO) )


	# actualisation de l'écran
	pygame.display.flip()

	
	# ========== MISE A JOUR

	Globals.counter += 1
	clock.tick(Globals.FPS)