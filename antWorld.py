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

def drawLandUpdate(ant):
    '''refresh the part of the background that ant went pass'''
    for x in range(int(ant.x)-5, int(ant.x)+33):
        for y in range(int(ant.y)-5, int(ant.y)+33):
            e = antWorld.land.element[x % antWorld.length][y % antWorld.width]
            SURFACE.set_at((e.x, e.y), e.color)

def drawAnts(ant):
    antImg = rot_center('ant.png', -ant.facingAngle/2/pi*360) 
    SURFACE.blit(antImg, (ant.x, ant.y))
   
#Initialization
pygame.init()
fpsClock = pygame.time.Clock() #setup clock
antWorld = AntWorld(1, 800, 800) # game model
FPS = 30 # frames per second setting
iWHITE = (250, 250, 250) # background color

# set up the window
SURFACE = pygame.display.set_mode((antWorld.length, antWorld.width), 0, 32)
pygame.display.set_caption('antWorld')
SURFACE.fill(iWHITE)

# load image resources
foodImg = pygame.image.load('food.png')
SURFACE.blit(foodImg, antWorld.getFoodPosition())

#World Simulation Start
while not antWorld.checkSuccess(): # the main game loop

    antWorld.run()
    map(drawLandUpdate, antWorld.ants)    
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
