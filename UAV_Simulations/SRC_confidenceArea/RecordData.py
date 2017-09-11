'''
Created on Sep 3, 2017

@author: DougBrownWin

class for recording all the data/pics/video of a confidence area simulation
'''

import Variables as varis
import numpy as np
import matplotlib.pyplot as plt


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
    # records every second
    def rec_confAreaSize(self, confArea):
        
        # only save every second
        if(self.sec_counter == 0 or varis.params.current_time > self.sec_counter):
            self.sec_counter += 1
            
            # save size of confidence area
            self.area_progression.append(confArea.get_areaSize())
        
    # print data to string
    def toString(self):
        buf = 'Confidence area simulation\n\n'      
        buf += "Time limit = %f\n" % (varis.params.time_limit)
        buf += 'Ended at time = %f\n' % (varis.params.current_time)
        buf += 'Running until %f %% of maximum radius\n' % (varis.pso_radius_fraction * 100)
        buf += "Confidence area final size (m^2) = %f\n" % (np.max(self.area_progression))
        buf += "Max Radius = %f \n\t Max Searchable Radius = %f\n" % (varis.params.radius_max, varis.params.radius_search) 
        buf += "Uav info:\n\tNumber: %d\n\tSpeed: %d\n\tD_fov: %d\n\tfps: %d\n" % (varis.params.uav_num, varis.params.uav_speed, varis.params.uav_fov,
                                                                                varis.params.fps)
        buf += "TargetRandom info:\n\tSpeed: %d\n" % (varis.params.target_speed)
        return(buf)  
    
    # save graph data 
    def save_graphs(self, confArea):
        # record confidence area vs time
        plt.plot(self.area_progression)
        plt.title('Confidence area vs time')
        plt.xlabel('Time (s)')
        plt.ylabel('Area (m^2)')
        
        buf = varis.saveDir + 'confArea_vs_t.png'
        plt.savefig(buf)
        
        # recorder image of confidence area at end
        plt.imshow(confArea.matrix, cmap = 'gray_r')
        plt.title('Confidence area matrix')
        buf = varis.saveDir + 'confArea.png'
        plt.savefig(buf)
    
    # record data to file
    def save_txt(self):
        buf = varis.saveDir + "info" + '.txt'
        file  = open(buf,'w')
        file.write(self.toString())
        file.close()
        
    