'''
Created on Mar 15, 2017



@author: Doug Brown
'''
from numba.types import none
import random as rand
from cmath import sqrt
import numpy as np


class TargetRandom(object):
    '''
    classdocs
    '''
    
    # save params
    params = none

    def __init__(self, params):
        '''
        Constructor
        params: current parameters object
        
        initialize position and direction
        '''
        self.detected = False
        TargetRandom.params = params
        
        # target information
        # position is given by x,y coordinates
        # direction cartesian
        self.position = np.array([0.0,0.0])
        self.direction = np.array([0.0,0.0])
        
        # generate initial random position
        self.position[0] = params.radius_search * (2 * rand.random()  - 1) 
        self.position[1] = params.radius_search * (2 * rand.random()  - 1)
        while(self.getRadius() > TargetRandom.params.radius_search):
            self.position[0] = params.radius_search * (2 * rand.random() - 1)
            self.position[1] = params.radius_search * (2 * rand.random() - 1)
            
        # generate direction of travel
        self.newDirection()
        
    # distance from center
    def getRadius(self):
        return np.linalg.norm(self.position)

    # generate new direction for uav to travel along
    def newDirection(self):
        # generate random direction for target
        self.direction[0] = (2 * rand.random() - 1)
        self.direction[1] = (2 * rand.random() - 1)
        # normalize direction vector
        self.direction = self.direction / np.linalg.norm(self.direction)
        
        
    # make movement step
    def moveStep(self):
        # step amount
        shift = self.direction * TargetRandom.params.target_speed / TargetRandom.params.fps
        
        # check bounds
        while(np.linalg.norm(self.position + shift) > TargetRandom.params.radius_search):
            self.newDirection()
            # step amount
            shift = self.direction * TargetRandom.params.target_speed / TargetRandom.params.fps
        
        # make movement
        self.position += shift
        