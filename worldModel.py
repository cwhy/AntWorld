from life import Ant, Food, Land
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
        self.ants = [Ant(self.land) for i in range(numOfAnts)]
        self.food = Food(self.land)
    def run(self):
        for ant in self.ants:
            ant.walk()
            self.checkBoundary(ant)
            ant.leaveSignal()
        
    def checkSuccess(self):
        for ant in self.ants:
            if self.getDistance(ant, self.food)<10:
                return True
        return False
    
    def getFoodPosition(self):
        return (self.food.x, self.food.y)
    
    def getDistance(self, lifea, lifeb):
        return sqrt((lifea.x-lifeb.x)**2+(lifea.y-lifeb.y)**2)
    
    def checkBoundary(self, ant):
        #Rule 1 Touch wall = cross    
        if (ant.x >= self.width):
            ant.x = 0
        elif(ant.y >= self.length):
            ant.y = 0
        elif(ant.x <= 0):
            ant.x = self.width
        elif(ant.y <= 0):
            ant.y = self.length    

