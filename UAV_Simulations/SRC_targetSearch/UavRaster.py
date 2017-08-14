'''
Created on Mar 20, 2017

@author: Doug Brown

Move Uav over raster path

7-25-17: added getPos() (135)
'''

import numpy as np
from numba.types import none
from numpy.linalg import norm
import copy

class UavRaster(object):
    '''
    classdocs
    '''
    
    params = none

    def __init__(self, params, uav_indx):
        '''
        Constructor
        '''
        # points for the uav to travel by
        self.path_points = []
        
        # next point indx in self.path_points for the uav to travel to
        self.next_indx = 0
        
        UavRaster.params = params
        
        
        
        
        # calculate all the raster x points
        # need two x points, as there will be a top and bottom
        # ergo the two appends
        x = []
        x.append(-params.radius_max)
        x.append(-params.radius_max)
        
        # needs to search till whole area can be covered
        while(x[len(x) - 1] < params.radius_max):
            new_x = x[len(x) - 1] + params.uav_fov
            x.append(new_x)
            x.append(new_x)
        
        # now generating y values to search over
        y = []
        for indx in range(0, len(x)):
            
            # for getter inner part of path completely covered 
            inner_x = x[indx] - np.sign(x[indx]) * params.uav_fov / 2
            
            # basically if odd of even
            # odd is on bottom of points, even is top
            if(indx % 2 == 0):
                new_y = np.sqrt(params.radius_search**2 - inner_x**2)
            else: 
                new_y = -np.sqrt(params.radius_search**2 - inner_x**2)
                
            # odd rows need to be switched
            if(np.floor(indx/2) % 2 != 0):
                new_y = new_y * -1
                
            y.insert(indx, new_y)
            
            # store points into class variable
            point = [x[indx], y[indx]]
            self.path_points.append(point)
        
        # now initialize class specific info
        # initial posiiton, chose a vertical line, then change direction if need to loop around
        x_indx = uav_indx * 2
        if(x_indx >= len(x)):
            x_indx - len(x)
            
            # different create different direction by operating on points
            self.shiftPoints()
            
             
        # set position
        x_pos = x[x_indx]
        
        self.position = [x_pos, 0]
        self.next_indx = uav_indx * 2 + 1
    
    
    # shift points, bascially just swaps pairs
    def shiftPoints(self):        
        for indx in range(0, int(len(self.path_points)/2)):
            temp = copy.deepcopy(self.path_points[2 * indx + 1])
            self.path_points[2*indx + 1] = self.path_points[2 * indx]
            self.path_points[2*indx] = temp
        

            
            
            
    # MOVE Z UAV HANS!!!
    def moveStep(self):
        
        # get direction and movement step uav
        direction = np.subtract(self.path_points[self.next_indx] , self.position)
        direction = np.divide(direction,norm(direction))
        shift = UavRaster.params.uav_speed / UavRaster.params.fps
        shift = np.multiply(direction, shift)
        
        # if reached next point
        if(norm(shift) >= norm(np.subtract(self.path_points[self.next_indx] , self.position))):
            self.next_indx += 1
            # if reached end of points, update array
            if(self.next_indx >= len(self.path_points)):
                
                # hard to explain, just work out example to figure out why this is
                self.path_points = np.flipud(self.path_points)
                self.shiftPoints()
                self.next_indx = 2
                
                
            # get direction and movement step uav
            direction = np.subtract(self.path_points[self.next_indx] , self.position)
            direction = np.divide(direction,norm(direction))
            shift = UavRaster.params.target_speed / UavRaster.params.fps
            shift = np.multiply(direction, shift)
        
        
        # update posistion
        self.position += shift
        
    # get posistion of UAV
    def getPos(self):
        return self.position
        






        