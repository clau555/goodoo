# -*- coding : utf-8 -*-

from view.game import *
from view.menu import *
from view.guide import * 
from view.selection import *
from view.game_over import *
from view.game_victory import *
from global_variables import *


screen = Screen()

Globals.launched = True

while Globals.launched:

	if Globals.ecran == "game":
		game = Game()
		while Globals.ecran == "game" and Globals.launched:
			game.body(screen)
			game.display(screen)
		# vidage de la mémoire
		Globals.blocks = []
		Globals.enemies = []
		Globals.projectiles = []
		Globals.mists = []
		Globals.popups = []

	elif Globals.ecran == "menu":
		menu = Menu()
		while Globals.ecran == "menu" and Globals.launched:
			menu.body(screen)
			menu.display(screen)

	elif Globals.ecran == "select":
		selection = Selection()
		while Globals.ecran == "select" and Globals.launched:
			selection.body(screen)
			selection.display(screen)

	elif Globals.ecran == "guide":
		guide = Guide()
		while Globals.ecran == "guide" and Globals.launched:
			guide.body(screen)
			guide.display(screen)

	elif Globals.ecran == "game_over":
		gameover = GameOver()
		while Globals.ecran == "game_over" and Globals.launched:
			gameover.body(screen)
			gameover.display(screen)

	elif Globals.ecran == "game_victory":
		gamevictory = GameVictory()
		while Globals.ecran == "game_victory" and Globals.launched:
			gamevictory.body(screen)
			gamevictory.display(screen)

pygame.quit()