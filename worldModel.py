from life import Ant, Food, Land


class AntWorld:
    '''
    It contains the World Model
    '''
    def __init__(self, numOfAnts=1, width=800, length=800):
        self.time = 0
        self.numOfAnts = numOfAnts
        bgColor = (250, 250, 250)  # background color
        self.land = Land(width, length, bgColor)
        self.land.ants = [Ant(self.land) for i in range(numOfAnts)]
        self.land.food = Food(self.land)
        self.land.time = self.time
        self.land.bounce = True
        self.ants = self.land.ants
        self.food = self.land.food

    def run(self):
        self.time += 1
        self.land.time = self.time

    def checkSuccess(self):
 #       for ant in self.ants:
  #          if self.land.getDistanceAB(ant, self.food) < 15:
  #              return True
        return False
