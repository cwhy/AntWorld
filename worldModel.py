from life import Ant, Food, Land
from math import sqrt, pi
class AntWorld:
    '''
    It contains the World Model
    '''
    def __init__(self, numOfAnts=1, width=800, length=800):
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
            if self.getDistance(ant, self.food) < 15:
                return True
        return False
    
    def getFoodPosition(self):
        return (self.food.x, self.food.y)
    
    def getDistance(self, lifea, lifeb):
        return sqrt((lifea.x - lifeb.x) ** 2 + (lifea.y - lifeb.y) ** 2)
    
    def checkBoundary(self, ant, bounce=False):
        if (bounce == True):
            #Rule 1 Touch wall = bounce back like light
            if (int(ant.x) >= self.width - 1):
                ant.facingAngle = -ant.facingAngle - pi
                ant.x = self.width - 1
            elif (int(ant.x) <= 0):
                ant.facingAngle = -ant.facingAngle - pi
                ant.x = 0
            
            elif (int(ant.y) >= self.length - 1):
                ant.facingAngle = -ant.facingAngle
                ant.y = self.length - 1
            
            elif (int(ant.y) <= 0):
                ant.facingAngle = -ant.facingAngle
                ant.y = 0
            ant.facingAngle %= 2 * pi
        else:
            #Rule 2 Touch wall = cross
            ant.x %= self.width
            ant.y %= self.length
            
