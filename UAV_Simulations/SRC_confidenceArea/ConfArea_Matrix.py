'''
Created on Sep 3, 2017

@author: DougBrownWin
'''
import numpy as np
import Variables as varis
import math

class ConfArea_Matrix(object):
    '''
    classdocs
    
    this is the matrix for confidence area
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        # there is a scale factor for the area
        # going to include 110% of searchable area
        radius_search = varis.params.get_radiusSearch(varis.uavs_max)
        self.real2matrix = (varis.matrix_dim / 2) / (radius_search * 1.1)
        self.matrix2real = 1 / self.real2matrix
        
        
        # matrix for 
        self.matrix = np.zeros((varis.matrix_dim, varis.matrix_dim))
        
        # time for target to travel one block
        self.time_targetStep = self.matrix2real / varis.target_speed
        
        # step counter for time stuff... see code at bottom
        self.time_stepCount = 0
        
        
    # get the area value for the confidence area
    def get_areaSize(self):
        sum = np.sum(self.matrix)
        area = sum * (self.matrix2real ** 2)
        return area     
    
    # get matrix
    def get_matrix(self):
        return self.matrix
        
        
    # update environement matrix
    def update_area(self, uavs):
        
        # center of search area
        center = [varis.matrix_dim / 2, varis.matrix_dim / 2]

        # going to decrease matrix first, then update matrix based on UAV pos                        
        
        # update entire matrix when target could have traveled one block
        if(varis.params.current_time / self.time_targetStep > self.time_stepCount):
            self.time_stepCount += 1
            
            # step through all cells
            # starting at 1 and stopping 1 short so as to avoid edges... dont need to check them
            for row in range(1, varis.matrix_dim - 1, 1):
                for column in range(1,varis.matrix_dim - 1, 1):
                    
                    # so update to 0.5, only update based on zeros
                    # then at end make all 0.5s down to zero.
                    # keeps current changes from effect matrix as i step through it
                    
                    # check near zero cell
                    # only updating 1 cells
                    if(self.matrix[row,column] == 1):
                        if(self.matrix[row - 1,column] == 0):
                            self.matrix[row,column] = 0.5
                            
                        if(self.matrix[row + 1,column] == 0):
                            self.matrix[row,column] = 0.5
                            
                        if(self.matrix[row,column - 1] == 0):
                            self.matrix[row,column] = 0.5
                            
                        if(self.matrix[row,column + 1] == 0):
                            self.matrix[row,column] = 0.5
                            
            # again step through matrix and push changes into matrix
            for row in range(1, varis.matrix_dim - 1, 1):
                for column in range(1,varis.matrix_dim - 1, 1):
                    
                    if(self.matrix[row,column] == 0.5):
                        self.matrix[row,column] = 0
                    
            
            
        # update for uavs
        for uav in uavs:
            position = np.multiply(uav.getPos(), self.real2matrix) + center
            
            # where to start update scheme
            topLeft_corner = []
            topLeft_corner.insert(0, math.floor(position[0] - varis.uav_fov * self.real2matrix / 2) )
            topLeft_corner.insert(1, math.floor(position[1] - varis.uav_fov * self.real2matrix / 2) )
            
            # +1: make sure to look over entire matrix
            side_length = math.ceil(varis.uav_fov * self.real2matrix + 1)
            
            # step through matrix
            for row in range(topLeft_corner[0], topLeft_corner[0] + side_length, 1):
                for column in range(topLeft_corner[1], topLeft_corner[1] + side_length, 1):
                    
                    # radius from UAV
                    radius = np.linalg.norm([row,column] - position)
                    
                    # update uncertainty
                    if(radius < (varis.uav_fov * self.real2matrix / 2)):
                        self.matrix[row,column] = 1;





