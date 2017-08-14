'''
created: 4-11-17
creator: Doug Brown
Purpose: to record data about attack simulation
'''
from TargetAttack import SUCCESSFULL
import matplotlib.pyplot as plt
import numpy as np
import math

class Data(object):
	
	def __init__(self, params, save_dir):
		# need directory to save information to
		self.save_dir = save_dir
		
		# store params object
		self.params = params
		
		# initialize list of successfull posistions
		self.successfull_positions = []
		
	
	# record successfull locations of attack for targets
	def recordSuccess(self, params):
		# step through targets that were successfull
		# if successful, save that position to array
		for target in params.targets:
			if(target.status == SUCCESSFULL):
				self.successfull_positions.append(target.get_initialPos())
	
	
	
	
	# going to record graph
	# record additional data
	
	# include percent of 2*pi that detection failed
			# save image of successful attacks and data information
			# include path of uavs from last run so as to see the full motion of uavs
	def saveData(self):
		# save toStrign() to txt file
		buf = self.save_dir + "info" + '.txt'
		file = open(buf, 'w')
		file.write(self.toString())
		file.close()
		
		
		self.saveGraph()
	
	
	
	# save graph of simulation
		# uavs paths
		# targets successfull initial locations
		# legend... wait for it... dary!! to show what lines mean what
	def saveGraph(self):
		for point in self.successfull_positions:
			plt.plot(point[0],point[1],'b+')
			
		# plot circle around searchable area
		radius = self.params.radius_search
		t = np.arange(0, 2 * math.pi, 0.01)
		x = np.cos(t) * radius
		y = np.sin(t) * radius
		plt.plot(x,y,'k--')
		
		plt.title('Successful target positions of attack')
		plt.xlabel('East (m)')
		plt.ylabel('North (m)')
		
		buf = self.save_dir + 'successAttack.png'
		plt.savefig(buf)
		
	
		
	
	# return string of information about the data run
	def toString(self):
		buf = ''
		buf += "Max Radius = %f \n\t Max Searchable Radius = %f\n" % (self.params.radius_max, self.params.radius_search) 
		buf += "Uav info:\n\tNumber: %d\n\tSpeed: %d\n\tD_fov: %d\n\tfps: %d\n" % (self.params.uav_num, self.params.uav_speed, self.params.uav_fov,
		                                                                        self.params.fps)
		buf += "TargetRandom info:\n\tNumber %d\n\tSpeed: %d\n" % (self.params.target_num, self.params.target_speed)         
		return buf
		
		# add info for failure rate of uav to defend
		# need number of successful directions devided by total number of attacks
		
		# initial attack radius
		# max attack radius
		# radial step size
		# number of radii 
		
		
		# number of uavs
		# uav speed
		# uav type
		# field of view
		
		# number of targets for one radius
		# target speed
		# target type