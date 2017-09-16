'''
Created on Sep 3, 2017

@author: DougBrownWin
create a framework to visualize a continous confidence area generated by the UAVs
'''

import Variables as varis
from SRC_confidenceArea.ConfArea_Matrix import ConfArea_Matrix
from SRC_confidenceArea.ViewLive import ViewLive
from UavPso import UavPso
from RecordData import RecordData
import numpy as np
from UavPso_add_sub import UavPso_addSub
import math

class ConfArea(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        self.confArea = ConfArea_Matrix()
        self.viewLive = ViewLive()
        
    # this controls which uav object to return
    def getUav(self, indx):
        uav = UavPso_addSub(varis.params,indx)
        
        # add uav to params
        varis.params.addUav(uav)
        
        return(uav)   
            
    
    
    # begin simualtion test
    def begin(self):
        
        # create uavs
        uavs = []
        for indx in range(0,varis.params.uav_num):
            uav = self.getUav(indx)
            uavs.insert(indx, uav)
        
        # data/pic/video recorder
        # record position, confArea size, time, 
        # also save pic/video files
        recorder = RecordData() 
        
        
        print("Running confidence area simulation")
        
        # basically just keeptrack of percent to manage printing
        percent_counter = math.floor(100 * np.linalg.norm(uavs[0].getPos())/np.linalg.norm(varis.params.radius_max))

        # loop until radius is at 99 percent
        # have done all add/sub proceedures
        # and proceedures are complete
        while(np.linalg.norm(uavs[0].getPos())/np.linalg.norm(varis.params.radius_max) < varis.pso_radius_fraction or 
              len(varis.uavChangeArray) > 0 or 
              uavs[0].getPsoStatus() != varis.PSO_NORMAL):
            
            percent = 100 * np.linalg.norm(uavs[0].getPos())/np.linalg.norm(varis.params.radius_max)
            if(percent > percent_counter):
                percent_counter += 1
                print('%% %.0f' % (percent))
            
            # update positions for uavs
            for indx in range(0,varis.params.uav_num):
                uav = uavs[indx]
                uav.moveStep()

                
            # update confidence area
            # update map based on UAV position
            # if UaV covers 50% or more, make 1
            # initialy all zeros
            # update other squares when target could have traveld 1 full square lengthwise
            self.confArea.update_area(uavs)
             
            # update time
            varis.params.timeStep()
            
            # realTime view of stuff
            if (varis.view_liveBool == True):
                self.viewLive.plotLive(self.confArea, uavs)
            
             
            # record stuff
            recorder.rec_confAreaSize(self.confArea)
            recorder.rec_anime(self.confArea)
            
            # chech if need to jump into add/subtract procedure
            if(np.linalg.norm(uavs[0].getPos())/varis.params.radius_max > varis.pso_radius_fraction and
               len(varis.uavChangeArray) > 0):
                
                print("Adding UAV")
                
                status = varis.uavChangeArray.pop()
                
                # if adding a uav
                if(status == varis.OP_ADD):
                    # add uav to end of uavs
                    # place between first and last
                    uav = self.getUav(varis.uav_num)                    
                    
                    # calc radius and position of uav
                    uav.radius = np.linalg.norm(uavs[0].getPos())
                    uav.angle = 2*math.pi + uavs[0].angle - (math.pi)/varis.uav_num
                    uav.updatePos()
                    
                    # append uavs
                    uavs.append(uav)
                    
                    
                    # increase UAV number
                    varis.uav_num += 1
                    varis.params.uav_num += 1
                    
                    # mark time when uav as added
                    recorder.uavAdded()
                    
                    # recalcualte pso path
                    varis.params.calc_psoPath()
                    
                    
                    # reference uav
                    uavs[0].setUavStatus(varis.UAV_REFERENCE)
                    
                    # make all other uavs reorient
                    for indx in range(1,varis.uav_num):
                        uavs[indx].setUavStatus(varis.UAV_REORIENT)
                    
                    # pso status is to reorient
                    uavs[0].setPsoStatus(varis.PSO_PRE_REORIENT)
                    uavs[0].startPreReorient()                 
                    
                    # update percentage
                    percent_counter = math.floor(100 * np.linalg.norm(uavs[0].getPos())/np.linalg.norm(varis.params.radius_max))
                    
                
                # else subtracting a uav
                else: 
                    # TODO: stuff
                    print('error')   
                
        
                    
        
        # print and save simulation data...
        print(recorder.toString())
        recorder.save_txt()
        recorder.save_graphs(self.confArea)
        recorder.saveAnime()



# RUN Z PROGRAM HANZ!!
if __name__ == '__main__':
    pass

    # initialize and run simulation
    confArea = ConfArea()
    confArea.begin()
    