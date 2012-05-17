from life import Ant, Food, Land
from math import pi
class AntWorld:
    '''
    It contains the World Model
    '''
    def __init__(self, numOfAnts=1, width=800, length=800):
        self.time = 0
        self.numOfAnts = numOfAnts
        self.land = Land(width, length)
        self.land.ants = [Ant(self.land) for i in range(numOfAnts)]
        self.land.food = Food(self.land)
        self.land.time = self.time
        self.ants = self.land.ants
        self.food = self.land.food
        
    def run(self):
        for ant in self.ants:
            ant.patrol()
            self.checkBoundary(ant, True)
            ant.leaveSignal(self.time)
        self.time += 1
        self.land.time = self.time
        
    def checkSuccess(self):
 #       for ant in self.ants:
  #          if self.land.getDistanceAB(ant, self.food) < 15:
  #              return True
        return False
    
    
    
    def checkBoundary(self, ant, bounce=False):
        if (bounce == True):
            #Rule 1 Touch wall = bounce back like light
            if (int(ant.x) >= self.land.width - 1):
                ant.facingAngle = -ant.facingAngle - pi
                ant.x = self.land.width - 1
            elif (int(ant.x) <= 0):
                ant.facingAngle = -ant.facingAngle - pi
                ant.x = 0
            
            elif (int(ant.y) >= self.land.length - 1):
                ant.facingAngle = -ant.facingAngle
                ant.y = self.land.length - 1
            
            elif (int(ant.y) <= 0):
                ant.facingAngle = -ant.facingAngle
                ant.y = 0
            ant.facingAngle %= 2 * pi
        else:
            #Rule 2 Touch wall = cross
            ant.x %= self.land.width
            ant.y %= self.length
            
