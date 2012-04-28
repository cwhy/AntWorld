import pygame, sys
from pygame.locals import *
import life
import land
import worldtimecycle
from math import *


def rot_center(filename, angle):
    """rotate an image while keeping its center and size"""
    image = pygame.image.load(filename)
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

pygame.init()
FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

newland = land.land(800)
# set up the window
DISPLAYSURF = pygame.display.set_mode((newland.length, newland.width), 0, 32)
pygame.display.set_caption('antWorld')

iWHITE = (250, 250, 250)

ant1 = life.ants()
food1 = life.antfood()
ant1.randomize_position(newland)
food1.randomize_position(newland)
antImg = pygame.image.load(ant1.imagename)
foodImg = pygame.image.load(food1.imagename)

#World Simulation Start

while True: # the main game loop
    DISPLAYSURF.fill(iWHITE)
    DISPLAYSURF.blit(foodImg, (food1.x, food1.y)) 
    WorldStatus = worldtimecycle.randomwalk(ant1, food1)#from cycle.py
    antImg = rot_center(ant1.imagename, -ant1.facingangle/2/pi*360) 
    display = DISPLAYSURF.blit(antImg, (ant1.x, ant1.y))   
    if WorldStatus == '2012' or WorldStatus == 'MissionComplete':
        print WorldStatus
        pygame.quit()
        sys.exit()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    print ant1.x, ant1.y, ant1.facingangle, food1.x, food1.y
    
    pygame.display.update()
    fpsClock.tick(FPS)