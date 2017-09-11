'''
Created on Sep 3, 2017

@author: DougBrownWin

general variables for confidence area simulation
'''
from numba.types import none
from Params import Params
import numpy as np
import math
import time
from SaveDirs import DIR_DATA
from UavPso_add_sub import UavPso_addSub
import os
import errno

# state of PSO formation
PSO_NORMAL = 1
PSO_REORIENT = 2
PSO_REDUCE_RADIUS = 3


# State of UAV
UAV_NORMAL = 1
UAV_REFERENCE = 2

# operations
OP_ADD = 1
OP_SUB = 2

#-------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------#


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

# sive of matrix to be used
matrix_dim = 100

# visualization stuff
view_liveBool = False
view_liveFPS = 1
view_liveDownSample = 2

# array for adding and subtracting uavs
# [] = run standard
uavChangeArray = [OP_ADD]




#-------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------#

# id for simulation runs
name_id = 'confArea'

# initialize parameters    
params = Params(uav_num, uav_fov, uav_speed, none, target_speed, fps, none, none)

# directory to which to save data
saveDir = DIR_DATA + time.strftime('%Y-%m-%d--%H-%M-%S--') + name_id + "/"
if not os.path.exists(saveDir):
    try: 
        os.makedirs(saveDir)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise









