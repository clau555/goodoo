#codin:utf-8
import pygame
import time

pygame.init()

"""ToDo :
	Revoir qualité du code
	collision à gérer (pas par coord)
	environements à travailler
	Fichiers externes pour environement
	sprite ?
"""


"""############INITIALISATIONS VARIBALES############"""

clock = pygame.time.Clock()

screen_resolution = (1000,600)
white = (255,255,255)
black = (0,0,0)
l = 0 #compteur de boucle de rafraichissement
i = 0 #compteur animation goodoo

direction_x = 0
direction_y = 5
x = 500
y = 100


left = False
right = False

"""############INITIALISATIONS SURFACES############"""

pygame.display.set_caption("Goodoo")

screen = pygame.display.set_mode((screen_resolution))

#ENVIRONNEMENT 1
ground = pygame.Rect((0,590,1000,10))
#mur gauche
rect1 = pygame.Rect((0,40,30,110))
rect2 = pygame.Rect((0,150,50,150))
rect3 = pygame.Rect((0,300,80,290))
rect4 = pygame.Rect((80,450,70,250))
#mur droite
rect5 = pygame.Rect((1000-30,40,30,110))
rect6 = pygame.Rect((1000-50,150,50,150))
rect7 = pygame.Rect((1000-80,300,80,290))
rect8 = pygame.Rect((1000-80-70,450,70,250))

def environnement1():
	pygame.draw.rect(screen, white, ground)
	pygame.draw.rect(screen, white, rect1)
	pygame.draw.rect(screen, white, rect2)
	pygame.draw.rect(screen, white, rect3)
	pygame.draw.rect(screen, white, rect4)
	pygame.draw.rect(screen, white, rect5)
	pygame.draw.rect(screen, white, rect6)
	pygame.draw.rect(screen, white, rect7)
	pygame.draw.rect(screen, white, rect8)

environnement1()


#JOUEUR

goodoo1 = pygame.image.load("goodoo1.png")
goodoo2 = pygame.image.load("goodoo2.png")
goodoo3 = pygame.image.load("goodoo3.png")
goodoo4 = pygame.image.load("goodoo4.png")
goodoo1.convert_alpha()
goodoo2.convert_alpha()
goodoo3.convert_alpha()
goodoo4.convert_alpha()

goodoo = (goodoo1, goodoo2, goodoo3, goodoo4)
screen.blit(goodoo[1],(500,100))


#PREMIERE ACTUALISATION
pygame.display.flip()

"""############FONCTIONS############"""

"""def collision():
	if goodoo.coliderect(ground):"""



"""############CORPS############"""

launched = True #Vrai tant que fenêtre active

while launched:

	#EVENTS
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			launched = False

		#contrôle des touches
		elif event.type == pygame.KEYDOWN:

			if event.key == pygame.K_ESCAPE:
				launched = False

			if event.key == pygame.K_RIGHT:
				right = True

			if event.key == pygame.K_LEFT:
				left = True

			if right and left:
				direction_x = 0

			elif right:
				direction_x = 5
				if i == 3:
					i = 1
				elif i == 2:
					i = 0
				print("droite")

			elif left:
				direction_x = -5
				if i == 1:
					i = 3
				elif i == 0:
					i = 2
				print("gauche")


		elif event.type == pygame.KEYUP:

			if event.key == pygame.K_RIGHT:
				right = False
				direction_x = 0
				print("plus droite")

			elif event.key == pygame.K_LEFT:
				left = False
				direction_x = 0
				print("plus gauche")


	#ACTUALISATION VARIABLES

	#animation
	if l%30 == 0:
		if i == 0:
			i = 1
		elif i == 1:
			i = 0
		elif i == 2:
			i = 3
		elif i == 3:
			i = 2

	#coords
	x += direction_x

	if y >= 590 - 48:
		y += 0
	else:
		y += direction_y
	
	#
	l += 1

	#ACTUALISATION SURFACES
	screen.fill(black)
	environnement1()
	screen.blit(goodoo[i],(x,y))

	pygame.display.flip()
	time.sleep(.016) # 60 fps

pygame.quit()