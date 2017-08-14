'''
Created on Jul 27, 2017

@author: Doug Brown
'''

class RecordData(object):
    '''
    classdocs
    
    record and save/print data about continuous attack simulation
    '''


    def __init__(self, params, target_angles, target_seperation, pso_radius_percent):
        '''
        Constructor
        '''
        
        # initial target and UAV number
        # number of targets will be updated by method
        self.targets_num = 0
        self.uav_num = 0
        
        self.target_angles = target_angles
        self.target_seperation = target_seperation
        
        # keeps track of targets detected and successful attacks
        self.targets_det = 0
        self.targets_success = 0
        
        self.params = params
        
        self.pso_radius_percent = pso_radius_percent
        
    # a target was generated
    def addTarget(self):
        self.targets_num += 1
        
    # a UAV was generated
    def addUAV(self):
        self.uav_num += 1
    
    # add one to num of targets that where detected
    def targetDetect(self):
        self.targets_det += 1
    
    # add one to num of targets that were successful at attacking
    def targetSuccess(self):
        self.targets_success += 1
        
    # print out string information 
    def toString(self):
        buf = "This is the continous attack simulation\n-------------\n"
        buf += "Of %d targets:\n" % (self.targets_num)
        buf += "\t Detected: %d\n\t Successfully attacked: %d\n" % (self.targets_det, self.targets_success)
        buf += "Time to reach %f of max radius and one loop for PSO: %f (s)\n" % (self.pso_radius_percent, self.params.time_limit)
        buf += "Target info:\n"
        buf += "\t Target Num = %d\n\t Target Speed = %d\n" % (self.targets_num, self.params.target_speed) 
        buf += "UAV info:\n\t UAV num = %d\n\t UAV speed = %d\n" % (self.uav_num, self.params.uav_speed)
        buf += "Max Radius = %f \nMax Searchable Radius = %f\n" % (self.params.radius_max, self.params.radius_search) 
        
        return(buf)
        
        
    
        
        
        