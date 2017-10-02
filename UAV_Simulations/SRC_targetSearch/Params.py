'''
Created on Mar 19, 2017
Purpose: hold parameters for program

@author: Doug Brown
'''

from scipy import integrate
from matplotlib.pylab import *
from numba.types import none



class Params(object):    
    '''
    classdocs
    '''  
    # uav number, feild of view, speed
    uav_num = none
    uav_fov = none
    uav_speed = none
    
    # target speed and number
    target_num = none
    target_speed = none
    
    # frames per second
    fps = none
    
    # number of simulations
    simulations = none    
    
    # maximum acheivable radius
    radius_max = none
    
    # time and radius equations for spiral out motion
    pso_time = none
    pso_radius = none 
    
    # keeps track of time
    current_time = none


    def __init__(self, uav_num, uav_fov, uav_speed, target_num, target_speed, fps, simulations, time_limit):
        '''
        Constructor
        Bascially include all the parameteres
        '''
        # this just initializes the local variables
        self.uav_num = uav_num
        self.uav_fov = uav_fov
        self.uav_speed = uav_speed
        self.target_num = target_num
        self.target_speed = target_speed
        self.fps = fps
        self.simulations = simulations
        self.time_limit = time_limit
        
        # global current time that is being run for this simulation
        self.current_time = 0
        
        
        # keep track of uavs and targets
        self.uavs = []
        self.targets = []
        
        # calculate the pso path
        self.calc_psoPath()
        
        
        
    # see notes, this is the diff eq to move the uav
    def diff_eq(self, Y,t):
        eq = self.uav_num * self.uav_fov *self.uav_speed /(2*math.pi * Y[0]) - self.target_speed 
        return eq
    
    # program to solve diff eq for radial motion
    def diff_solve(self, solTime_max, solTime_step):
        self.pso_time = np.arange(1,solTime_max,solTime_step)
        self.pso_radius = integrate.odeint(self.diff_eq, 1, self.pso_time)
        self.pso_radius = np.reshape(self.pso_radius, len(self.pso_radius))
        
    def timeStep(self):
        self.current_time += 1/self.fps
    
    def reset(self):
        self.current_time = 0
        self.uavs = []
        self.targets = []
        
    # adds uav to list
    def addUav(self, uav):
        self.uavs.append(uav)
        
    # remove uav from list
    def delUav(self, indx):
        self.uavs.pop(indx)
    
    # add target to list
    def addTarget(self, target):
        self.targets.append(target)
        
    # calculate pso path
    def calc_psoPath(self):
        self.radius_max = self.get_radiusMax(self.uav_num)
        self.radius_search = self.get_radiusSearch(self.uav_num)
        
        # this is a loop to solve for the equations of motion PSO
        solTime_max = 20.0
        solTime_step = 0.01
        self.diff_solve(solTime_max, solTime_step)
        while max(self.pso_radius) < self.radius_max * 0.99:
            solTime_max *= 2
            solTime_step *= 2
            self.diff_solve(solTime_max, solTime_step)
            
    # get max search radius based on number of uavs
    def get_radiusMax(self, uav_num):
        return self.uav_fov * uav_num * self.uav_speed / (2 * math.pi * self.target_speed)
        
    def get_radiusSearch(self, uav_num):
        radius_max = self.get_radiusMax(uav_num)
        return radius_max + self.uav_fov/2
        
        
        