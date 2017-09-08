'''
Created on Sep 3, 2017

@author: DougBrownWin

general variables for confidence area simulation
'''
from numba.types import none
from Params import Params
import numpy as np
from UavPso import UavPso
import math
import time
from SaveDirs import DIR_DATA
import os
import errno

# number of uavs
uav_num = 1

# uav stuff
uav_speed = 25
uav_fov = 100

# target stuff
target_speed = 3

# fps of detection
fps = 30

# percent radius for which the pso algorithm much reach when using dipole target
# number of final loops to do when reached 0.99 radius
pso_radius_fraction = 0.99
pso_final_loops = 2

# sive of matrix to be used
matrix_dim = 100

# visualization stuff
view_liveBool = False
view_liveFPS = 1
view_liveDownSample = 2




#-------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------#

# id for simulation runs
name_id = 'confArea'

# initialize parameters    
params = Params(uav_num, uav_fov, uav_speed, none, target_speed, fps, none, none)

# calc time limit
# get indx for reaching 99% radius
indx =  params.pso_radius > params.radius_max*pso_radius_fraction
radius_limit = np.min(params.pso_radius[indx])
time_limit = np.min(params.pso_time[indx])

# get rid of time not acutally in pso path at beginning
indx = params.pso_radius > UavPso.getInitRadius(params)
time_limit -= np.min(params.pso_time[indx])

# need to adjust for initial motion of two loops at initial radius
time_initial = 2 * 2 * math.pi * UavPso.getInitRadius(params) / uav_speed
time_limit += time_initial


# do two loops at end
time_limit += pso_final_loops * 2*np.pi * radius_limit / params.uav_speed    
params.time_limit = time_limit



# directory to which to save data
saveDir = DIR_DATA + time.strftime('%Y-%m-%d--%H-%M-%S--') + name_id + "/"
if not os.path.exists(saveDir):
    try: 
        os.makedirs(saveDir)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise







