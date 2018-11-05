'''
Created on Mar 22, 2017

@author: Doug Brown

basicaly populate searchable area with specific number of UAVs.
Search for those targets and save data 

8-13-17: updated to loop through number of targets and UAVs
'''
from SearchSimulation import *
from Params import Params
from numba.types import none
import os
import numpy as np
import math

if __name__ == '__main__':
    pass

    ### CONTROL PROGRAM VARIABLES ####
    # for looping tests
    uav_num_i = 5
    uav_num_f = 5
    target_num_i = 4
    target_num_f = 4
    
    
    # number of siumations to be run
    simulations = 1000
        
    # time limit (s) for how long the program can run
    time_limit = 1000
    
    # percent radius for which the pso algorithm much reach when using dipole target
    # number of final loops to do when reached 0.99 radius
    pso_radius_fraction = 0.99
    pso_final_loops = 2
    
    # save images and the rate at which to save them
    saveImages = False
    saveImages_rate = 100
    
    # save move stuff
    saveMovie = False
    saveMovie_rate = 1
    
    #### ENVIRONMENT VARIABLES ####
    target_speed = 3
    
    uav_speed = 20
    uav_fov = 100
    
    # fps of detection
    fps = 30
    
    
    # select the uav to be used
    # UAV_PSO: for pso flight pattern with uav
    # UAV_RASTER: for raster flight pattern
    uav_id = UAV_RASTER
    
    # select type of target to be used
    # TARGET_RANDOM: is for random moving target
    # TARGET_DIPOLE: target behaves as uavs are dipoles
    target_id = TARGET_DIPOLE
    
    
    # loop through tests and save info
    for uav_num in range(uav_num_i, uav_num_f + 1):
        for target_num in range(target_num_i, target_num_f + 1):
            # make sure params is clear
            params = none
    
            # initialize parameters    
            params = Params(uav_num, uav_fov, uav_speed, target_num, target_speed, fps, simulations, time_limit)
            
            # check for dipole "smart" target, and adjust time limit accordingly
            if(target_id == TARGET_DIPOLE):
               
                # calc time limit
                # get indx for reaching 99% radius
                indx =  params.pso_radius > params.radius_max*pso_radius_fraction
                radius_limit = np.min(params.pso_radius[indx])
                time_limit = np.min(params.pso_time[indx])
                
                # get rid of time not acutally in pso path at beginning
                indx = params.pso_radius > UavPso.getInitRadius(params)
                time_limit -= np.min(params.pso_time[indx])
                
                # need to adjust for initial motion of one loop at initial radius
                time_initial = 2 * math.pi * UavPso.getInitRadius(params) / uav_speed
                time_limit += time_initial
                
                
                # do two loops at end
                time_limit += pso_final_loops * 2*np.pi * radius_limit / params.uav_speed    
                params.time_limit = time_limit
            
            # run simulation run
            searchSim = SearchSimulation(params, uav_id, target_id, saveImages, saveImages_rate, saveMovie, saveMovie_rate, time_limit)    
            searchSim.begin()
    