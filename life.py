# !usr/bin/python
# Edited by
# Updated on

from __future__ import division
import random
from math import pi, cos, sin, sqrt, fabs
import numpy as np
import colorsys
from skimage.color import hsv2rgb


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

    def getSignalByAngle(self, signalType, angle, maxDistance):
        _distance = np.array(range(2, maxDistance))
        X = (self.x + cos(angle) * _distance).astype(np.uint16, copy=False)
        Y = (self.y + sin(angle) * _distance).astype(np.uint16, copy=False)
        _cond = (X < self.land.width - 1) * (X > 0) * (Y < self.land.length - 1) * (Y > 0)
        X = X[_cond]
        Y = Y[_cond]
        _distance = _distance[_cond]

        # _getSignalXY = np.vectorize(self.land.getSignalP)
        if len(_distance) == 0:
            return 0
        else:
            # _idx = np.ix_(X,Y,[0])
            return np.sum(self.land.getSignalB(X, Y, signalType)/(0.01 * _distance + 1))
            # signalByAngle = np.sum(_getSignalXY(X, Y, signalType)/(0.01 * _distance + 1))

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
            #print "signal", maxSignal, "angle", maxAngle
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
        return self.signal[signalType][x, y, 0]

    def getColorP(self, x, y):  # get the color of point x, y
        return self.color[x,y,:]

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

    def updateColorAll(self):
        _Vs = list()
        for signalType in self.signalColors.keys():
            _v = self.signal[signalType][:,:,0]
            _v[_v > 100] = 100
            _Vs.append(_v/100)
        V = sum(_Vs)
        S = np.ones(V.shape)
        S[V == 0] = 0
        H = np.ones(V.shape)
        H[V == 0] = 0.5
        V = 1 - V
        HSV = np.dstack((H, S, V))
        self.color = 255*hsv2rgb(HSV).astype(np.uint8, copy=False)

    def updateSignalAll(self):
        for signalType in self.signalColors.keys():
            a = 0.005  # Larger -> faster
            b = 0.0
            dtime = self.time - self.signal[signalType][:,:,1]
            _decaycoef = np.exp(-a * (dtime)) + b
            self.signal[signalType][:,:,0] *= _decaycoef

    def getSignalAll(self, signalType):
        return self.signal[signalType][:,:,0]

    def getSignalB(self, X, Y, signalType):
        _idx = np.ix_(X,Y,[0])
        return self.signal[signalType][_idx]
