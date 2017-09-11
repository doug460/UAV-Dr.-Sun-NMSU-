'''
Created on Mar 15, 2017

@author: Doug Brown
'''

import numpy as np
from scipy import integrate
from matplotlib.pylab import *
from numba.types import none
from UavPso import UavPso
import Variables as varis
from SRC_confidenceArea.Variables import UAV_NORMAL

class UavPso_addSub(UavPso):
    '''
    classdocs
    '''   
    
    # pso formation status
    pso_status = none
    
    def __init__(self, params, indx):
        UavPso.__init__(self, params, indx)
        
        # status for uav
        self.status = varis.UAV_NORMAL
        
        # initially running normally
        UavPso_addSub.pso_status = varis.PSO_NORMAL 
        
    # move step for UAV
    def moveStep(self):
        # if pso status is normal
        if(UavPso_addSub.pso_status == varis.PSO_NORMAL):
            UavPso.moveStep(self)
        
        # reorient UAVs
        elif(UavPso_addSub.pso_status == varis.PSO_REORIENT):
            # non reference slow down by 2 m/s
            if(self.status == UAV_NORMAL):
                
            # reference moves at contsant speed
            else:
                
            
        # going to smaller radius for uavs
        else:
            print('blank')
            
    
    # this is like morecircle but with different speed
    # move circularly, used as initial motion for uavs
    def moveCircle_reorient(self, speed):
        # angular ditance to travel in time step
        theta_delta  = speed / (UavPso_addSub.params.fps * self.radius) 
        # update angle    
        self.angle += theta_delta
        
        # update position
        self.updatePos()        
    
    
    # get status of pso formation
    def getPsoStatus(self):
        return UavPso_addSub.pso_status
    
    # set pso status
    def setPsoStatus(self, status):
        UavPso_addSub.pso_status = status
        
    def getUavStatus(self):
        return self.status
        
    def setUavStatus(self, status):
        self.status = status
        