import pygame
from environnements import *

"""
Changelog 3:
	Collision entre le joueur et le décor
	Passage en programmation orienté objet -- IMPORTANT
"""


#========== INITIALISATION VARIABLES GLOBALES ==========

ratio = 20 # ratio écran/grille
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



class Block():

	def __init__(self, pos):

		blocks.append(self) # est ajouté à la liste de tout les blocs
		self.rect = pygame.Rect((pos[0], pos[1]),(ratio,ratio))



class Player():

	def __init__(self):

		self.width = 1
		self.rect = pygame.Rect((42.0*ratio, 20.0*ratio), (self.width*ratio,self.width*ratio)) # hitbox
		self.sprites_right = [ pygame.image.load("ressources/goodoo_white/goodoo1.png"),
							pygame.image.load("ressources/goodoo_white/goodoo2.png")]
		self.sprites_left = [ pygame.image.load("ressources/goodoo_white/goodoo3.png"),
							pygame.image.load("ressources/goodoo_white/goodoo4.png")]
		self.animation_counter = 0
		self.sprite = self.sprites_right[self.animation_counter] # sprite courant
		self.last_move = "right"
		self.velocity = 0.2 # blocs par image


	def move(self, vx, vy):
		"""Bouge chaque axe séparemment"""

		if vx != 0:
			self.move_single_axis(vx, 0)
		if vy != 0:
			self.move_single_axis(0, vy)


	def move_single_axis(self, vx, vy):
		"""Bouge en fonction de vx et vy"""

		# bouge le rect
		self.rect.x += vx*ratio
		self.rect.y += vy*ratio

		# Si collision avec un bloc, se repositionne
		for block in blocks:
			if self.rect.colliderect(block.rect):
				if vx > 0:
					self.rect.right = block.rect.left
				if vx < 0:
					self.rect.left = block.rect.right
				if vy > 0:
					self.rect.bottom = block.rect.top
				if vy < 0:
					self.rect.top = block.rect.bottom


	def animation(self, last_move):
		"""Oriente le joueur selon son dernier mouvement"""

		# on passe au sprite suivant toute les 30 images
		if counter%30 == 0:
			self.animation_counter += 1
		# on revient au premier sprite une fois le 2e sprite passé
		if self.animation_counter >= len(self.sprites_right):
			self.animation_counter = 0

		if last_move=="right" :
			self.sprite = self.sprites_right[self.animation_counter]

		elif last_move=="left" :
			self.sprite = self.sprites_left[self.animation_counter]



#========== INITIALISATION PYGAME ==========

pygame.init()

# FENETRE
icon = pygame.image.load("ressources/icon.jpg")
pygame.display.set_icon(icon)
pygame.display.set_caption("Goodoo")
screen = Screen()

# ENVIRONNEMENT
tab = tab3 # tableau du niveau, cf envirronements.py
blocks = [] # liste qui stock des blocs de l'environnement
# créer tout les blocs de l'environnement
for i in range(0,len(tab)):
	for j in range(0,len(tab[0])):
		if tab[i][j]==1:
			Block( (j*ratio , i*ratio) )

# JOUEUR
player = Player()

# MUSIQUE
pygame.mixer.music.load("ressources/S.Rachmaninov - prelude op 23 no 5.wav")

# HORLOGE
clock = pygame.time.Clock()


#========== CORPS DU PROGRAMME ==========

pygame.mixer.music.play()
launched = True

while launched:


	# EVENTS
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
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
	if keys[pygame.K_LEFT]:
		if not(keys[pygame.K_RIGHT]):
			player.last_move = "left"
		player.move(-player.velocity, 0)
	if keys[pygame.K_RIGHT]:
		if not(keys[pygame.K_LEFT]):
			player.last_move = "right"
		player.move(player.velocity, 0)
	if keys[pygame.K_UP]:
		player.move(0, -player.velocity)
	if keys[pygame.K_DOWN]:
		player.move(0, player.velocity)



	# DESSIN DES SURFACES
	screen.surface.fill(black)
	# dessine tout les blocs de la liste blocks
	for block in blocks:
		pygame.draw.rect(screen.surface, white, block.rect)
	#pygame.draw.rect(screen.surface, red, player.rect) # hitbox
	player.animation(player.last_move)
	screen.surface.blit(player.sprite, (player.rect.x, player.rect.y) )

	pygame.display.flip() # actualisation de l'écran



	counter += 1
	clock.tick(60) # 60 fps


pygame.quit()