# -*- coding : utf-8 -*-

import pygame

from global_variables import *
from classes.screen import *
from classes.big_button import *


# ==================================================================================================================================

class Selection:

	def __init__(self):

		# MENU
		big_button1 = Big_button(8, 10, pygame.image.load("./resources/levels_img/tab1.jpg"))
		big_button2 = Big_button(26, 10, pygame.image.load("./resources/levels_img/tab2.jpg"))
		big_button3 = Big_button(44, 10, pygame.image.load("./resources/levels_img/tab3.jpg"))
		big_button4 = Big_button(8, 25, pygame.image.load("./resources/levels_img/tab4.jpg"))
		big_button5 = Big_button(26, 25, pygame.image.load("./resources/levels_img/tab5.jpg"))
		big_button6 = Big_button(44, 25, pygame.image.load("./resources/levels_img/tab6.jpg"))
		self.big_buttons = [ big_button1, big_button2, big_button3, big_button4, big_button5, big_button6 ]

		level1_title = Globals.FONT.render("001", False, Globals.WHITE)
		level2_title = Globals.FONT.render("002", False, Globals.WHITE)
		level3_title = Globals.FONT.render("003", False, Globals.WHITE)
		level4_title = Globals.FONT.render("004", False, Globals.WHITE)
		level5_title = Globals.FONT.render("005", False, Globals.WHITE)
		level6_title = Globals.FONT.render("006", False, Globals.WHITE)
		self.levels_titles = [ level1_title, level2_title, level3_title, level4_title, level5_title, level6_title ]

		self.selection = 1

# ==================================================================================================================================


	def body(self, screen):

		# EVENTS

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				Globals.launched = False

			elif event.type == pygame.KEYDOWN:

				# selection
				if event.key == pygame.K_RIGHT:
					self.selection += 1

				elif event.key == pygame.K_LEFT:
					self.selection -= 1

				elif event.key == pygame.K_UP or event.key == pygame.K_UP:
					self.selection = 0

				elif event.key == pygame.K_DOWN and self.selection == 0:
					self.selection = 1

				# activation de la sélection
				elif event.key == pygame.K_RETURN:
					# retour arrière
					if self.selection == 0:
						Globals.ecran = "menu"
					# lancement d'un niveau
					else :
						if self.selection == 1:
							Globals.level = 1
						elif self.selection == 2:
							Globals.level = 2
						elif self.selection == 3:
							Globals.level = 3
						elif self.selection == 4:
							Globals.level = 4
						elif self.selection == 5:
							Globals.level = 5
						elif self.selection == 6:
							Globals.level = 6
						Globals.ecran = "game"

		# FENETRE
		keys = pygame.key.get_pressed()
		screen.update(keys)

		# SELECTION
		if self.selection > 6:
			self.selection = 6
		elif self.selection < 0:
			self.selection = 0

# ==================================================================================================================================


	def display(self, screen):

		# fond
		screen.surface.fill(Globals.BLACK)
		
		# gros bouttons
		i = 0
		for button in self.big_buttons:
			screen.surface.blit(button.sprite, (button.rect.x, button.rect.y) )
			screen.surface.blit( self.levels_titles[i], (button.rect.x, button.rect.y - 1.5*Globals.RATIO ) )
			i += 1

		# titre
		title = Globals.TITLE_FONT.render("LEVEL SELECTION", False, Globals.WHITE)
		screen.surface.blit(title, (1*Globals.RATIO, 1*Globals.RATIO) )

		# retour arrière
		if self.selection == 0:
			back_button = Globals.FONT.render("BACK <-", False, Globals.WHITE)
		else:
			back_button = Globals.FONT.render("BACK", False, Globals.WHITE)
		screen.surface.blit(back_button, (1*Globals.RATIO, 4*Globals.RATIO) )

		# sélection
		select_button = Globals.FONT.render("<- START ->", False, Globals.WHITE)
		if self.selection == 1:
			screen.surface.blit(select_button, (8*Globals.RATIO, 18*Globals.RATIO) )
		elif self.selection == 2:
			screen.surface.blit(select_button, (26*Globals.RATIO, 18*Globals.RATIO) )
		elif self.selection == 3:
			screen.surface.blit(select_button, (44*Globals.RATIO, 18*Globals.RATIO) )
		elif self.selection == 4:
			screen.surface.blit(select_button, (8*Globals.RATIO, 33*Globals.RATIO) )
		elif self.selection == 5:
			screen.surface.blit(select_button, (26*Globals.RATIO, 33*Globals.RATIO) )
		elif self.selection == 6:
			screen.surface.blit(select_button, (44*Globals.RATIO, 33*Globals.RATIO) )

		# MISE A JOUR
		pygame.display.flip()
		Globals.counter += 1