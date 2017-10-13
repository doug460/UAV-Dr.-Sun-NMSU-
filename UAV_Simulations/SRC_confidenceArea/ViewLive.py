'''
Created on Sep 3, 2017

@author: DougBrownWin

program for viewing stuff live
'''

import Variables as varis
import matplotlib.pyplot as plt
import numpy as np
import math

class ViewLive(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        # step size in time and visualize counter
        self.time_frameStep = 1 / varis.view_liveFPS
        self.time_counter = 0
        
        plt.ion()
    
    
    # plot live view of matrix area
    def plotLive(self, matrix, uavs):
        
        # basically plot at frame rate
        if(varis.params.current_time / self.time_frameStep > self.time_counter):
            self.time_counter += 1
            
            # matrix dimension
            dim = varis.matrix_dim
            
            # image to be plotted
            dim_half = math.floor(dim/varis.view_liveDownSample)
            image = np.zeros((dim_half, dim_half))
            
            # downsample half of size
            for row in range(0,dim,varis.view_liveDownSample):
                for column in range(0,dim,varis.view_liveDownSample):
                    image[math.floor(row/varis.view_liveDownSample),math.floor(column/varis.view_liveDownSample)] = matrix.get_matrix()[row, column]
                    
            
            # plot that shit
            plt.imshow(image)
            
            # get current radius percent
            radius = np.linalg.norm(uavs[0].getPos())
            radius_percent = 100 * radius / varis.params.radius_max 
            plt.title('Radius %3.0f%% of max' % (radius_percent))
            
            plt.pause(0.05)
        