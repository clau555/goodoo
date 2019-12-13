from classes.entity import *
from classes.player import *
from classes.weapon import *
from classes.enemy1 import *
from classes.enemy2 import *
from classes.enemy3 import *
from classes.mist import *
from ressources.conversion_tool import *

# ========== VAGUES

class Level6:

	def __init__(self):

		self.im = Image.open('ressources/levels_tab/tab6.jpg')
		self.TAB = convert_to_tab(self.im)

		self.player = Player(31.0, 31.0)
		self.weapon = None

		# ==================== VAGUE 1

		def pre_wave1(self):

			Mist(1.0, 25.0)
			Mist(10.0, 5.0)
			Mist(60.0, 25.0)
			Mist(55.0, 5.0)


		def wave1(self):
			# JOUEUR
			self.player.weaponized = False
			# ARME
			self.weapon = Weapon(12.0, 1.0)
			# ENNEMIES
			Enemy1(1.0, 25.0)
			Enemy1(10.0, 5.0)
			Enemy1(60.0, 25.0)
			Enemy1(55.0, 5.0)


		# ==================== VAGUE 2

		def pre_wave2(self):

			Mist(1.0, 25.0)
			Mist(4.0, 6.0)
			Mist(60.0, 25.0)
			Mist(59.0, 6.0)


		def wave2(self):
			# JOUEUR
			self.player.weaponized = False
			self.player.sprites_right = [ pygame.image.load("./ressources/goodoo_white/1.png"),
									pygame.image.load("./ressources/goodoo_white/2.png") ]
			self.player.sprites_left = [ pygame.image.load("./ressources/goodoo_white/3.png"),
									pygame.image.load("./ressources/goodoo_white/4.png") ]
			# ARME
			self.weapon = Weapon(41.0, 24.0)
			# ENNEMIES
			Enemy2(1.0, 25.0)
			Enemy2(4.0, 6.0)
			Enemy2(60.0, 25.0)
			Enemy2(59.0, 6.0)

		# ==================== VAGUE 3

		def pre_wave3(self):

			Mist(1.0, 25.0)
			Mist(10.0, 5.0)
			Mist(60.0, 25.0)
			Mist(55.0, 5.0)

		def wave3(self):
			# JOUEUR
			self.player.weaponized = False
			self.player.sprites_right = [ pygame.image.load("./ressources/goodoo_white/1.png"),
									pygame.image.load("./ressources/goodoo_white/2.png") ]
			self.player.sprites_left = [ pygame.image.load("./ressources/goodoo_white/3.png"),
									pygame.image.load("./ressources/goodoo_white/4.png") ]
			# ARME
			self.weapon = Weapon(49.0, 1.0)
			# ENNEMIES
			Enemy3(1.0, 25.0)
			Enemy3(10.0, 5.0)
			Enemy3(60.0, 25.0)
			Enemy3(55.0, 5.0)


		# ==================== REPERTOIRE DES FONCTIONS

		self.pre_waves = [ pre_wave1, pre_wave2, pre_wave3 ]
		self.waves = [ wave1, wave2, wave3 ]