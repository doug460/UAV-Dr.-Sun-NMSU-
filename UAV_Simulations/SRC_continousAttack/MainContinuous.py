'''
Created on Jul 11, 2017

@author: Doug Brown
The idea here is to have a continuos stream of targets attacking the center of the search area
Count failed defense
'''


from Params import Params
from numba.types import none
from LoopController import *

if __name__ == '__main__':
    pass

    # num of uavs
    uav_num = 1
    
    # num of target angles placed throughout searchable
    # radial seperation between targets (m)
    target_angles = 180
    target_seperation = 20
    
    # the percent that PSO should reach its max radius 
    # this is used for time limit of simulation
    # reaches this percent of max radius and adds time for one more complete revolution
    pso_radius_percent = 0.99
    
    #### ENVIRONMENT VARIABLES ####
    target_speed = 3
    
    uav_speed = 25
    uav_fov = 100
    
    # fps of detection
    fps = 30  
    
    # select the uav to be used
    # UAV_PSO: for pso flight pattern with uav
    # UAV_RASTER: for raster flight pattern
    uav_id = UAV_PSO
    
    # select type of target to be used
    # TARGET_GENERIC: more generic target which is the only one to be use with this program
    target_id = TARGET_GENERIC
    
    # initialize parameters    
    params = Params(uav_num, uav_fov, uav_speed, none, target_speed, fps, none, none)
    
    # variables to pass to loopController
    #    target_angles, params
    loopCont = LoopController(params, target_angles, uav_id, target_id, target_seperation, pso_radius_percent)
    loopCont.begin()
    


