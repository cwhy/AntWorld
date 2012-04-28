import random
from math import *


class Life:
        def __init__(self):
            self.x = 0
            self.y = 0
            self.alive = True
            self.facingAngle = 0
            # Right direction is 0, anticlockwise positive
            
        #Function: used to turn ant and move the ant forward
		#Parameter: angle of turning, step length
		#Return: none
		def move(self, turn, forward):
            if forward < 0:
                raise ValueError, 'Moving distance should be positive!'         
            
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
			
        # def randomize_position(self, newland):
            # self.x = int(random.random() * newland.width)
            # self.y = int(random.random() * newland.length)
            
class Ant(life):
    def __init__(self):
        life.__init__(self)
        self.x = 0
        self.y = 0
        self.type = 'life'
        self.imageName = 'ant.png'

class Food(life):
    def __init__(self):
        life.__init__(self)
        self.x = 0
        self.y = 0
        self.type = 'antfood'
        self.imageName = 'food.png'
    