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

class UavPso_addSub(UavPso):
    '''
    classdocs
    '''   
    
    # pso formation status
    pso_status = none
    
    # angle that pre-reorient wil finish
    angle_preReorient_final = none
    
    # for reducing radius
    reduce_r_i = none
    reduce_r_f = none
    reduce_speed = none
    
    def __init__(self, params, indx):
        UavPso.__init__(self, params, indx)
        
        # status for uav
        self.status = varis.UAV_NORMAL
        
        # initially running normally
        self.setPsoStatus(varis.PSO_NORMAL) 
        
    # move step for UAV
    def moveStep(self):
        # check status if still running circle motion
        # once finished circle motion return to spiral out
        if(self.indx == 0 and UavPso_addSub.pso_status == varis.PSO_PRE_NORMAL):
            if(self.angle > self.angle_toReach):
                self.setPsoStatus(varis.PSO_NORMAL)
                
                # update time perameter
                radius = np.linalg.norm(self.getPos())
                time_new = np.interp(radius, varis.params.pso_radius, varis.params.pso_time)
            
                UavPso.time_shift = time_new - varis.params.current_time
        
        
        # if pso status is normal
        if(UavPso_addSub.pso_status == varis.PSO_NORMAL):
            UavPso.moveStep(self)
        
        # if prereorient
        elif(UavPso_addSub.pso_status == varis.PSO_PRE_REORIENT):
            self.moveCircle()
            
            # check if traveled full amount
            if(self.indx == 0 and self.angle > UavPso_addSub.angle_preReorient_final):
                self.setPsoStatus(varis.PSO_REORIENT)
                

        # reorient UAVs
        elif(UavPso_addSub.pso_status == varis.PSO_REORIENT):
            # check status real quick
            self.checkStatus()
            
            # non reference slow down by 2 m/s
            if(self.status == varis.UAV_REORIENT):
                # optimal distrobution
                angle_optimal = (2 * math.pi / varis.uav_num) * self.indx
                
                # move slower until it reaches optimal distance
                # remember 0th uav is reference
                angle_distance = self.angle - varis.params.uavs[0].angle
                
                if(angle_distance > angle_optimal):
                    # move circularly but slower
                    self.moveCircle_reorient(varis.uav_reorientSpeed)
                else:
                    # move circularly normal speed 
                    self.moveCircle()
                    self.setUavStatus(varis.UAV_NORMAL)

            # reference moves at contsant speed
            else:
                self.moveCircle()
        
        elif(UavPso_addSub.pso_status == varis.PSO_PRE_NORMAL):
            self.moveCircle()
                
            
        # going to smaller radius for uavs
        else:            
            # need to reduce radius untill...
            if(self.radius > UavPso_addSub.reduce_r_f):
                self.moveReduce()
                
            # reached safe radius, now reorient
            else:
                # when reached new radius, recalculate pso path 
                # set system to reorient 
                varis.params.calc_psoPath()
                self.setPsoStatus(varis.PSO_REORIENT)
                

    # reduce the radius by the speed of the target
    def moveReduce(self):
        # radial and angular velocity
        v_rad = -1 * UavPso_addSub.reduce_speed
        # pathagorien theorem and maths...
        w = math.sqrt(varis.uav_speed ** 2 - v_rad ** 2) / self.radius 
        
        # get change
        theta_delta = w / varis.params.fps
        radius_delta = v_rad / varis.params.fps
        
        # get new schtuff
        self.angle += theta_delta
        self.radius += radius_delta
        
        # update pos
        self.updatePos()
        
            
    
    # this is like morecircle but with different speed
    # move circularly, used as initial motion for uavs
    def moveCircle_reorient(self, speed):
        # angular ditance to travel in time step
        theta_delta  = speed / (UavPso_addSub.params.fps * self.radius) 
        # update angle    
        self.angle += theta_delta
        
        # update position
        self.updatePos()     
    
    # check and update uav-pso status
    def checkStatus(self):
        uavs_normal = True
        
        # remember 0th uav is the reference uav, so dont check it
        for indx in range(1,varis.uav_num):
            uav = varis.params.uavs[indx]
            
            # if not all uavs are done, need to continue reorienting    
            if uav.status != varis.UAV_NORMAL: 
                uavs_normal = False
        
        # make sure reference uav is normal
        if(self.indx == 0 and uavs_normal):
            self.setUavStatus(varis.UAV_NORMAL)
            self.setPsoStatus(varis.PSO_PRE_NORMAL)
            
            # need to travel along this path for phi distance
            phi = (2 * math.pi / varis.uav_num)
            self.angle_toReach = phi + self.angle 
            
            
    def startPreReorient(self):
        UavPso_addSub.angle_preReorient_final = self.angle + (2 * math.pi / varis.uav_num)
    
    # get status of pso formation
    def getPsoStatus(self):
        return UavPso_addSub.pso_status
    
    # set pso status
    def setPsoStatus(self, status):
        UavPso_addSub.pso_status = status
        
        # save equations for reducing schtuff
        # see paper
        if(status == varis.PSO_REDUCE_RADIUS):
            # calculate new radius
            # calculate largest angle seperation
            angle_sep = 2 * math.pi / varis.uav_num
            angle_sep = angle_sep * 2
            
            # calculate radius_max AKA final radius            
            UavPso_addSub.reduce_r_i = self.radius
            UavPso_addSub.reduce_r_f = varis.uav_fov * varis.uav_speed / (angle_sep * varis.target_speed)
            
            UavPso_addSub.reduce_speed = varis.target_speed * math.pi * 2 / angle_sep
        
        
#         if(status == varis.PSO_NORMAL):
#             print("PSO NORMAL")
#         elif(status == varis.PSO_PRE_NORMAL):
#             print("PSO PRE-NORMAL")
#         elif(status == varis.PSO_REDUCE_RADIUS):
#             print("PSO REDUCE-RADIUS")
#         elif(status == varis.PSO_REORIENT):
#             print("PSO REORIENT")
        
    def getUavStatus(self):
        return self.status
        
    def setUavStatus(self, status):
        self.status = status
        
#         if(status == varis.UAV_NORMAL):
#             print("UAV NORMAL for %d" % (self.indx))
#         elif(status == varis.UAV_REFERENCE):
#             print("UAV REFERENCE for %d" % (self.indx))
#         elif(status == varis.UAV_REORIENT):
#             print("UAV REORIENT for %d" % (self.indx))
         