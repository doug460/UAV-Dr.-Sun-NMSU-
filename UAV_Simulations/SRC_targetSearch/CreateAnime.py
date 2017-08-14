'''
Created on Mar 22, 2017

@author: Doug Brown
'''

import matplotlib.pyplot as plt
import RecordPos
import numpy as np
import math
import matplotlib.animation as animation

class CreateAnime(object):
    '''
    classdocs
    '''
    
    frameStep = 10


    def __init__(self, params):
        '''
        Constructor
        '''
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        self.params = params
        
        self.maxAxis = params.radius_max +params.uav_fov
        
    def create(self, recordpos):
        self.targets_pos = recordpos.targets_pos
        self.uavs_pos = recordpos.uavs_pos
        
        ani = animation.FuncAnimation(self.fig, self.animate, interval = 1, frames = int(len(self.targets_pos[0])/CreateAnime.frameStep))
        return ani
        
    
    def animate(self, i):
        frame = i * CreateAnime.frameStep
        self.ax1.clear()
        
        # plot circle around searchable area
        radius = self.params.radius_search
        t = np.arange(0, 2 * math.pi, 0.01)
        x = np.cos(t) * radius
        y = np.sin(t) * radius
        self.ax1.plot(x,y,'k--')
        
        # plot uavs
        for indx in range(0,self.params.uav_num):
            array = self.uavs_pos[indx]
            x = array[frame][0]
            y = array[frame][1]
            self.ax1.plot(x,y, 'o-')
        
        # plot targets   
        for indx in range(0,self.params.target_num):
            array = self.targets_pos[indx]
            x = array[frame][0]
            y = array[frame][1]
            self.ax1.plot(x,y, '*--')
            
        # plot circle around each uav
        for indx in range(0,self.params.uav_num):
            radius = self.params.uav_fov/2
            t = np.arange(0, 2 * math.pi, 0.01)
            array = self.uavs_pos[indx][frame]
            x = np.cos(t) * radius + array[0]
            y = np.sin(t) * radius + array[1]
            self.ax1.plot(x,y,'g:')
            
        plt.ylim([-self.maxAxis,self.maxAxis])
        plt.xlim([-self.maxAxis,self.maxAxis])
        plt.title('Animation')
        plt.xlabel('East (m)')
        plt.ylabel('North (m)')
        
    
        
        
        