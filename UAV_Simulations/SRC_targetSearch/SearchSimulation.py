'''
Created on Mar 22, 2017

@author: Doug Brown

7-25-17: updated data directory to be relative (99)
8-13-17: got rid of this cause its actually a pain in the ass...
'''
import time
import os
import errno
from RecordData import RecordData
from RecordPos import RecordPos
from CheckDetect import CheckDetect
from UavPso import UavPso
from UavRaster import UavRaster
from TargetRandom import TargetRandom
from TargetDipole import TargetDipole

from SaveDirs import DIR_DATA


# type of uav to be used
UAV_PSO = 1
UAV_RASTER = 2

# type of target to be used
TARGET_RANDOM = 1
TARGET_DIPOLE = 2

class SearchSimulation(object):
    '''
    classdocs
    '''
    
   


    def __init__(self, params, uav_id, target_id, saveImages, saveImages_rate, saveMovie, saveMovie_rate, time_limit):
        '''
        Constructor
        '''
        
        self.saveImages = saveImages
        self.saveImages_rate = saveImages_rate
        self.saveMovie = saveMovie
        self.saveMovie_rate = saveMovie_rate
        self.time_limit = time_limit
       
        self.params = params
        self.uav_id = uav_id
        self.target_id = target_id
        
        if(uav_id == UAV_PSO):
            self.name_id = 'uavPso_'
        elif(uav_id == UAV_RASTER):
            self.name_id = 'uavRaster_'
        
        if(target_id == TARGET_RANDOM):
            self.name_id += 'targetRandom'
        elif(target_id == TARGET_DIPOLE):
            self.name_id += 'targetDipole'
    
        
    # this controls which uav object to return
    def getUav(self, params, indx):
        if(self.uav_id == UAV_PSO):
            uav = UavPso(params,indx)
        elif(self.uav_id == UAV_RASTER):
            uav = UavRaster(params,indx)
        else:
            raise ValueError('Uav_id class id not recognized')
        
        # add uav to params
        params.addUav(uav)
        
        return(uav)

    # this controls which target object to return
    def getTarget(self, params):
        if(self.target_id == TARGET_RANDOM):
            target = TargetRandom(params)
        elif(self.target_id == TARGET_DIPOLE):
            target = TargetDipole(params)
        else:
            raise ValueError('target_id class id not recognized')
    
        # add target to params
        params.addTarget(target)
        
        return(target)
    
    
    
    def begin(self):
        
        # directory to which to save data
        
        saveDir = DIR_DATA + time.strftime('%Y-%m-%d--%H-%M-%S--') + self.name_id + "/"
        if not os.path.exists(saveDir):
            try: 
                os.makedirs(saveDir)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        # initialize paramets    
        params = self.params
    
        # recrod data info class
        recordData = RecordData(params)
    
        for sim in range(0,params.simulations):
            # make sure reset 
            params.reset()
            
            
            buf = "Simulation %d of %d" % (sim + 1, params.simulations)
            print(buf)
                   
            
            # clear and create create uavs
            uavs = []
            for indx in range(0,params.uav_num):
                uav = self.getUav(params, indx)
                uavs.insert(indx, uav)
            
            # create targets
            targets = []
            for indx in range(0,params.target_num):
                target = self.getTarget(params)
                targets.insert(indx, target)
                
            # create recorder
            recordPos = RecordPos(params, uavs, targets)
              
            # work on detection
            while(CheckDetect.checkDetect(params, uavs, targets) == False and params.current_time < self.time_limit):
                # update positions for uavs and targets
                for indx in range(0, params.target_num):
                    target = targets[indx]
                    
                    # if detected don't move
                    if(target.detected == False):
                        target.moveStep()
            
                for indx in range(0,params.uav_num):
                    uav = uavs[indx]
                    uav.moveStep()
                 
                # update time
                params.timeStep()
                 
                # record positons 
                recordPos.record(uavs,targets)
            
            # record simulation data 
            recordData.rec(params, CheckDetect.checkDetect(params, uavs, targets), CheckDetect.totalDetected(params, targets))
            
            # create images and movies based on user input
            if(self.saveImages and (sim + 1) % self.saveImages_rate == 0):
                recordPos.savePlot(saveDir, str(sim + 1))
            
            if(self.saveMovie and (sim + 1) % self.saveMovie_rate == 0):
                # create animation of paths taken
                recordPos.saveAnime(saveDir, str(sim+1))
                
            
                
        
        # print and record data        
        print(recordData.toString())
        recordData.saveInfo(saveDir)
            
        