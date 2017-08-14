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

if __name__ == '__main__':
    pass

    ### CONTROL PROGRAM VARIABLES ####
    # for looping tests
    uav_num_i = 1
    uav_num_f = 1
    target_num_i = 1
    target_num_f = 1
    
    
    # number of siumations to be run
    simulations = 1000
    
    # time limit (s) for how long the program can run
    time_limit = 1000
    
    # save images and the rate at which to save them
    saveImages = True
    saveImages_rate = 100
    
    # save move stuff
    saveMovie = False
    saveMovie_rate = 1
    
    #### ENVIRONMENT VARIABLES ####
    target_speed = 3
    
    uav_speed = 25
    uav_fov = 100
    
    # fps of detection
    fps = 30
    
    #step back one step in dir path for os system
    os.chdir('..')
    
    
    # select the uav to be used
    # UAV_PSO: for pso flight pattern with uav
    # UAV_RASTER: for raster flight pattern
    uav_id = UAV_RASTER
    
    # select type of target to be used
    # TARGET_RANDOM: is for random moving target
    # TARGET_DIPOLE: target behaves as uavs are dipoles
    target_id = TARGET_RANDOM
    
    # loop through tests and save info
    for uav_num in range(uav_num_i, uav_num_f + 1):
        for target_num in range(target_num_i, target_num_f + 1):
            # make sure params is clear
            params = none
    
            # initialize parameters    
            params = Params(uav_num, uav_fov, uav_speed, target_num, target_speed, fps, simulations, time_limit)
            
            # run simulation run
            searchSim = SearchSimulation(params, uav_id, target_id, saveImages, saveImages_rate, saveMovie, saveMovie_rate, time_limit)    
            searchSim.begin()
    