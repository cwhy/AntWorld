import random
import physics 

def randomwalk(ant, food):
    turning_angle = random.gauss(0, 0.3)
    ant.move(turning_angle, 5)
    physics.checkstatus1(ant)
    
    if ant.alive == False: #Temporary setting: If it dies then stop the simulation
        return '2012'
    if physics.distance(ant, food) <= 10:
        return 'MissionComplete'
    return 'normal'
