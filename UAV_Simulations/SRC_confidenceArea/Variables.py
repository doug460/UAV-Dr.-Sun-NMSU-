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
import os
import errno

# RUN Z PROGRAM HANZ!!


# state of PSO formation
PSO_PRE_NORMAL = 4
PSO_NORMAL = 1

PSO_PRE_REORIENT = 5
PSO_REORIENT = 2

PSO_REDUCE_RADIUS = 3



# State of UAV
UAV_NORMAL = 1
UAV_REFERENCE = 2
UAV_REORIENT = 3

# operations
OP_ADD = 1
OP_SUB = 2

#-------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------#


# number of uavs
uav_num = 2

# uav stuff
uav_speed = 20
uav_fov = 100

# speed at which the reorienting uavs should travel
uav_reorientSpeed = uav_speed - 5

# target stuff
target_speed = 3

# fps of detection
fps = 30

# percent radius for which the pso algorithm much reach when using dipole target
# number of final loops to do when reached 0.99 radius
pso_radius_fraction = 0.99

# sive of matrix to be used
matrix_dim = 300

# visualization stuff
view_liveBool = False
view_liveFPS = 1
view_liveDownSample = 2

# for animation
# down sample is for matrix
anime_bool = True
anime_fps = 2
anime_downSample = 2

# array for adding and subtracting uavs
# [] = run standard
# read it backwards
uavChangeArray = [OP_ADD, OP_SUB, OP_ADD]



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

# get the total number of uavs
uavs_max = uav_num
for opp in uavChangeArray:
    if(opp == OP_ADD):
        uavs_max += 1









