'''
Created on Mar 20, 2017

@author: Doug Brown
'''
import numpy as np

class CheckDetect(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    
    @staticmethod
    def checkDetect(params, uavs, targets):
        # loop through all targets and uavs
        for indx_uav in range(0,params.uav_num):
            uav = uavs[indx_uav]
            for indx_target in range(0,params.target_num):
                target = targets[indx_target]
                
                # update detection
                if(np.linalg.norm(uav.position - target.position ) < params.uav_fov/2):
                    target.detected = True
        
        # check if all are detected
        allDetected = True
        for indx in range(0,params.target_num):
            if(targets[indx].detected == False):
                allDetected = False 
            
        return allDetected
    
    @staticmethod
    def totalDetected(params, targets):        
        # check if all are detected
        amountDetected = 0
        for indx in range(0,params.target_num):
            if(targets[indx].detected == True):
                amountDetected += 1
            
        return amountDetected