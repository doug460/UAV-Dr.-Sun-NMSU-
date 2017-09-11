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
	
	def __init__(self, params, save_dir, initial_radius, final_radius, radial_stepSize):
		# need directory to save information to
		self.save_dir = save_dir
		
		# store params object
		self.params = params
		
		# radius info
		self.initial_radius = initial_radius
		self.final_radius = final_radius
		self.radial_stepSize = radial_stepSize
		
		# initialize list of successfull posistions
		self.successfull_positions = []
		
		# for recording positions
		self.list_positions = []
		self.uavs_pos = []
		
		# keep track of radii
		self.radii = []
		
	
	# record successfull locations of attack for targets
	def recordSuccess(self, params):
		# step through targets that were successfull
		# if successful, save that position to array
		for target in params.targets:
			if(target.status == SUCCESSFULL):
				self.successfull_positions.append(target.get_initialPos())
				
	# record uav positions for graph
	def recordUavsPos(self, uavs):			
		# update uavs
		for indx in range(0,self.params.uav_num):
			uav = uavs[indx]
			list_positions = self.uavs_pos[indx]
			array = [uav.position[0], uav.position[1]]
			list_positions.append(array)
			
	# initialize uav positions
	def initUavsPos(self, uavs):
		# initializing uavs positions
		for indx in range(0,self.params.uav_num):
			uav = uavs[indx]
			array = [uav.position[0], uav.position[1]]
			self.list_positions.insert(0,array)
			self.uavs_pos.insert(indx,self.list_positions) 
	
	# record radii
	def recordRadii(self, radius):
		self.radii.append(radius)
	
	
	
	
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
			plt.plot(point[0],point[1],'bP')
			
		# plot circle around searchable area
		radius = self.params.radius_search
		t = np.arange(0, 2 * math.pi, 0.01)
		x = np.cos(t) * radius
		y = np.sin(t) * radius
		plt.plot(x,y,'k--')
		
		# plot uavs
		for indx in range(0,self.params.uav_num):
			array = self.uavs_pos[indx]
			x = [item[0] for item in array]
			y = [item[1] for item in array]
			plt.plot(x,y, 'r-')
			
			# mark initial posistion
			plt.plot(x[0],y[0],'o')
			
		# plot circle around each uav
		for indx in range(0,self.params.uav_num):
			radius = self.params.uav_fov/2
			t = np.arange(0, 2 * math.pi, 0.01)
			array = self.uavs_pos[indx][len(self.uavs_pos[indx]) - 1]
			x = np.cos(t) * radius + array[0]
			y = np.sin(t) * radius + array[1]
			plt.plot(x,y,'g:')
		
		# plot circle at each radii
		for radius in self.radii:
			t = np.arange(0, 2 * math.pi, 0.01)
			x = np.cos(t) * radius
			y = np.sin(t) * radius
			plt.plot(x,y,'k.',markersize = 0.5)
		
		plt.title('Successful target positions of attack')
		plt.xlabel('East (m)')
		plt.ylabel('North (m)')
		
		buf = self.save_dir + 'successAttack.png'
		plt.savefig(buf)
		
	
	# print info
	def printTxt(self):
		print(self.toString())
	
	# return string of information about the data run
	def toString(self):
		buf = 'Of %d targets, %d successfully attacked\n' % (self.params.target_num * self.params.simulations,
															len(self.successfull_positions))
		buf += 'Defense rate = %f %%\n' % (100 * (self.params.target_num * self.params.simulations - len(self.successfull_positions))/
										(self.params.target_num * self.params.simulations))
		buf += 'Radius info:\n'
		buf += '\tInitial target radius: %f\n' % (self.initial_radius)
		buf += '\tFinal target radius: %f\n' % (self.final_radius)
		buf += '\tTarget radius stepsize: %f\n' % (self.radial_stepSize)
		buf += "Max Radius = %f \n\t Max Searchable Radius = %f\n" % (self.params.radius_max, self.params.radius_search) 
		buf += "Uav info:\n\tNumber: %d\n\tSpeed: %d\n\tD_fov: %d\n\tfps: %d\n" % (self.params.uav_num, 
																				self.params.uav_speed, self.params.uav_fov,
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