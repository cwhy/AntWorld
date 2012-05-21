import random
import pygame, sys
from worldModel import AntWorld
from math import pi
from pygame.locals import QUIT

def rot_center(filename, angle):
    """rotate an image while keeping its center and size"""
    image = pygame.image.load(filename)
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def getLandColor(landElement, RANDOM=False):
    if RANDOM == True:
        return (200 + int(random.random() * 55), 200 + int(random.random() * 55), 200 + int(random.random() * 55)) 
    else:
        s = landElement.getSignal()

        if  s > 100:
            s = 100.0
        red = 250 - int((s / 100) * 250 )
        green = 250 - int((s / 100) * 50)
        blue = 250 - int((s / 100) * 50)
        return (red, green, blue) 

def drawLandUpdate(ant):
    '''refresh the part of the background that ant went pass'''
    refreshRange = 20 #Min 20 for the ant picture
    for x in range(int(ant.x) - refreshRange, int(ant.x) + refreshRange):
        for y in range(int(ant.y) - refreshRange, int(ant.y) + refreshRange):
            e = antWorld.land.getElement(x,y)
            SURFACE.set_at((e.x, e.y), getLandColor(e))

def drawAnts(ant):
    antImg = rot_center('ant.png', -ant.facingAngle / 2 / pi * 360) 
    SURFACE.blit(antImg, (ant.x - 15, ant.y - 15))
   
#Initialisation
pygame.init()
fpsClock = pygame.time.Clock() #setup clock
antWorld = AntWorld(6, 700, 700) # game model
FPS = 30 # frames per second setting
iWHITE = (250, 250, 250) # background color

# set up the window
SURFACE = pygame.display.set_mode((antWorld.land.length, antWorld.land.width), 0, 32)
pygame.display.set_caption('antWorld')
SURFACE.fill(iWHITE)

# load image resources
foodImg = pygame.image.load('food.png')
SURFACE.blit(foodImg, antWorld.food.getPosition())


#World Simulation Start
while not antWorld.checkSuccess(): # the main game loop

    antWorld.run() 
    SURFACE.blit(foodImg, antWorld.food.getPosition())
    map(drawAnts, antWorld.ants)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    map(drawLandUpdate, antWorld.ants) 
    fpsClock.tick(FPS)
pygame.quit()
sys.exit()
