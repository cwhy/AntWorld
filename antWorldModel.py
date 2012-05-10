from life import Ant, Food
from math import sqrt
class AntWorld:
    '''
    It contains the World Model
    '''
    def __init__(self, numOfAnts = 1, width = 800, length = 800):
        self.numOfAnts = numOfAnts
        self.width = width
        self.length = length
        self.land = Land(width, length)
        self.ant = Ant(self.land)
        self.food = Food(self.land)
         
    def run(self):
        self.ant.walk()
        self.checkBoundary()
        
    def checkSuccess(self):
        if self.getDistance(self.ant, self.food)<10:
            return True
        return False
    
    def getFoodPosition(self):
        return (self.food.x, self.food.y)
    
    def getAntPosition(self):
        return (self.ant.x, self.ant.y)
    
    def getDistance(self, lifea, lifeb):
        return sqrt((lifea.x-lifeb.x)**2+(lifea.y-lifeb.y)**2)
    
    def checkBoundary(self):
        #Rule 1 Touch wall = cross    
        if (self.ant.x>=794):
            self.ant.x = 5
        elif(self.ant.y>=794):
            self.ant.y = 5
        elif(self.ant.x<=5):
            self.ant.x = 794
        elif(self.ant.y<=5):
            self.ant.y = 794    

class Land:
    def __init__(self, length, width):
        self.length = length
        self.width = width
