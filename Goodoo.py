import pygame
from environnements import *

"""
Changelog 4:
	Gravité du joueur
	Saut du joueur
"""


#========== INITIALISATION VARIABLES GLOBALES ==========

ratio = 20 # ratio écran / grille
fps = 60 # images/boucles par seconde
counter = 0 # compteur de boucle

# COULEURS
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)
green = (0,255,0)
cyan = (0,255,255)
blue = (0,0,255)
purple = (255,0,255)



#========== OBJETS ==========

class Screen():

	def __init__(self):

		self.resolution = (1280,720)
		self.surface = pygame.display.set_mode((self.resolution))
		self.fullscreen = False
		self.icon = pygame.image.load("ressources/icon.jpg")
		pygame.display.set_icon(self.icon) # icône de la fenÃªtre
		pygame.display.set_caption("Goodoo") # titre de la fenÃªtre



class Block():

	def __init__(self, pos):
    
		blocks.append(self) # est ajouté à  la liste de tout les blocs
		self.rect = pygame.Rect((pos[0], pos[1]),(ratio,ratio))


class Player():

	def __init__(self, x, y):

		self.width = 1

		# ne servent qu'à  l'initialisation
		self.x = x
		self.y = y

		self.rect = pygame.Rect((self.x*ratio, self.y*ratio), (self.width*ratio,self.width*ratio)) # hitbox

		self.vx = list([(i / 20.0) - 1 for i in range(0, 40)]) # plage des vitesses en x
		self.vy = list([(i / 20.0) - 1 for i in range(0, 40)]) # plage des vitesses en y
		self.vx_index = len(self.vx)//2 # rang de la plage de vitesse en x, permet l'accÃ©lÃ©ration
		self.vy_index = len(self.vy)//2 # rang de la plage de vitesse en y, permet l'accÃ©lÃ©ration
		self.v_fixed = 0.2 # vÃ©locitÃ© fixÃ©e lors des dÃ©placements gauche/droite de l'utilisateur

		self.isjump = False
		self.onground = False
		self.iscollide = False
		self.blockcollide = pygame.Rect( (0, 0) , (0, 0) )

		self.sprites_right = [ pygame.image.load("./ressources/goodoo_white/goodoo1.png"),
							pygame.image.load("./ressources/goodoo_white/goodoo2.png")]
		self.sprites_left = [ pygame.image.load("./ressources/goodoo_white/goodoo3.png"),
							pygame.image.load("./ressources/goodoo_white/goodoo4.png")]
		self.animation_counter = 0
		self.sprite = self.sprites_right[self.animation_counter] # sprite courant
		self.last_move = "right"
		


	def move(self, vx, vy):
		"""Bouge chaque axe sÃ©paremment"""

		if vx != 0:
			self.move_single_axis(vx, 0)
		if vy != 0:
			self.move_single_axis(0, vy)



	def move_single_axis(self, vx, vy):
		"""Bouge en fonction de vx et vy"""

		# initialise les collisions
		self.iscollide = False
		self.blockcollide = pygame.Rect( (0, 0) , (0, 0) )


		# bouge le rect
		self.rect.x += vx*ratio
		self.rect.y += vy*ratio

		# Si collision avec un bloc, se repositionne
		for block in blocks:
			if self.rect.colliderect(block.rect):

				self.blockcollide = block.rect # sauvegarde du bloc en collision
				self.iscollide = True

				if vx > 0:
					self.rect.right = self.blockcollide.left
				if vx < 0:
					self.rect.left = self.blockcollide.right
				if vy > 0:
					self.rect.bottom = self.blockcollide.top
					self.onground = True
				if vy < 0:
					self.rect.top = self.blockcollide.bottom
					self.isjump = False
					self.vy_index = len(self.vy)//2



	def gravity(self):

		self.onground = False

		self.move_single_axis(0, self.vy[self.vy_index])
		self.vy_index += 1

		# on ramÃ¨ne la vÃ©locitÃ© Ã  0 si collision avec le sol
		if self.onground:
			self.vy_index = len(self.vy)//2

		# blocage de la vÃ©locitÃ© si Ã  son maximum
		if (self.vy_index >= len(self.vy)-1):
			self.vy_index = len(self.vy)-1



	def jump(self):

		self.move_single_axis(0, self.vy[self.vy_index])
		self.vy_index += 1

		if (self.vy_index >= len(self.vy)//2):
			self.vy_index = len(self.vy)//2
			self.isjump = False



	def animation(self, last_move):
		"""Oriente le sprite joueur selon son dernier mouvement"""

		# passe au sprite suivant toute les 30 images
		if counter%30 == 0:
			self.animation_counter += 1
		# revient au premier sprite une fois le 2e sprite passÃ©
		if self.animation_counter >= len(self.sprites_right):
			self.animation_counter = 0

		# oriente le sprite
		if last_move=="right" :
			self.sprite = self.sprites_right[self.animation_counter]

		elif last_move=="left" :
			self.sprite = self.sprites_left[self.animation_counter]



#========== INITIALISATION PYGAME ==========

pygame.init()

# FENETRE
screen = Screen()

# ENVIRONNEMENT
tab = tab4 # tableau de 1 et 0 du niveau, cf envirronements.py
blocks = [] # liste qui sitock des blocs de l'environnement
# crÃ©er tout les blocs de l'environnement
for i in range(0,len(tab)):
	for j in range(0,len(tab[0])):
		if tab[i][j]==1:
			Block( (j*ratio , i*ratio) )

# JOUEUR
player = Player(30.0,20.0)


# MUSIQUE
#pygame.mixer.music.load("./ressources/music/S.Rachmaninov - prelude op 23 no 5.wav")


# HORLOGE
clock = pygame.time.Clock()


#========== CORPS DU PROGRAMME ==========

#pygame.mixer.music.play()
launched = True

while launched:


	# EVENTS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			launched = False

	# OUT OF BOUND
	if player.rect.y > screen.resolution[1]:
		launched = False

	keys = pygame.key.get_pressed()

	# CONTROLE TOUCHES FENETRE
	if keys[pygame.K_ESCAPE]:
		launched = False
	if keys[pygame.K_F11] and screen.fullscreen==False:
		screen.surface = pygame.display.set_mode(screen.resolution, pygame.FULLSCREEN)
		pygame.mouse.set_visible(False)
		screen.fullscreen = True
	elif keys[pygame.K_F11] and screen.fullscreen==True:
		screen.surface = pygame.display.set_mode(screen.resolution)
		pygame.mouse.set_visible(True)
		screen.fullscreen = False


	# CONTROLE TOUCHES JOUEUR
	# dÃ©placement gauche
	if keys[pygame.K_LEFT]:
		if not(keys[pygame.K_RIGHT]):
			player.last_move = "left"
		player.move(-player.v_fixed, 0)
	# dÃ©placement droit
	if keys[pygame.K_RIGHT]:
		if not(keys[pygame.K_LEFT]):
			player.last_move = "right"
		player.move(player.v_fixed, 0)
	# saut
	if keys[pygame.K_SPACE] and player.onground and not player.isjump:
		player.isjump = True
		player.vy_index = len(player.vy)//6 # rang de vÃ©locitÃ© d'impulsion initiale
	if player.isjump:
		player.jump()


	# GRAVITE JOUEUR
	if not player.isjump:
		player.gravity()


	# DESSIN DES SURFACES
	screen.surface.fill(black)
	# dessine tout les blocs de la liste blocks
	for block in blocks:
		pygame.draw.rect(screen.surface, white, block.rect)
	#pygame.draw.rect(screen.surface, purple, player.blockcollide) # bloc de collision
	#pygame.draw.rect(screen.surface, red, player.rect) # hitbox
	player.animation(player.last_move)
	screen.surface.blit(player.sprite, (player.rect.x, player.rect.y) )

	pygame.display.flip() # actualisation de l'Ã©cran


	counter += 1
	clock.tick(fps)


pygame.quit()