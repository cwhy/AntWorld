import random
from math import *

class Life:
    def __init__(self, land):
        self.x = 0
        self.y = 0
        self.land = land

class Ant(Life):
    def __init__(self, land):
        Life.__init__(self, land)
        self.facingAngle = 0
        # Right direction is 0, anticlockwise positive

    def move(self, turn, forward):
        '''
        Function: used to turn ant and move the ant forward
        Parameter: angle of turning, step length>0
        Return: none
        '''
        # turn
        facingAngle = self.facingAngle + float(turn)
        facingAngle %= 2 * pi
           
        # move
        dist = float(forward)
        x = self.x + (cos(facingAngle) * dist)
        y = self.y + (sin(facingAngle) * dist)
        
        # update
        self.x = x
        self.y = y
        self.facingAngle = facingAngle
        
    def walk(self):
        '''random walk with step length 5 and random parameter 0.3'''
        turning_angle = random.gauss(0, 0.3)
        self.move(turning_angle, 5)
        
class Food(Life):
    def __init__(self, land):
        Life.__init__(self, land)
        self.x, self.y = 400, 400

class Land:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        