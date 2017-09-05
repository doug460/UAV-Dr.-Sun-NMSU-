'''
Created on Mar 15, 2017

@author: Doug Brown

7-25-17: updated initial radius of UAVs (41)
    added getPos() (105)
    
8-13-17: updated initial radius based on current best initial radius for PSO
    comes from journal paper 
'''

import numpy as np
from scipy import integrate
from matplotlib.pylab import *
from numba.types import none

class UavPso(object):
    '''
    classdocs
    '''   
    
    # basic parameters for uav
    params = none
    
   
    

    def __init__(self, params, indx):
        '''
        Constructor
        
        params: save the parameters
        indx: is the number of a specific uav that is being called
        '''
        
        # the time that the pso should begin based on the equaitons
        self.time_psoStart = none
        # time shift between pso_start and actuall time
        self.time_shift = none
        
        UavPso.params = params
        
        # initialize the position
        self.angle = (2 * math.pi / (params.uav_num)) * indx 
        self.radius =  self.getInitRadius(params)
        
        self.radius_initial = self.radius
        self.updatePos()
        
        # in the pso solution in params, this is when the spiral motion whill begin
        self.time_psoStart = np.interp(self.radius_initial, params.pso_radius, params.pso_time)

        
       
        
        
    # get cartesiatn coordiante poition of uav
    def updatePos(self):
        self.position = [self.radius * math.cos(self.angle), self.radius * math.sin(self.angle)]

        
    # move one step for uav
    def moveStep(self):
        if(UavPso.params.current_time < 4 * math.pi * self.radius_initial / (UavPso.params.uav_num * UavPso.params.uav_speed)):
            self.moveCircle()
        else:
            if(self.time_shift == none):
                self.time_shift = self.time_psoStart - UavPso.params.current_time
            self.moveSpiral()
        
        # update position
        self.updatePos()
        
    # move circularly, used as initial motion for uavs
    def moveCircle(self):
        # angular ditance to travel in time step
        theta_delta  = UavPso.params.uav_speed / (UavPso.params.fps * self.radius) 
        # update angle    
        self.angle += theta_delta
        
        # update position
        self.updatePos()
        
        
    
    # move spiral motion, this is after circle motion is completed
    def moveSpiral(self):
        time = UavPso.params.current_time + self.time_shift
        
        # solve for new radius
        if(time < max(UavPso.params.pso_time)):
            radius_new = np.interp(time, UavPso.params.pso_time, UavPso.params.pso_radius)
        else:
            radius_new = max(UavPso.params.pso_radius)
        
        # solve for new angle
        drdt = (radius_new - self.radius) * UavPso.params.fps
        delta_theta = (drdt + UavPso.params.target_speed) * 2 * math.pi / (UavPso.params.uav_num *UavPso.params.uav_fov)
        delta_theta *= 1/UavPso.params.fps
        
        # update angle, radius, and position
        self.angle += delta_theta
        self.radius = radius_new
        self.updatePos()
        
    # get position of uav
    def getPos(self):
        return self.position
    
    # get initial radius
    @staticmethod
    def getInitRadius(params):
        return params.uav_speed * params.uav_fov /(2*(2*params.target_speed + params.uav_speed))
        