'''
Created on Sep 3, 2017

@author: DougBrownWin

this is version 2, so including effects of diagonal reduction of matrix
'''
import numpy as np
import Variables as varis
import math
from scipy import signal

# set matrix to this value when area is observed
# specifically this value because abs = 1
matrix_ratio = 1/math.sqrt(2)
detected_value = (1 + 1j)*matrix_ratio 


class ConfArea_Matrix_v2(object):
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
        self.matrix = np.zeros((varis.matrix_dim, varis.matrix_dim), dtype = np.complex)
        
        # time for target to travel one step
        self.time_step = 1 / varis.fps
        
        # step counter for time stuff... see code at bottom
        self.time_stepCount = 0
        
        # matrix to hold indexs of ones
        self.ones = np.zeros((varis.matrix_dim, varis.matrix_dim))
        
        
        # values for how quickly upDown and Diagonals should reduce
        # keep as positive amount 
        self.reduce_upDowns = matrix_ratio * varis.target_speed / (varis.fps * self.matrix2real)
        self.reduce_diagonals = 1j * matrix_ratio * varis.target_speed / (varis.fps * self.matrix2real) / math.sqrt(2)
                
        
    # get the area value for the confidence area
    def get_areaSize(self):
        sum = np.sum(np.abs(self.matrix))
        area = sum * (self.matrix2real ** 2)
        return area  
    
    # get area matrix
    def get_matrix(self):
        return np.abs(self.matrix)
    
    # get diagonal edges of array
    # returns bool of edges
    #
    # diaginal down -1, shift up and left
    # diag up +1 shift up,
    #     -1 shift left
    #
    # diaganols reduce imaginary by specified amount
    # linears reduce real
    def get_diagonals(self, array):
        diag1 = np.array([[1,0],[0,-1]])
        diag2 = np.array([[0,-1],[1,0]])
        
        shape = array.shape
        
        # get diag1
        conv3 = signal.convolve2d(array, diag1, mode='full')
        
        temp1 = np.roll(conv3 < 0, -1, axis = 0)
        temp1 = np.roll(temp1, -1, axis = 1)
        temp1 = np.add(temp1,conv3 == 1)
        temp1 = temp1[0:shape[0], 0:shape[1]]
        
    
        # get diag2
        conv4 = signal.convolve2d(array, diag2, mode='full')
        
        indx_plus = np.roll(conv4 > 0, -1, axis = 0)[0:shape[0], 0:shape[1]]
        indx_minus = np.roll(conv4 < 0, -1, axis = 1)[0:shape[0], 0:shape[1]]
        
        # get combined output and return values
        out = np.add(temp1, np.add(indx_plus, indx_minus))
        
        return(out)
       
    # get up down edges of array
    # returns bool of edges
    #    
    # vertical -1 shift up
    # horizontal -1 shift left
    def get_upDowns(self, array):
        
        # right edges are at the one, left edges are right 1
        horiz = np.array([[1,-1]])
        vert = np.array([[1],[-1]])
        
        shape = array.shape
        
        
        # get convolution of horizontal edges
        conv1 = signal.convolve2d(array, horiz, mode='full')
         
        temp1 = np.roll(conv1 < 0, -1, axis = 1)
    
        temp1 = np.add(temp1,conv1 == 1)
        temp1 = temp1[0:shape[0], 0:shape[1]]
          
        # get convolution of verticle edges
        conv2 = signal.convolve2d(array, vert, mode='full')
         
        temp2 = np.roll(conv2 < 0, -1, axis = 0)
        temp2 = np.add(temp2,conv2 == 1)
        temp2 = temp2[0:shape[0], 0:shape[1]]
        
        # combine edges and return bools
        out = np.add(temp2, temp1)
        
        return(out[0:array.shape[0],0:array.shape[1]])
        
        
    # update environement matrix
    def update_area(self, uavs):
        
        # center of search area
        center = [varis.matrix_dim / 2, varis.matrix_dim / 2]

        # going to decrease matrix first, then update matrix based on UAV pos                        
        
        # get matrix of ones for non-zero elemenents
        self.ones[:,:] = 0
        self.ones[np.add(self.matrix.real > 0, self.matrix.imag > 0)] = 1
        
        
        # get horiz vertical edges and reduce my set amount
        self.matrix[self.get_upDowns(self.ones)] -= self.reduce_upDowns
        
        # get verticals and reduce by set amount
        self.matrix[self.get_diagonals(self.ones)] -= self.reduce_diagonals
        
        # set  negatives to zero
        self.matrix[np.add(self.matrix.real < 0, self.matrix.imag < 0)] = 0
                    
            
            
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
                        self.matrix[row,column] = detected_value;
                        
                        
    # basically want to et search area size for ;lotting
    def getSearchEdge(self):
        return self.matrix2real * varis.matrix_dim
    
    
    
    
    
    
    
    
    
         
                        
    





