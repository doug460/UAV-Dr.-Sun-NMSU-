'''
Created on Mar 15, 2017

@author: Doug Brown

The purpose of this code is to recreate the environment that I had in Matlab
However just make it better
'''

from UavPso import UavPso
import matplotlib.pyplot as plt
from Params import Params
from TargetRandom import TargetRandom
import numpy as np
import cmath as cm
import math as math
from scipy.interpolate import interp1d
from RecordPos import RecordPos
import CheckDetect_attack.CheckDetect
from RecordData import RecordData
import time
import os.path
import errno

if __name__ == '__main__':
    pass
        
    ### CONTROL PROGRAM VARIABLES ####
    
    uav_num = 1
    target_num = 4
    
    # number of siumations to be run
    simulations = 1
    
    # save images and the rate at which to save them
    saveImages = True
    saveImages_rate = 200
    
    
    #### ENVIRONMENT VARIABLES ####
    target_speed = 3
    
    uav_speed = 25
    uav_fov = 100
    
    # fps of detectorW
    fps = 30
    
    
    
    
    
    # type of simualtion run id
    type_id = "uav_pso"
    
    # directory to which to save data
    saveDir = "D:/Users/Doug Brown/Documents/NMSU Research Dr. Sun/Programming/Python/Data" + "/" + time.strftime('%Y-%m-%d--%H-%M-%S--') + type_id + "/"
    if not os.path.exists(saveDir):
        try: 
            os.makedirs(saveDir)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    
    if __name__ == '__main__':
        pass
        # initialize paramets    
        params = Params(uav_num, uav_fov, uav_speed, target_num, target_speed, fps, simulations)
    
        recordData = RecordData(params)
    
        for sim in range(0,simulations):
            # make sure reset 
            params.reset()
            
            
            buf = "Simulation %d of %d" % (sim + 1, simulations)
            print(buf)
                   
            
            # create uavs
            uavs = []
            for indx in range(0,uav_num):
                uav = UavPso(params, indx)
                uavs.insert(indx, uav)
            
            # create targets
            targets = []
            for indx in range(0,target_num):
                target = TargetRandom(params)
                targets.insert(indx, target)
                
            # create recorder
            recordPos = RecordPos(params, uavs, targets)
              
            # work on detection
            while(CheckDetect_attack.checkDetect(params, uavs, targets) == False):
                # update positions
                for indx in range(0, target_num):
                    target = targets[indx]
                    target.moveStep()
         
                 
                     
                for indx in range(0,uav_num):
                    uav = uavs[indx]
                    uav.moveStep()
                 
                # update time
                params.timeStep()
                 
                # record positons 
                recordPos.record(uavs,targets)
             
            recordData.rec(params)
            
            if(saveImages and (sim + 1) % saveImages_rate == 0):
                recordPos.savePlot(saveDir, str(sim + 1))
            
        print(recordData.toString())
        recordData.saveInfo(saveDir)
        
    