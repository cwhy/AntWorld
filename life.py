import random
from math import *


class life():
        def __init__(self):
            self.x = 0
            self.y = 0
            self.alive = True
            self.facingangle = 0
            # Right direction is 0, anticlockwise positive
            
        def move(self, turn, forward):
            if forward < 0:
                raise ValueError, 'Moving distance should be positive!'         
            
            # turn, and add randomness to the turning command
            facingangle = self.facingangle + float(turn)
            facingangle %= 2 * pi
           
            # move, and add randomness to the motion command
            dist = float(forward)
            x = self.x + (cos(facingangle) * dist)
            y = self.y + (sin(facingangle) * dist)
            
            self.x = x
            self.y = y
            self.facingangle = facingangle
            print facingangle
        def randomize_position(self, newland):
            self.x = int(random.random() * newland.width)
            self.y = int(random.random() * newland.length)
            
class ants(life):
    def __init__(self):
        life.__init__(self)
        self.x = 0
        self.y = 0
        self.type = 'life'
        self.imagename = 'ant.png'

class antfood(life):
    def __init__(self):
        life.__init__(self)
        self.x = 0
        self.y = 0
        self.type = 'antfood'
        self.imagename = 'food.png'
    