import pygame
from environnements import *

"""
Changelog 2:
	Fenêtre de 1280x720px
	Environnement en grille 64x36 blocs
	1 bloc = 20 px
	Grille de 64x36 blocs
	Nouvelle taille du joueur (1 bloc)

Changelog 3:
	Collision entre le joueur et le décor
	Passage en programmation orienté objet -- IMPORTANT
"""


#========== INITIALISATION VARIABLES GLOBALES ==========

ratio = 20 # ratio écran/grille

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

class Screen(object):

	def __init__(self):

		self.resolution = (1280,720)
		self.surface = pygame.display.set_mode((1280,720))
		self.fullscreen = False
		


class Player(object):

	def __init__(self):

		self.x = 45.0
		self.y = 17.0
		self.width = 1
		self.rect = pygame.Rect((self.x*ratio, self.y*ratio), (self.width*ratio,self.width*ratio)) # hitbox
		self.sprites = [ pygame.image.load("img/goodoo_white/goodoo1.png"),
						pygame.image.load("img/goodoo_white/goodoo2.png"),
						pygame.image.load("img/goodoo_white/goodoo3.png"),
						pygame.image.load("img/goodoo_white/goodoo4.png") ]
		self.sprite = self.sprites[0] # sprite courant
		self.last_move = "right"
		self.velocity = 0.2


	def coord_to_real(x, y):
		"""Convertis les coords de la grille en coords de pixels"""

		return (x*ratio , y*ratio)


	def move(self, vx, vy):
		"""Bouge chaque axe séparemment"""

		if vx != 0:
			self.move_single_axis(vx, 0)
		if vy != 0:
			self.move_single_axis(0, vy)


	def move_single_axis(self, vx, vy):

		self.x += vx
		self.y += vy

		"""
		# If you collide with a wall, move out based on velocity
		for wall in walls:
			if self.rect.colliderect(wall.rect):
				if vx > 0: # Moving right; Hit the left side of the wall
					self.rect.right = wall.rect.left
				if vx < 0: # Moving left; Hit the right side of the wall
					self.rect.left = wall.rect.right
				if vy > 0: # Moving down; Hit the top side of the wall
					self.rect.bottom = wall.rect.top
				if vy < 0: # Moving up; Hit the bottom side of the wall
					self.rect.top = wall.rect.bottom
		"""

	def animation(self, last_move):
		if last_move=="right" :
			self.sprite = self.sprites[0]

		elif last_move=="left" :
			self.sprite = self.sprites[2]
		


class Block(object): #######inutile pour l'instant
    
    def __init__(self, pos):
        blocks.append(self)
        self.rect = pygame.Rect((pos[0], pos[1]),(ratio,ratio))




#========== INITIALISATION PYGAME ==========

# FENETRE
icon = pygame.image.load("./img/icon.jpg")
pygame.display.set_icon(icon)
pygame.display.set_caption("Goodoo")
screen = Screen()

clock = pygame.time.Clock()
walls = [] # List to hold the walls
player = Player()

tab = tab0 # tableau de 1 et 0 du niveau, cf envirronements.py


#========== CORPS DU PROGRAMME ==========

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
		player.last_move = "left"
		player.move(-player.velocity, 0)
	if keys[pygame.K_RIGHT]:
		player.last_move = "right"
		player.move(player.velocity, 0)
	if keys[pygame.K_UP]:
		player.move(0, -player.velocity)
	if keys[pygame.K_DOWN]:
		player.move(0, player.velocity)



	# DESSIN DES SURFACES
	screen.surface.fill(black)
	#pygame.draw.rect(screen.surface, white, player.rect) # hitbox
	player.animation(player.last_move)
	screen.surface.blit(player.sprite, (player.x*ratio, player.y*ratio) )

	pygame.display.flip() #actualisation de l'écran



	clock.tick(60) #60 fps

pygame.quit()