# -*- coding : utf-8 -*-

from classes.entity import *
from classes.player import *
from classes.weapon import *
from classes.enemy1 import *
from classes.enemy2 import *
from classes.enemy3 import *
from classes.mist import *
from ressources.conversion_tool import *

# ========== VAGUES

class Level4:

	def __init__(self):

		self.im = Image.open('ressources/levels_tab/tab4.jpg')
		self.TAB = convert_to_tab(self.im)

		self.player = Player(32.0, 5.0)
		self.weapon = None

		# ==================== VAGUE 1

		def pre_wave1(self):

			Mist(13.0, 20.0)
			Mist(51.0, 20.0)


		def wave1(self):
			# JOUEUR
			self.player.weaponized = False
			# ARME
			self.weapon = Weapon(1.0, 32.0)
			# ENNEMIES
			Enemy2(13.0, 20.0)
			Enemy2(51.0, 20.0)


		# ==================== VAGUE 2

		def pre_wave2(self):

			Mist(5.0, 24.0)
			Mist(58.0, 24.0)
			Mist(55.0, 7.0)
			Mist(3.0, 8.0)


		def wave2(self):
			# ARME
			self.weapon = Weapon(62.0, 32.0)
			# ENNEMIES
			Enemy2(5.0, 24.0)
			Enemy2(58.0, 24.0)
			Enemy1(55.0, 7.0)
			Enemy2(3.0, 8.0)


		# ==================== VAGUE 3

		def pre_wave3(self):

			Mist(22.0, 16.0)
			Mist(42.0, 16.0)
			Mist(12.0, 12.0)
			Mist(51.0, 12.0)


		def wave3(self):
			# ARME
			self.weapon = Weapon(36.0, 1.0)
			# ENNEMIES
			Enemy2(22.0, 16.0)
			Enemy2(42.0, 16.0)
			Enemy2(12.0, 12.0)
			Enemy2(51.0, 12.0)


		# ==================== REPERTOIRE DES FONCTIONS

		self.pre_waves = [ pre_wave1, pre_wave2, pre_wave3 ]
		self.waves = [ wave1, wave2, wave3 ]