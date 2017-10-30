'''
Created on Sep 3, 2017

@author: DougBrownWin

program for viewing stuff live
'''

import matplotlib.pyplot as plt
import numpy as np
import math

class ViewLive(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        
        nothing special here....
        '''
        
        plt.ion()

    
    
    # plot live view of matrix area
    def plotLive(self, targets, uavs):
        plt.clf()
        for target in targets:
            pos = target.position
            plt.plot(pos[0], pos[1], 'xk')
        
        for uav in uavs:
            pos = uav.position
            plt.plot(pos[0], pos[1], '.k')
        
        
        # pritn title
        plt.title('Live view')
        
        plt.pause(0.05)
        