import random
from math import pi, cos, sin, sqrt

class Life:
    def __init__(self, land, x=0, y=0):
        self.x = x
        self.y = y
        self.land = land
        
    def getLandElement(self):
        return self.land.getElement(self.x, self.y)

class Ant(Life):
    def __init__(self, land):
        Life.__init__(self, land)
        self.facingAngle = 0

        self.home = land.element[0][0]
        self.searchMode = True #For patrol testing
        self.hasFood = False
        
        self.speed = 8
        self.viewRange = pi*5/6
        self.viewMaxDistance = 50
        self.signalSensitivity = 20
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
        print "angle", self.facingAngle/pi*180
        
    def randomWalk(self):
        '''this is internal walking mechanism of ants which is supposed not exposed to user'''
        turning_angle = random.gauss(0, 0.2)
        self.move(turning_angle, self.speed)
        
    def detectSignal(self):
        '''return the angle of the signal of the strongest direction'''
        sideAngle = int((0.5 * self.viewRange) * self.viewMaxDistance)# viewResolution = 1 / self.viewMaxDistance theta is about actan(theta) when theta is small
        maxAngle = self.facingAngle
        maxSignal = 0
        for a in range(-sideAngle, sideAngle):
            for distance in range(0, self.viewMaxDistance):
                x = sin(a) * distance
                y = cos(a) * distance
                s = self.land.getElement(x, y).antSignal          
                if s > maxSignal:
                    maxSignal = s
                    maxAngle = a
        if maxSignal <= 10:
            return None
        else:
            print "signal",maxSignal
            return maxAngle
        
    def followSignal(self):
        '''follow the signal...'''
        if self.detectSignal() != None:
            turning_angle = self.detectSignal() - self.facingAngle
            self.move(turning_angle, self.speed)
            print "following!"
        else:
            print "still no signal..."
            self.randomWalk()
            
    def patrol(self):
        if (not self.hasFood) and self.land.getDistanceAB(self, self.land.food) < 100:#Turn back
            self.facingAngle = (pi + self.facingAngle) % (2*pi)
            self.searchMode = False
            self.hasFood = True
            self.followSignal()
            print "Found! Turing back"
        elif self.hasFood and self.land.getDistanceAB(self, self.home) < 100: #Go to food again
            self.facingAngle = (pi + self.facingAngle) % (2*pi)
            self.hasFood = False
            self.followSignal()
        else:
            if  self.searchMode: #Find food
                self.randomWalk()
            else:
                self.followSignal()
            
            
        
    def leaveSignal(self):
        '''leave traces after walking'''
        element = self.getLandElement()
        element.gainSignal(100)
        element.diffuseSignal()

class Food(Life):
    def __init__(self, land):
        Life.__init__(self, land)
        self.x, self.y = 400, 400
    def getPosition(self):
        return (self.x, self.y)

class LandElement:
    '''all kinds of information in land'''
    def __init__(self, land, x, y):
        self.land = land
        self.x = x
        self.y = y
        self.antSignal = 0 # the tracing signal of ants
        
        
    def getAdjacentElements(self):
        return self.land.getAdjacentElements(self.x, self.y)
    
    def diffuseSignal(self):
        diffuseRatio = 0.1
        diffuseThreshold = 2
        
        adjacent = self.getAdjacentElements()
        for element in adjacent:
            amount = self.antSignal * diffuseRatio / len(adjacent)
            if amount >= diffuseThreshold:
                element.gainSignal(amount)
                self.gainSignal(-amount-10)
                element.diffuseSignal()

    def gainSignal(self, amount = 100):    
        self.antSignal += amount
    
class Land:
    def __init__(self, width,length):
        self.length = length
        self.width = width
        self.element = []
        for x in range(0,length):
            column = []
            for y in range(0,width):
                column.append(LandElement(self, x, y))
            self.element.append(column)
            
    def getDistanceAB(self, A, B):
        return sqrt((A.x - B.x) ** 2 + (A.y - B.y) ** 2)
    
    def getElement(self, x, y):
        '''getLandElement at x, y, (x, y need not to be integer)'''
        return self.element[int(x)][int(y)]
    
    def getAdjacentElements(self, x, y):
        s = 2 # size of adjacent
        adjacent = []
        for i in range(int(x-s), int(x+s)):
            for j in range(int(y-s), int(y+s)):
                if i != x or j != y:
                    adjacent.append(self.getElement(i % self.width, j % self.length))
        return adjacent
