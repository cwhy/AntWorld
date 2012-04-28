from math import *

def distance(lifea, lifeb):
    return sqrt((lifea.x-lifeb.x)**2+(lifea.y-lifeb.y)**2)
    
def checkstatus1(movingobject,all_lives=[]):
    #Rule 1 Touch wall = cross    
    if (movingobject.x>=794):
        movingobject.x = 5
    elif(movingobject.y>=794):
        movingobject.y = 5
    elif(movingobject.x<=5):
        movingobject.x = 794
    elif(movingobject.y<=5):
        movingobject.y = 794
        
    
def checkstatus(movingobject, all_lives=[]):
    #Rule 1 Touch wall = die    
    if (movingobject.x>=794 or movingobject.y>=794 or movingobject.x<=5 or movingobject.y<=5):
        movingobject.alive = False