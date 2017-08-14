'''
Created on Jul 25, 2017

@author: Doug Brown
basically really similar to TargetAttack in attack_simulaiton
difference it is initialized with direction and location, then moves in that direction
'''
from numba.types import none
import numpy as np

class TargetGeneric(object):
    '''
    classdocs
    '''
    params = none


    def __init__(self, params, position, direction):
        '''
        Constructor
        '''
        TargetGeneric.params = params
        
        # set position and direction
        self.position = position
        self.direction = direction
        
        
    # get position of target
    def getPos(self):
        return self.position
    
    
    # move target in direction 
    def moveStep(self):
        # basically get radial vector, and move towards center by step amount
        shift = self.direction * TargetGeneric.params.target_speed / TargetGeneric.params.fps
        self.position += shift
        