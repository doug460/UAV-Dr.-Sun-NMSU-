'''
Created on Mar 20, 2017

@author: Doug Brown

setup to record data of stuffs
'''

import numpy as np
import matplotlib.pyplot as plt

class RecordData(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.time_to_detect = []
        self.successNum = 0
        self.params = params
        
        
    def rec(self,params, detected_success):
        self.time_to_detect.append(params.current_time)
        if(detected_success):
            self.successNum += 1
        
    def averageTime(self):
        return np.mean(self.time_to_detect)

    def stdTime(self):
        return np.std(self.time_to_detect)
        
    def toString(self):
        buf = "Simulations run: %d\n" % (self.params.simulations)
        buf += "Detected %d out of %d simulatoins\n" % (self.successNum, self.params.simulations)
        buf += "Time limit = %f\n" % (self.params.time_limit)
        buf += "Average Time to detection: %f \n\tstd = %f\n" % (self.averageTime(), self.stdTime())
        buf += "Max Radius = %f \n\t Max Searchable Radius = %f\n" % (self.params.radius_max, self.params.radius_search) 
        buf += "Uav info:\n\tNumber: %d\n\tSpeed: %d\n\tD_fov: %d\n\tfps: %d\n" % (self.params.uav_num, self.params.uav_speed, self.params.uav_fov,
                                                                                self.params.fps)
        buf += "TargetRandom info:\n\tNumber %d\n\tSpeed: %d\n" % (self.params.target_num, self.params.target_speed)         
        return buf
        
    def saveInfo(self, saveDir):
        buf = saveDir + "info" + '.txt'
        file  = open(buf,'w')
        file.write(self.toString())
        file.close()
        
        self.averagedTime(saveDir)
        
        
        
    def averagedTime(self, saveDir):
        # save averaged over time
        array = np.zeros(len(self.time_to_detect))
        for count, value in enumerate(self.time_to_detect):
            if count == 0:
                array[ count ] = value
            else: 
                array[ count ] = ( array[ count - 1 ] * ( count - 1 ) + value ) / count
        
        file = saveDir + "averagedData"
        np.save(file, array)
        
            
        
        
        
        