'''
Created on Apr 14, 2017

@author: Doug Brown
'''

import numpy as np
from TargetAttack import *

class CheckDetect_attack(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    @staticmethod
    def updateStatus(params):
        for target in params.targets:
            for uav in params.uavs:
                
                # check radius between targets and uavs
                if(np.linalg.norm(uav.position - target.position) < params.uav_fov/2 and target.getStatus() == ATTACKING):
                    target.setStatus(DETECTED)
                    
                elif(np.linalg.norm(target.position) < params.target_speed/params.fps):
                    target.setStatus(SUCCESSFULL)
    
    # basically check if all targets are detected or not   
    @staticmethod
    def shouldContinue(params):
        for target in params.targets:
            if (target.status == ATTACKING):
                return True
        
        return False
                    