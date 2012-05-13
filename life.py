import random
from math import pi, cos, sin, atan

class Life:
    def __init__(self, land):
        self.x = 0
        self.y = 0
        self.land = land
        
    def getLandElement(self):
        return self.land.getElement(self.x, self.y)

class Ant(Life):
    def __init__(self, land):
        Life.__init__(self, land)
        self.facingAngle = 0
        self.signalSensitivity = 20
        # Right direction is 0, anticlockwise positive
        
    def walk(self):
        '''random walk with step length 5 and random parameter 0.3'''
        if not self.detectSignal():
            self.randomWalk()
        
    def randomWalk(self):
        '''this is internal walking mechanism of ants which is supposed not exposed to user'''
        turning_angle = random.gauss(0, 0.3)
        self.move(turning_angle, 5)
    
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

    def detectSignal(self):
        '''return true if signal detected in adjacent elements and move towards the signal'''
        sight = self.getSight()
        for element in sight:
            if element.antSignal > self.signalSensitivity:
                x, y = element.x, element.y
                if x-self.x == 0 and y-self.y < 0:
                    self.facingAngle = 3*pi/2
                elif x-self.x == 0 and y-self.y > 0:
                    self.facingAngle = pi/2
                elif x-self.x < 0:
                    self.facingAngle = atan((y-self.y) / (x-self.x)) + pi
                else:
                    self.facingAngle = atan((y-self.y) / (x-self.x))
                self.move(0, 1)
                print "Detect!"
                return True
        return False
        
    def leaveSignal(self):
        '''leave traces after walking'''
        element = self.getLandElement()
        element.gainSignal(100)
        element.diffuseSignal()

    def getSight(self):
        '''get landElements in the sight'''
        s = 2
        x = self.x + s*cos(self.facingAngle)
        y = self.y + s*sin(self.facingAngle)
        return self.land.getAdjacentElements(x, y)
    
class Food(Life):
    def __init__(self, land):
        Life.__init__(self, land)
        self.x, self.y = 400, 400

class LandElement:
    '''all kinds of infomation in land'''
    def __init__(self, land, x, y):
        self.land = land
        self.x = x
        self.y = y
        self.antSignal = 0 # the tracing signal of ants
        self.color = (200, 200, 200) # Used for testing
    
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
                self.gainSignal(-amount)
                element.diffuseSignal()

    def gainSignal(self, amount = 100):    
        self.antSignal += amount
    

class Land:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.element = []
        for x in range(0,length):
            column = []
            for y in range(0,width):
                column.append(LandElement(self, x, y))
            self.element.append(column)
            
    def getElement(self, x, y):
        '''getLandElement at x, y, (x, y need not to be integer)'''
        return self.element[int(x) % self.width][int(y) % self.length]
    
    def getAdjacentElements(self, x, y):
        s = 2 # size of adjacent
        adjacent = []
        for i in range(int(x-s), int(x+s)):
            for j in range(int(y-s), int(y+s)):
                if i != x or j != y:
                    adjacent.append(self.getElement(i % self.width, j % self.length))
        return adjacent
