"""
-- EN COURS
Changelog 6:
	Corrections diverses
	Transition entre les vagues
	Menu et sélection des niveaux
	Game over
	Setup niveaux 1, 2 et 3
	Amélioration IA
	Ennemies 3 et 4?
"""

import inspect
from game import *
from menu import *
from guide import * 
from select import *
from game_over import *
from game_victory import *
from gl0bals import *


pygame.init()
screen = Screen()

Globals.launched = True

while Globals.launched:

	if Globals.ecran == "game":
		game_initialize()
		while Globals.ecran == "game" and Globals.launched:
			game_body(screen)
			game_display(screen)
		# vidage de la mémoire
		Globals.blocks = []
		Globals.enemies1 = []
		Globals.enemies2 = []
		Globals.enemies3 = []
		Globals.enemies = []
		Globals.projectiles = []
		Globals.mists = []
		Globals.popups = []
		Globals.transition = Globals.TRANSITION

	elif Globals.ecran == "menu":
		menu_initialize()
		while Globals.ecran == "menu" and Globals.launched:
			menu_body(screen)
			menu_display(screen)

	elif Globals.ecran == "select":
		select_initialize()
		while Globals.ecran == "select" and Globals.launched:
			select_body(screen)
			select_display(screen)

	elif Globals.ecran == "guide":
		guide_initialize()
		while Globals.ecran == "guide" and Globals.launched:
			guide_body(screen)
			guide_display(screen)

	elif Globals.ecran == "game_over":
		over_initialize()
		while Globals.ecran == "game_over" and Globals.launched:
			over_body(screen)
			over_display(screen)

	elif Globals.ecran == "game_victory":
		victory_initialize()
		while Globals.ecran == "game_victory" and Globals.launched:
			victory_body(screen)
			victory_display(screen)

pygame.quit()