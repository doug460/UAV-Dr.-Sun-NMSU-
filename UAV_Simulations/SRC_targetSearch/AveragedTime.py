'''
Created on Sep 3, 2018

@author: DougBrownWin

create averaged time file of simulations
'''

from SaveDirs import DIR_DATA
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    pass

    # just doing 4 targets and 2 UAVs for raster and PSO
    folder = DIR_DATA
    fileRast = folder + "raster.npy"
    filePso = folder + "pso.npy"
    
    dataRast = np.load(fileRast)
    dataPso = np.load(filePso) 
    
    pRast = plt.plot(dataRast)
    pPso = plt.plot(dataPso)
    
    plt.title('Average Time vs Simulations')
    plt.xlabel('Simulation')
    plt.ylabel('Averaged Time (s)')
    
    plt.legend(('Raster', 'PSO'))    
    
    fileSave = DIR_DATA + 'AveragedTime.png'
    plt.savefig(fileSave)