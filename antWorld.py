import pygame, sys
from antWorldModel import AntWorld
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

#Initialization
pygame.init()
fpsClock = pygame.time.Clock() #setup clock
antWorld = AntWorld() # game model
FPS = 30 # frames per second setting
iWHITE = (250, 250, 250) # background color

# set up the window
DISPLAYSURF = pygame.display.set_mode((antWorld.length, antWorld.width), 0, 32)
pygame.display.set_caption('antWorld')

# load image resources
foodImg = pygame.image.load('food.png')

#World Simulation Start
while not antWorld.checkSuccess(): # the main game loop
    DISPLAYSURF.fill(iWHITE)
    DISPLAYSURF.blit(foodImg, antWorld.getFoodPosition())  
    antImg = rot_center('ant.png', -antWorld.ant.facingAngle/2/pi*360) 
    display = DISPLAYSURF.blit(antImg, antWorld.getAntPosition())   
    
    antWorld.run()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.update()
    fpsClock.tick(FPS)
    
pygame.quit()
sys.exit()