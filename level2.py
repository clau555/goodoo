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

class Level2:

	def __init__(self):

		self.im = Image.open('ressources/levels_tab/tab2.jpg')
		self.TAB = convert_to_tab(self.im)

		self.player = Player(7.0, 15.0)
		self.weapon = None

		# ==================== VAGUE 1

		def pre_wave1(self):

			Mist(59.0, 8.0)


		def wave1(self):
			# JOUEUR
			self.player.weaponized = False
			# ARME
			self.weapon = Weapon(26.0, 2.0)
			# ENNEMIES
			Enemy2(59.0, 8.0)


		# ==================== VAGUE 2

		def pre_wave2(self):

			Mist(50.0, 20.0)
			Mist(12.0, 20.0)


		def wave2(self):
			# ARME
			self.weapon = Weapon(31.0, 33.0)
			# ENNEMIES
			Enemy2(50.0, 20.0)
			Enemy2(12.0, 20.0)


		# ==================== VAGUE 3

		def pre_wave3(self):

			Mist(18.0, 25.0)
			Mist(26.0, 2.0)
			Mist(32.0, 2.0)
			Mist(31.0, 22.0)


		def wave3(self):
			# ARME
			self.weapon = Weapon(8.0, 1.0)
			# ENNEMIES
			Enemy2(18.0, 25.0)
			Enemy1(26.0, 2.0)
			Enemy1(32.0, 2.0)
			Enemy1(31.0, 22.0)


		# ==================== REPERTOIRE DES FONCTIONS

		self.pre_waves = [ pre_wave1, pre_wave2, pre_wave3 ]
		self.waves = [ wave1, wave2, wave3 ]