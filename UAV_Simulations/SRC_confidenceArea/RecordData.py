'''
Created on Sep 3, 2017

@author: DougBrownWin

class for recording all the data/pics/video of a confidence area simulation
'''

import Variables as varis
import numpy as np
import matplotlib.pyplot as plt
from numba.types import none
import math
from CreateAnime import CreateAnime
import matplotlib.animation as animation


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
        
        # time when uavs were added
        # time when uavs were subtracted
        self.uavAdded_time = []
        self.uavSub_time = []
        
        self.anime = CreateAnime()
    
    
    # for size of confidence area
    # records every second
    def rec_confAreaSize(self, confArea):
        
        # only save every second
        if(self.sec_counter == 0 or varis.params.current_time > self.sec_counter):
            self.sec_counter += 1
            
            # save size of confidence area
            self.area_progression.append(confArea.get_areaSize())
            
    # record image for animation
    def rec_anime(self, confArea):
        if varis.anime_bool:
            self.anime.addImage(confArea.matrix)
        
    # print data to string
    def toString(self):
        buf = 'Confidence area simulation\n\n'      
        if(varis.params.time_limit != none):
            buf += "Time limit = %f\n" % (varis.params.time_limit)
        buf += 'Ended at time = %f\n' % (varis.params.current_time)
        buf += 'Running until %f %% of maximum radius\n' % (varis.pso_radius_fraction * 100)
        buf += "Confidence area final size (m^2) = %f\n" % (self.area_progression[len(self.area_progression) - 1])
        buf += "Max Radius = %f \n\t Max Searchable Radius = %f\n" % (varis.params.radius_max, varis.params.radius_search) 
        buf += "Uav info:\n\tNumber: %d\n\tSpeed: %d\n\tD_fov: %d\n\tfps: %d\n" % (varis.params.uav_num, varis.params.uav_speed, varis.params.uav_fov,
                                                                                varis.params.fps)
        buf += "TargetRandom info:\n\tSpeed: %d\n" % (varis.params.target_speed)
        return(buf)  
    
    # save graph data 
    def save_graphs(self, confArea):  
        # handles for the plots
        hnd_add = none
        hnd_sub = none
              
        # record confidence area vs time
        hnd_area, = plt.plot(self.area_progression)
        plt.title('Confidence area vs time')
        plt.xlabel('Time (s)')
        plt.ylabel('Area (m^2)')
        
        #plot times when uav was added and subtracted
        for x in self.uavAdded_time:
            hnd_add, = plt.plot([x,x],[0,self.area_progression[x]], '--k') 
            print("added time %d\n" % (x))
        
        for x in self.uavSub_time:
            hnd_sub, = plt.plot([x,x],[0,self.area_progression[x]], '--k')
        
        # create legend
        
        
        if hnd_add is none:
            if hnd_sub is none:
                plt.legend([hnd_area], ['Area'])
            else:
                plt.legend([hnd_area, hnd_sub], ['Area', 'Uav Subtracted'])
        elif hnd_sub is none:
            plt.legend([hnd_area, hnd_add], ['Area', 'Uav Added'])
        else:
            plt.legend([hnd_area, hnd_add, hnd_sub], ['Confidence Area', 'Uav Added', 'Uav Subtracted'])
            
            
        
        buf = varis.saveDir + 'confArea_vs_t.png'
        plt.savefig(buf)
        
        plt.clf()
        
        # recorder image of confidence area at end
        plt.imshow(confArea.matrix, cmap = 'gray_r')
        plt.title('Confidence Area')
        plt.xlabel('East')
        plt.ylabel('North')
        buf = varis.saveDir + 'confArea.png'
        plt.savefig(buf)
    
    # record data to file
    def save_txt(self):
        buf = varis.saveDir + "info" + '.txt'
        file  = open(buf,'w')
        file.write(self.toString())
        file.close()
    
    # record time a uav as added
    def uavAdded(self):
        self.uavAdded_time.append(math.floor( varis.params.current_time))
    
    # record time when a uav was subbtracted
    def uavSub(self):
        self.uavSub_time.append(math.floor(varis.params.current_time))
        
    # save animation
    def saveAnime(self):
        if varis.anime_bool:
            ani = self.anime.create()
            buf = varis.saveDir + 'animation.mp4'
            
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps = 15, metadata=dict(artist='Me'), bitrate=1800)
            
            print('Saving Animation...')
            ani.save(buf, writer = writer)
            print('Save Complete!')