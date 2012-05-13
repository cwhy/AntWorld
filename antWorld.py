import random
import numpy as np
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

def getLandColor(landElement, RANDOM = False):
	if RANDOM == True:
	        return (200 + int(random.random() * 55), 200 + int(random.random() * 55), 200 + int(random.random() * 55)) 
	else:
		red = 250 -int((landElement.smell[0]/100)*250)
		green = 250-int((landElement.smell[0]/100)*100)
		blue = 250-int((landElement.smell[0]/100)*100)
		return ( red, green, blue ) 

def fullLandUpdate(antWorld):
	landArray = np.zeros((antWorld.length, antWorld.width, 3), dtype=int) # 3 indicates we need to store R,G and B values for each point
	for column in antWorld.land.element:
		for e in column:
			landArray[e.x, e.y, :] = getLandColor(e)
	pygame.surfarray.blit_array(SURFACE, landArray)

def drawLandUpdate(ant):
    '''refresh the part of the background that ant went pass'''
    for x in range(int(ant.x)-20, int(ant.x)+20):
        for y in range(int(ant.y)-20, int(ant.y)+20):
            e = antWorld.land.element[x%antWorld.length][y%antWorld.width]
            SURFACE.set_at((e.x, e.y), getLandColor(e))

def drawAnts(ant):
    antImg = rot_center('ant.png', -ant.facingAngle/2/pi*360) 
    SURFACE.blit(antImg, (ant.x - 15, ant.y - 15))
   
#Initialization
pygame.init()
fpsClock = pygame.time.Clock() #setup clock
antWorld = AntWorld(30, 800, 800) # game model
FPS = 30 # frames per second setting
iWHITE = (250, 250, 250) # background color

# set up the window
SURFACE = pygame.display.set_mode((antWorld.length, antWorld.width), 0, 32)
pygame.display.set_caption('antWorld')
SURFACE.fill(iWHITE)

# load image resources
foodImg = pygame.image.load('food.png')

#World Simulation Start
while not antWorld.checkSuccess(): # the main game loop

    antWorld.run()
    map(drawLandUpdate, antWorld.ants)  
#   fullLandUpdate(antWorld)
    SURFACE.blit(foodImg, antWorld.getFoodPosition())
    map(drawAnts, antWorld.ants)  
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)
    
pygame.quit()
sys.exit()
