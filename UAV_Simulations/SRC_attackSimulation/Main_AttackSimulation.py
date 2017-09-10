'''
created: 4-11-17
creator: Doug Brown

Purpose: control the simulation of defense from targets attack searchable area

The targets are place radialy around the searchable area. They attack in and the 
resulting deffense information is then saved 
'''

from AttackSimulation import *
from Params import Params
from numba.types import none

if __name__ == '__main__':
    pass

    ### CONTROL PROGRAM VARIABLES ####
    
    # number of uavs
    uav_num = 1
    
    # targets will get distributed evenly over a circle
    target_num = 50
    
    #### ENVIRONMENT VARIABLES ####
    target_speed = 3
    
    uav_speed = 25
    uav_fov = 100
    
    # fps of detection
    fps = 30
    
    # initial radius multipler for stopping radius
    radius_multiplier = 2
    radius_steps = 5
    
    
    # select the uav to be used
    # UAV_PSO: for pso flight pattern with uav
    # UAV_RASTER: for raster flight pattern
    uav_id = UAV_RASTER
    
    # select type of target to be used
    # TARGET_RANDOM: is for random moving target
    # TARGET_DIPOLE: target behaves as uavs are dipoles
    # TARGET_ATTACK: for sending uav in a direction toward the center of the search area
    target_id = TARGET_ATTACK
    
    # initialize parameters    
    params = Params(uav_num, uav_fov, uav_speed, target_num, target_speed, fps, none, none)
    
    # radius parameters for attacking targets
    initial_radius = params.radius_search
    final_radius = initial_radius * radius_multiplier
    radial_stepSize = (final_radius - initial_radius)/radius_steps
    
    # initialize and run simulation
    attackSim = AttackSimulation(params, uav_id, target_id, initial_radius, final_radius, radial_stepSize)
    attackSim.begin()