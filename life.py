import random
from math import pi, cos, sin, sqrt, exp, fabs

class Life:
    def __init__(self, land, x=0, y=0):
        self.x = x
        self.y = y
        self.land = land
        
    def getLandElement(self):
        element = self.land.getElement(self.x, self.y)
        if element == None:
            print self.x, self.y
            raise "???"
        else:
            return element

class Ant(Life):
    def __init__(self, land):
        Life.__init__(self, land)
        self.facingAngle = 0

        self.home = land.element[0][0]
        self.searchMode = True #For patrol testing
        self.hasFood = False
        
        self.speed = 8
        self.viewRange = 2*pi
        self.viewMaxDistance = 30
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
        #print "angle", self.facingAngle/pi*180
        
    def randomWalk(self,randomness=0.15):
        '''this is internal walking mechanism of ants which is supposed not exposed to user'''
        turning_angle = random.gauss(0, randomness)
        self.move(turning_angle, self.speed)
        
    def detectSignal(self):
        '''return the angle of the signal of the strongest direction'''
        sideAngle = int((0.5 * self.viewRange) * self.viewMaxDistance)# viewResolution = 1 / self.viewMaxDistance theta is about actan(theta) when theta is small
        maxAngle = self.facingAngle
        maxSignal = 0
        for a in range(-sideAngle, sideAngle):
            angle = float(a)/self.viewMaxDistance + self.facingAngle
            signal = self.land.getElement(self.x, self.y).getSignalByAngle(angle, self.viewMaxDistance)
            if signal > maxSignal:
                maxSignal = signal
                maxAngle = angle
            #print angle, signal
        if maxSignal <= 0.1:
            return None
        else:
            #print "signal",maxSignal, "angle", maxAngle
            return maxAngle
    
    def detectSignalC(self):
        '''return the angle of a strong signal in front of the ant '''
        centerism = 1.0 # MAX 2 The tendency of going forward, the larger the more centered
        sideAngle = int((0.5 * self.viewRange) * self.viewMaxDistance)# viewResolution = 1 / self.viewMaxDistance theta is about actan(theta) when theta is small
        maxAngle = self.facingAngle
        maxSignal = 0
        for a in range(-sideAngle, sideAngle):
            angle = float(a)/self.viewMaxDistance + self.facingAngle
            signal = self.land.getElement(self.x, self.y).getSignalByAngle(angle, self.viewMaxDistance)
            signal *= 1 - centerism * fabs(a)/sideAngle
            if signal > maxSignal:
                maxSignal = signal
                maxAngle = angle
            print angle, signal
        if maxSignal <= 0.1:
            return None
        else:
            #print "signal",maxSignal, "angle", maxAngle
            return maxAngle
        
    def followSignal(self):
        '''follow the signal...'''
        preferedSignal = self.detectSignalC()
        if  preferedSignal != None:
            turning_angle = preferedSignal - self.facingAngle
            self.move(turning_angle, self.speed)
            print "following!"
        else:
            print "No signal..."
            #self.randomWalk(0.1)
            
    def patrol(self):
        '''The algorithm to let the ant patrol'''
        if (not self.hasFood) and self.land.getDistanceAB(self, self.land.food) < 20:#Turn back
            self.facingAngle = (pi + self.facingAngle) % (2*pi)
            self.searchMode = False
            self.hasFood = True
            self.followSignal()
            print "Found! Turing back"
        elif self.hasFood and self.land.getDistanceAB(self, self.home) < 5: #Go to food again
            self.facingAngle = (pi + self.facingAngle) % (2*pi)
            self.hasFood = False
            self.followSignal()
        else:
            if  self.searchMode: #Find food
                self.randomWalk()
            else:
                self.followSignal()
                print self.hasFood
            
        
    def leaveSignal(self):
        '''leave traces after walking'''
        element = self.getLandElement()
        element.gainSignal()

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
        self.antSignal = [0.0,0] # the tracing signal of ants, time of signal
        
        
    def calcDecayedSignal(self,time):
        a = 0.005 #Larger -> faster
        b = 0.0
        
        dtime = float(time - self.antSignal[1])
        #    if self.antSignal[0] != 0:
        #print dtime, "bfo",self.antSignal[0],"aft:", int((exp(-a * dtime) + b) * self.antSignal[0])  
        return (exp(-a * (dtime)) + b) * self.antSignal[0]    
    
    
    def getSignal(self):
        if self.antSignal[1] == 0: #No time records of signal
            return 0
        else:
            #print time, self.antSignal[1]
            return self.calcDecayedSignal(self.land.time)

    def getSignalByAngle(self,angle,maxDistance = 50):#50 is almost the max signal because if far the signal will be weak
        signalByAngle = 0.0
        for distance in range(2, maxDistance):
            x = self.x + cos(angle) * distance
            y = self.y + sin(angle) * distance
            e = self.land.getElement(x, y)
            if e != None:#not out of boundary
                signalByAngle += e.getSignal()/(0.01 * distance + 1)
        return signalByAngle

    def gainSignal(self, amount = 100.0):
            self.antSignal[0] = amount + self.getSignal()
            self.antSignal[1] = self.land.time
    
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
        if self.bounce == True:
            if int(x) >= 0 and int(y) >= 0 and int(x) <= self.width - 1 and int(y) <= self.length - 1:
                return self.element[int(x)][int(y)]
            else:
                #print x, y, int(x), int(y)
                return None
        else:
            return self.element[int(x)%self.width][int(y)%self.length]
    
