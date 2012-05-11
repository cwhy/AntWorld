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

class LandElement:
	'''all kinds of infomation in land'''
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.antSignal = 0 # the tracing signal of ants
		self.color = (200+int(random.random() * 55), 200+int(random.random() * 55), 200+int(random.random() * 55))# Used for testing

class Land:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.element = []
        for x in range(0,length):
            column = []
            for y in range(0,width):
                column.append(LandElement(x, y))
            self.element.append(column)

