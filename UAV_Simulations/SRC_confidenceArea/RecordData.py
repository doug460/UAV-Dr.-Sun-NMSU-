'''
Created on Sep 3, 2017

@author: DougBrownWin

class for recording all the data/pics/video of a confidence area simulation
'''

import Variables as varis
import numpy as np


class RecordData(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        # keeps track of seconds for recording info
        self.sec_counter = 0
        
        # keeps track of size of confidence area over time
        self.area_progression = []
    
    
    # for size of confidence area
    def rec_confArea(self, confArea):
        
        # only save every second
        if(self.sec_counter == 0 or varis.params.current_time > self.sec_counter):
            self.sec_counter += 1
            
            # save size of confidence area
            self.area_progression.append(confArea.get_areaSize())
        
    # print data to string
    def toString(self):
        buf = 'Confidence area simulation\n\n'      
        buf += "Time limit = %f\n" % (varis.params.time_limit)
        buf += "Confidence area final size (m^2) = %f\n" % (np.max(self.area_progression))
        buf += "Max Radius = %f \n\t Max Searchable Radius = %f\n" % (varis.params.radius_max, varis.params.radius_search) 
        buf += "Uav info:\n\tNumber: %d\n\tSpeed: %d\n\tD_fov: %d\n\tfps: %d\n" % (varis.params.uav_num, varis.params.uav_speed, varis.params.uav_fov,
                                                                                varis.params.fps)
        buf += "TargetRandom info:\n\tSpeed: %d\n" % (varis.params.target_speed)
        return(buf)  
    
    # record data to file
    def save_txt(self):
        buf = varis.saveDir + "info" + '.txt'
        file  = open(buf,'w')
        file.write(self.toString())
        file.close()
        
    