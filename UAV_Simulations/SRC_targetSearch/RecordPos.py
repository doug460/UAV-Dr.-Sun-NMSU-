'''
Created on Mar 20, 2017

record positions of uavs and targets
@author: Doug Brown
'''
from numba.types import none
import matplotlib.pyplot as plt
import numpy as np
import math as math
from pylab import *
import os
from CreateAnime import CreateAnime
import matplotlib.animation as animation


class RecordPos(object):
    '''
    classdocs
    '''
    
    targets_pos = []
    uavs_pos = []

    # save a copy of the params
    params = none

    def __init__(self, params, uavs, targets):
        '''
        Constructor
        '''
        self.params = params
        self.record_indx = 0
        
        # initialziing targets position as array
        for indx in range(0,params.target_num):
            list_positions = []
            target = targets[indx]
            array = [target.position[0], target.position[1]]
            list_positions.insert(0,array)
            self.targets_pos.insert(indx,list_positions)
            
            
        # initializing uavs positions
        for indx in range(0,params.uav_num):
            list_positions = []
            uav = uavs[indx]
            array = [uav.position[0], uav.position[1]]
            list_positions.insert(0,array)
            self.uavs_pos.insert(indx,list_positions)
        
        
    # record the positions of the targets     
    def record(self, uavs, targets):
        
        # update target
        for indx in range(0,self.params.target_num):
            target = targets[indx]
            list_positions = self.targets_pos[indx]
            array = [target.position[0], target.position[1]]
            list_positions.append(array)
            
        
        # update uavs
        for indx in range(0,self.params.uav_num):
            uav = uavs[indx]
            list_positions = self.uavs_pos[indx]
            array = [uav.position[0], uav.position[1]]
            list_positions.append(array) 
            
            
    def savePlot(self, saveDir, name):
        
        # need to plot all the uavs and targets paths  
        for indx in range(0,self.params.target_num):
            array = self.targets_pos[indx]
            x = [item[0] for item in array]
            y = [item[1] for item in array]
            line_targets, = plt.plot(x,y, 'b--', label = 'Target')
            line_initial, = plt.plot(x[0],y[0], 'k*', label = 'Start Position', markersize = 8)
        
        # plot uavs
        for indx in range(0,self.params.uav_num):
            array = self.uavs_pos[indx]
            x = [item[0] for item in array]
            y = [item[1] for item in array]
            line_uavs, = plt.plot(x,y, 'r-', label = 'UAV')
            plt.plot(x[0],y[0], 'k*', markersize = 8)
        
        # plot circle around searchable area
        radius = self.params.radius_search
        t = np.arange(0, 2 * math.pi, 0.01)
        x = np.cos(t) * radius
        y = np.sin(t) * radius
        line_area, = plt.plot(x,y,'k--', label = 'Search Area')
        
        # plot circle around each uav
        for indx in range(0,self.params.uav_num):
            radius = self.params.uav_fov/2
            t = np.arange(0, 2 * math.pi, 0.01)
            array = self.uavs_pos[indx][len(self.uavs_pos[indx]) - 1]
            x = np.cos(t) * radius + array[0]
            y = np.sin(t) * radius + array[1]
            line_fov, = plt.plot(x,y,'g:', label = 'Field of View')
        
        plt.title('UAV-TargetRandom Simulation')
        plt.xlabel('East (m)')
        plt.ylabel('North (m)')
        
        plt.legend(handles = [line_uavs, line_targets, line_area, line_fov, line_initial])
        
        buf = saveDir + name + '.png'
        plt.savefig(buf)
        
        plt.close()
    
    def saveAnime(self, saveDir, name):
        createAnime = CreateAnime(self.params)
        ani = createAnime.create(self)
        buf = saveDir + name + '.mp4'
        
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps = 29, metadata=dict(artist='Me'), bitrate=1800)
        
        print('Saving Animation...')
        ani.save(buf, writer = writer)
        print('Save Complete!')
    
        