'''
Created on Jul 25, 2017

@author: Doug Brown
'''

from UavPso import UavPso
from UavRaster import UavRaster
from TargetRandom import TargetRandom
from TargetDipole import TargetDipole 
import os
import time
import errno
import numpy as np
import math
from TargetGeneric import TargetGeneric
from CheckStatus import checkStatus
from RecordData_cont import RecordData
from Constants import *

class LoopController(object):
    '''
    classdocs
    '''

    # initialize variables
    def __init__(self, params, target_angles, uav_id, target_id, target_seperation, pso_radius_percent):
        '''
        Constructor
        '''
        
        self.uav_id = uav_id
        self.target_id = target_id
        
        self.params = params
        self.target_angles = target_angles
        
        self.target_seperation = target_seperation
        self.pso_radius_percent = pso_radius_percent
        
        #id stuff
        if(uav_id == UAV_PSO):
            self.name_id = 'uavPso_'
        elif(uav_id == UAV_RASTER):
            self.name_id = 'uavRaster_'
        
        if(target_id == TARGET_RANDOM):
            self.name_id += 'targetRandom'
        elif(target_id == TARGET_DIPOLE):
            self.name_id += 'targetDipole'
        elif(target_id == TARGET_GENERIC):
            self.name_id += 'targetGeneric'
            
        # initialize data recorder
        # record number of uavs, targets generated
        # record successful and detected
        # record time peramiters
        self.recData = RecordData(params, target_angles, target_seperation, pso_radius_percent)
        
            
    # this controls which uav object to return
    def getUav(self, params, indx):
        self.recData.addUAV()
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
    def getTarget(self, params, position, direction):
        self.recData.addTarget()
        if(self.target_id == TARGET_GENERIC):
            # generate generic target
            target = TargetGeneric(params, position, direction)
        else:
            raise ValueError('target_id class id not valid')
    
        # add target to params
        # NOTE: got rid of this as it seems unnecessary and wasteful...
#         params.addTarget(target)

        return(target)
        
    
    # begin continuous attack 
    def begin(self):
        # directory to which to save data
        data_path = 'Data/'
        
        saveDir = data_path + time.strftime('%Y-%m-%d--%H-%M-%S--') + self.name_id + "/"
        
        if not os.path.exists(saveDir):
            try: 
                os.makedirs(saveDir)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        # local copy of params    
        params = self.params
        
        # get steps for simulation
        # get indx for reaching 99% radius
        indx =  params.pso_radius > params.radius_max*self.pso_radius_percent
        radius_limit = np.min(params.pso_radius[indx])
        time_limit = np.min(params.pso_time[indx])
        
        # add the time it takes to do two loop at that radius
        time_limit += 2*np.pi * radius_limit / params.uav_speed    
        params.time_limit = time_limit
        
        
        
        # create UAVs
        uavs = []
        for indx in range(0,params.uav_num):
            uav = self.getUav(params, indx)
            uavs.insert(indx, uav)
        
        # there are going to be 360 targets distributed circularly at every 10m from origin    
        targets = []
        for indx in range(0,math.ceil(params.radius_max/self.target_seperation)*self.target_angles):
            # set position and direction
            # basically build outwards
            # every 10m place target, 360 of them at every degree based on target_num
            radius = math.floor(indx/self.target_angles + 1)*self.target_seperation
            angle = np.radians(indx)
            x = np.cos(angle)*radius
            y = np.cos(angle)*radius
            position = np.array([x,y])
            
            # get direction
            direction = np.array([-math.cos(angle), -math.sin(angle)])
            
            # get target object
            target = self.getTarget(params, position, direction)
            targets.insert(indx, target)
        
        

        print("Running simulation...")
        # while less than radius
        step_stop = math.ceil(time_limit * params.fps)
        for step in range(0, step_stop):
            # loop till PSO would have reached 99.9% of its search path + one loop
            
            # basically just prints out progress of algorithm
            if(step%10 == 0):
                percent = 100 * step/step_stop
                buf = "Complete: %f%%" % (percent)
                print(buf)
            
            # check detection parameters
            # if detected or reach center, move to perimeter
            for uav in uavs:
                for target in targets:
                    status = checkStatus(params, uav, target)
                    #  also count detected and successful targets
                    if(status == TARGET_DETECTED):
                        self.recData.targetDetect()
                        del targets[targets.index(target)]
                        
                    if(status == TARGET_SUCCESSFUL):
                        self.recData.targetSuccess()
                        del targets[targets.index(target)]
                        
            
            # move UAVs and targets
            for uav in uavs:
                uav.moveStep()
            for target in targets:
                target.moveStep()
                
            # generate new targets at specific time, at the outer radius
            if(step > 0 and step%(self.target_seperation /( params.target_speed / params.fps)) == 0):
                for indx in range(0,self.target_angles):
                    radius = params.radius_max
                    angle = np.radians(indx)
                    x = np.cos(angle)*radius
                    y = np.cos(angle)*radius
                    position = np.array([x,y])
                    
                    # get direction
                    direction = np.array([-math.cos(angle), -math.sin(angle)])
                    
                    # get target object
                    target = self.getTarget(params, position, direction)
                    targets.append(target)
                    
        
        # TODO: Print and record data
        print(self.recData.toString())
            
            
        
    
    
        