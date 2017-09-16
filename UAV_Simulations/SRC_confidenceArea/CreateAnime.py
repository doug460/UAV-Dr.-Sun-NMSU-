'''
Created on Sep 16, 2017

@author: DougBrownWin
'''

import matplotlib.pyplot as plt
import Variables as varis
import matplotlib.animation as animation
import math
import numpy as np


class CreateAnime(object):
    '''
    classdocs
    '''
    


    def __init__(self):
        '''
        Constructor
        '''
        
        # holder for images
        self.images = []
        
        # keeps track of radius
        self.radiusPercent = []
        
        # keep track of pso status
        self.psoStatus = []
        
        # step size in time and visualize counter
        self.time_frameStep = 1 / varis.anime_fps
        self.time_counter = 0
    
    # image to be in movie    
    def addImage(self, image):        
        # basically plot at frame rate
        if(varis.params.current_time / self.time_frameStep > self.time_counter):
            
            self.time_counter += 1
            
            # matrix dimension
            dim = varis.matrix_dim
            
            # image to be plotted
            dim_half = math.floor(dim/varis.view_liveDownSample)
            image_new = np.zeros((dim_half, dim_half))
            
            # downsample matrix
            for row in range(0,dim,varis.anime_downSample):
                for column in range(0,dim,varis.anime_downSample):
                    image_new[math.floor(row/varis.anime_downSample),math.floor(column/varis.anime_downSample)] = image[row, column]
            
            # store downsampled image
            self.images.append(image_new)
            
            # get radius percentage
            uav = varis.params.uavs[0]
            radius = np.linalg.norm(uav.getPos())
            radiusPercent = 100 * radius / varis.params.radius_max 
            self.radiusPercent.append(radiusPercent)
            
            # record status of pso algorithm
            psoStatus = uav.getPsoStatus()
            self.psoStatus.append(psoStatus)
    
    
    # schtuff for animation
    def create(self):        
        # figure stuff
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
              
        ani = animation.FuncAnimation(self.fig, self.animate, interval = 1, frames = int(len(self.images)))
        return ani
        
    
    def animate(self, i):
        frame = i
        self.ax1.clear()
        
        # plot that shit
        self.ax1.imshow(self.images[frame], cmap = 'gray_r')

        
        # get current radius percent
        buf = 'Radius %3.0f%% of max' % (self.radiusPercent[frame])
        
        # add info about Status
        status = self.psoStatus[frame]
        if(status == varis.PSO_NORMAL):
            buf += ' (Normal)'
        elif(status == varis.PSO_PRE_NORMAL):
            buf += ' (Pre-Normal)'
        elif(status == varis.PSO_PRE_REORIENT):
            buf += ' (Pre-Reorient)'
        elif(status == varis.PSO_REDUCE_RADIUS):
            buf += ' (Reduce)'
        elif(status == varis.PSO_REORIENT):
            buf += ' (Reorient)'
            
        plt.title(buf)

        plt.xlabel('East (m)')
        plt.ylabel('North (m)')
        