import pygame, sys
from pygame.locals import *

pygame.init()

#Create a displace surface object
DISPLAYSURF = pygame.display.set_mode((400, 300), FULLSCREEN)

mainLoop = True

while mainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
    pygame.display.update()

pygame.quit()
