'''
Created on Jul 26, 2017

@author: Doug Brown
basically just want to check status of stuff
'''
import numpy as np
from Constants import *

def checkStatus(params, uav, target):
    # update detection
    if(np.linalg.norm(uav.position - target.position ) < params.uav_fov/2):
        status = TARGET_DETECTED
    elif(np.linalg.norm(target.position) < params.target_speed):
        status = TARGET_SUCCESSFUL
    else:
        status = TARGET_NORMAL
    
    return(status)
