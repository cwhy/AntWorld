import pygame
import sys
from worldModel import AntWorld
from math import pi
from pygame.locals import QUIT
from pygame.locals import DOUBLEBUF
#from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor


def rot_center(filename, angle):
    """rotate an image while keeping its center and size"""
    image = pygame.image.load(filename)
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def drawAnts(ant):
    antImg = rot_center('ant.png', -ant.facingAngle / 2 / pi * 360)
    SURFACE.blit(antImg, (ant.x - 15, ant.y - 15))

#Initialisation
# pool = Pool(5)
pool = ThreadPoolExecutor(3)
pygame.init()
fpsClock = pygame.time.Clock()  # setup clock
antWorld = AntWorld(1, 500, 500)  # game model
FPS = 30  # frames per second setting

# set up the window
SURFACE = pygame.display.set_mode((antWorld.land.length, antWorld.land.width), DOUBLEBUF, 32)
pygame.display.set_caption('antWorld')
SURFACE.fill(antWorld.land.bgColor)

# load image resources
foodImg = pygame.image.load('food.png')
SURFACE.blit(foodImg, (antWorld.food.x-15,antWorld.food.y-15))


#World Simulation Start
while not antWorld.checkSuccess():  # the main game loop

    antWorld.run()
    for ant in antWorld.ants:
        # pool.submit(ant)
        ant()
    pool.submit(antWorld.land.updateSignalAll())
    antWorld.land.updateSignalAll()

    SURFACE.blit(foodImg, (antWorld.food.x-15,antWorld.food.y-15))

    map(drawAnts, antWorld.ants)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
#     map(drawLandUpdate, antWorld.ants)
#     for _x in range(antWorld.land.width):
#         for _y in range(antWorld.land.length):
#             if antWorld.land.signal['Ant'][_x,_y,1] != 0:
#                 print _x, _y
#                 SURFACE.set_at((_x, _y), antWorld.land.getColorP(_x,_y))
    print antWorld.land.time
    pygame.surfarray.blit_array(SURFACE, antWorld.land.getColorAll())
    fpsClock.tick(FPS)
pygame.quit()
sys.exit()
