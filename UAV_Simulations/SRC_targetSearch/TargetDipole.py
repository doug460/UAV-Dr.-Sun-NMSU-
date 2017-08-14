'''
Created on Mar 23, 2017

@author: Doug Brown

The purpose of this is to move the target in such a way that it avoids the uavs 
The uavs will be seen as a dipole, with positive in front and negative in back
The target will be treated as also being positively charged and move accordingly 
'''
from numba.types import none
import numpy as np
import random as rand
from cmath import sqrt
import copy
from numpy.linalg import norm

class TargetDipole(object):
    '''
    classdocs
    '''
    # this is the length for seperatoin between the charges
    dipoleSeperation = 10
    

    
    
    

    def __init__(self, params):
        '''
        Constructor
        '''
        self.detected = False
        self.params = params
        
        # negative and positive chargets
        self.neg_charges = []
        self.pos_charges = []
        
        # target information
        # position is given by x,y coordinates
        # direction cartesian
        self.position = np.array([0.0,0.0])
        self.direction = np.array([0.0,0.0])
        
        # generate initial random position
        self.position[0] = params.radius_search * (2 * rand.random()  - 1) 
        self.position[1] = params.radius_search * (2 * rand.random()  - 1)
        while(self.getRadius() > self.params.radius_search):
            self.position[0] = params.radius_search * (2 * rand.random() - 1)
            self.position[1] = params.radius_search * (2 * rand.random() - 1)

        
    # if uav direction is known, move based on potential field, else dont move
    def moveStep(self):
        # if no charges saved, create charges
        if(len(self.pos_charges) == 0):
            uavs = self.params.uavs
            for uav in uavs:
                self.neg_charges.append(copy.deepcopy(uav.position))
                self.pos_charges.append(copy.deepcopy(uav.position))
        # else move based on charges
        else:
            self.updateCharges()
            direction = self.getSuperposition()
            
            # shift amount
            shift = direction * self.params.target_speed / self.params.fps
            
            # if position with shift is within bound, move uav
            if(norm(shift + self.position) < self.params.radius_search):
                self.position += shift
            
    
    # get uav direction and seperate charges accordingly 
    def updateCharges(self):
        uavs = self.params.uavs
        for indx in range(0,len(uavs)):
            self.neg_charges[indx] = copy.deepcopy(self.pos_charges[indx])
            self.pos_charges[indx] =  copy.deepcopy(uavs[indx].position)
  
    
    # get superposiiton of forces from charges
    def getSuperposition(self):
        # summ up forces
        force = [0.0, 0.0]
        uavs = self.params.uavs
        for indx in range(0,len(self.pos_charges)):
            # gets direction of moment
            direction = np.subtract(self.pos_charges[indx], self.neg_charges[indx])
            direction = direction/norm(direction)
            
            # places charges at seperation around uav
            pos_charge = np.add(uavs[indx].position, np.multiply(direction, TargetDipole.dipoleSeperation/2))
            neg_charge = np.subtract(uavs[indx].position, np.multiply(direction, TargetDipole.dipoleSeperation/2))
            
            # add positive force
            direction = np.subtract(self.position, pos_charge)
            # divide diretion by distance to first normalize, then follow 1/r^2 for the other two powers
            force += np.array(np.divide(direction, norm(direction)**3))
            
            # add negative force
            direction = np.subtract(neg_charge, self.position)
            # divide diretion by distance to first normalize, then follow 1/r^2 for the other two powers
            force += np.array(np.divide(direction, norm(direction)**3))
        
        # add force pulling it to center
        #force -= self.position/(norm(self.position)**4)
        
        # return directoin of net force        
        force = force/norm(force)
        return(force)
    
    # got distance from center
    def getRadius(self):
        return np.linalg.norm(self.position)
    
            
            
            
            
            
        