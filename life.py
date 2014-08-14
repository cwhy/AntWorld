# !usr/bin/python
# Edited by
# Updated on

from __future__ import division
import random
from math import pi, cos, sin, sqrt, exp, fabs
import numpy as np
import colorsys


class LandElement(object):
    '''all kinds of things in land'''
    def __init__(self, land, x=0, y=0):
        self.land = land
        self.x = x
        self.y = y

    def getDistanceAB(self, A, B):
        return sqrt((A.x - B.x) ** 2 + (A.y - B.y) ** 2)

    def getDistanceB(self, B):
        return sqrt((self.x - B.x) ** 2 + (self.y - B.y) ** 2)

    def getSignal(self, signalType):
        return self.land.getSignalP(self.x, self.y, signalType)

    def getSignalByAngle(self, signalType, angle, maxDistance=50):
        # 50 is almost the max signal because if far the signal will be weak
        signalByAngle = 0.0
        for distance in range(2, maxDistance):
            x = self.x + cos(angle) * distance
            y = self.y + sin(angle) * distance
            if x < self.land.width - 1 and x > 0 and y < self.land.length - 1 and y > 0:
                signalByAngle += self.land.getSignalP(x, y, signalType)/(0.01 * distance + 1)
        return signalByAngle

    def updateSignal(self, signalType, amount=0):
        _x = self.x
        _y = self.y
        self.land.signal[signalType][_x, _y, 0] = amount + self.getSignal(signalType)
        self.land.signal[signalType][_x, _y, 1] = self.land.time

    def getPosition(self):
        return (self.x, self.y)

    def updatePosition(self, x, y):
        self.x = x
        self.y = y
        if self.land.tunnel:
            self.x = int(x) % self.width
            self.y = int(y) % self.length
        elif self.land.bounce:
            if x >= self.land.width - 1:
                self.x = self.land.width - 1
            if x <= 0:
                self.x = 0
            if y >= self.land.length - 1:
                self.y = self.land.length - 1
            if y <= 0:
                self.y = 0


class Life(LandElement):
    def __init__(self, land, x=0, y=0):
        super(Life, self).__init__(land)


class Animal(Life):
    def __init__(self, land):
        super(Animal, self).__init__(land)
        self.facingAngle = 0
        self.speed = 8

    def bounce(self, x, y, facingAngle):
        #Rule 1 Touch wall = bounce back like light
        if x >= self.land.width - 1 or x <= 0:
            self.facingAngle = -facingAngle - pi
            print "Pong!"
        if y >= self.land.length - 1 or y <= 0:
            self.facingAngle = -facingAngle
            print "Pong!"

        self.facingAngle %= 2 * pi

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
        self.facingAngle = facingAngle
        if self.land.bounce:
            self.bounce(x, y, facingAngle)
        self.updatePosition(x, y)

        #print "angle", self.facingAngle/pi*180

    def randomWalk(self,randomness=0.15):
        '''this is internal walking mechanism of ants which is supposed not exposed to user'''
        turning_angle = random.gauss(0, randomness)
        self.move(turning_angle, self.speed)


class Ant(Animal):
    def __init__(self, land):
        super(Ant, self).__init__(land)
        if 'Ant' not in land.signal:
            land.newSignal('Ant')
            land.signalColors['Ant'] = 0.5  # Hue of the ant signal
        self.home = LandElement(land, 0, 0)
        self.searchMode = True  # For patrol testing
        self.hasFood = False
        self.viewRange = 2*pi
        self.viewMaxDistance = 30
        self.signalSensitivity = 20
        self.signalIntensity = 100
        # Right direction is 0, anticlockwise positive

    def __call__(self):
        self.patrol()
        self.leaveSignal()

    def detectSignalC(self):
        '''return the angle of a strong signal in front of the ant '''
        centerism = 1.0  # MAX 2 The tendency of going forward, the larger the more centered
        sideAngle = int((0.5 * self.viewRange) * self.viewMaxDistance)
        # viewResolution = 1 / self.viewMaxDistance theta is about actan(theta) when theta is small
        maxAngle = self.facingAngle
        maxSignal = 0
        for a in range(-sideAngle, sideAngle):
            angle = float(a)/self.viewMaxDistance + self.facingAngle
            signal = self.getSignalByAngle('Ant', angle, self.viewMaxDistance)
            signal *= 1 - centerism * fabs(a)/sideAngle
            if signal > maxSignal:
                maxSignal = signal
                maxAngle = angle
            # print angle, signal
        if maxSignal <= 0.1:
            return None
        else:
            #print "signal",maxSignal, "angle", maxAngle
            return maxAngle

    def followSignal(self):
        '''follow the signal...'''
        preferedSignal = self.detectSignalC()
        if preferedSignal is not None:
            turning_angle = preferedSignal - self.facingAngle
            self.move(turning_angle, self.speed)
            # print "following!"
        else:
            print "No signal..."
            #self.randomWalk(0.1)

    def patrol(self):
        '''The algorithm to let the ant patrol'''
        if (not self.hasFood) and self.getDistanceB(self.land.food) < 20:  # Turn back
            self.facingAngle = (pi + self.facingAngle) % (2*pi)
            self.searchMode = False
            self.hasFood = True
            self.followSignal()
            print "Found! Turing back"
        elif self.hasFood and self.getDistanceB(self.home) < 5:  # Go to food again
            self.facingAngle = (pi + self.facingAngle) % (2*pi)
            self.hasFood = False
            self.followSignal()
        else:
            if self.searchMode:  # Find food
                self.randomWalk()
            else:
                self.followSignal()

    def leaveSignal(self):
        '''leave traces after walking'''
        self.updateSignal('Ant', self.signalIntensity)


class Food(Life):
    def __init__(self, land):
        Life.__init__(self, land)
        self.x, self.y = 300, 300


class Land:
    def __init__(self, width, length, bgColor):
        self.length = length
        self.width = width
        self.bounce = True
        self.tunnel = False
        self.time = 0
        self.signal = dict()
        self.bgColor = bgColor
        self.signalColors = dict()  # Hue of the signal
        self.color = np.tile(bgColor, (self.width, self.length, 1))

    def newSignal(self, signalType):
        self.signal[signalType] = np.zeros((self.width, self.length, 2))

    def getSignalP(self, x, y, signalType):
        a = 0.005  # Larger -> faster
        b = 0.0
        dtime = float(self.time - self.signal[signalType][x, y, 1])
        _decaycoef = exp(-a * (dtime)) + b
        return _decaycoef * self.signal[signalType][x, y, 0]

    def getColorP(self, x, y):  # get the color of point x, y
        self.updateColorP(x, y)
        return self.color[x,y,:]

    def getColorB(self, X, Y):  # get the color of block X, Y
        self.updateColorB(X, Y)
        C = self.color[np.ix_(X,Y)]
        return C

    def getColorAll(self):  # get the color of block X, Y
        self.updateColorAll()
        return self.color

    def updateColorP(self, x, y):
        _colors = list()
        for signalType in self.signalColors.keys():
            _h = self.signalColors[signalType]
            _v = min(self.getSignalP(x,y,signalType), 100)/100
            _colors.append((_v, _h, 1))
        (v, h, s) = max(_colors)
        _mainColor = 255*colorsys.hsv_to_rgb(h, s, v)
        self.color[x,y,:] = _mainColor

    def updateColorB(self, X, Y):
        _Vs = list()
        Min = np.vectorize(min)
        for signalType in self.signalColors.keys():
            # _h = self.signalColors[signalType]
            _Vs.append(Min(self.getSignalB(X,Y,signalType), 100)/100)
        V = sum(_Vs)
        blockRGB = np.vectorize(colorsys.hsv_to_rgb)
        k = 255*blockRGB(0.5, 0.5, V)
        self.color[:,:,0] = k[0][:,:]
        self.color[:,:,1] = k[1][:,:]
        self.color[:,:,2] = k[2][:,:]

    def updateColorAll(self):
        _Vs = list()
        Min = np.vectorize(min)
        for signalType in self.signalColors.keys():
            # _h = self.signalColors[signalType]
            _Vs.append(Min(self.getSignalAll(signalType), 100)/100)
        V = sum(_Vs)
        S = np.ones(V.shape)
        S[V == 0] = 0
        H = np.ones(V.shape)
        H[V == 0] = 0.5
        V = 1 - V
        blockRGB = np.vectorize(colorsys.hsv_to_rgb)
        k = blockRGB(H, S, V)
        for i in range(3):
            self.color[:,:,i] = 255*k[i][:,:]

    def getSignalB(self, X, Y, signalType):
        a = 0.005  # Larger -> faster
        b = 0.0
        dtime = self.time - self.signal[signalType][np.ix_(X,Y,[1])]
        _decaycoef = np.exp(-a * (dtime)) + b
        return _decaycoef * self.signal[signalType][np.ix_(X,Y,[0])]

    def getSignalAll(self, signalType):
        a = 0.005  # Larger -> faster
        b = 0.0
        dtime = self.time - self.signal[signalType][:,:,1]
        _decaycoef = np.exp(-a * (dtime)) + b
        return _decaycoef * self.signal[signalType][:,:,0]
