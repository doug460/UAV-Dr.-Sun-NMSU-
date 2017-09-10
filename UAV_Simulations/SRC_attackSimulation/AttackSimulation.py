'''
created: 4-11-17
creator: Doug Brown

Purpose: run the loop to simulate the attack

'''

from Params import Params
from TargetAttack import TargetAttack, ATTACKING
from UavPso import UavPso
from UavRaster import UavRaster
from Data import Data
from CheckDetect_attack import CheckDetect_attack
import time
import os
import errno
import numpy as np

from SaveDirs import DIR_DATA

# type of uav to be used
UAV_PSO = 1
UAV_RASTER = 2

# type of target to be used
TARGET_ATTACK = 1


class AttackSimulation(object):
	
	def __init__(self, params, uav_id, target_id, initial_radius, final_radius, radial_stepSize):
		'''
		Constructor
		'''
		self.params = params
		
		# need to now what radius to start targetw at and how many radii are going to be created
		self.final_radius = final_radius
		self.radial_stepSize = radial_stepSize		
		self.initial_radius = initial_radius
		
		# target_id should be an attack target which goes to origin
		self.target_id = target_id
		self.uav_id = uav_id
		
		if(uav_id == UAV_PSO):
			self.name_id = 'uavPso_'
		elif(uav_id == UAV_RASTER):
			self.name_id = 'uavRaster_'
		
		if(target_id == TARGET_ATTACK):
			self.name_id += 'targetAttack'
	
	# this controls which target object to return
	def getTarget(self, params, indx, radius):
		if(self.target_id == TARGET_ATTACK):
			target = TargetAttack(params, indx, radius)
		else:
			raise ValueError('Target_id class id not recognized')
		params.addTarget(target)
		return(target)
	
			
	# this controls which uav object to return
	def getUav(self, params, indx):
		if(self.uav_id == UAV_PSO):
			uav = UavPso(params,indx)
		elif(self.uav_id == UAV_RASTER):
			uav = UavRaster(params,indx)
		else:
			raise ValueError('Uav_id class id not recognized')
		
		# add uav to params
		params.addUav(uav)
		
		return(uav)
	
	
	
	# start of program
	def begin(self):
		# specify save directory
		# directory to which to save data
		save_dir = DIR_DATA + "/" + time.strftime('%Y-%m-%d--%H-%M-%S--') + self.name_id + "/"
		if not os.path.exists(save_dir):
			try: 
				os.makedirs(save_dir)
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					raise
		
		params = self.params
		
		# create DATA object to hold successful locations of attacks from targets
		# DATA object will also hold what ever information that I wish it to hold
		data = Data(self.params, save_dir)
		
		# create detection object for check status of targets with respect to uavs
		checkDetect = CheckDetect_attack()
		
		# get total simulations
		total_sims = (self.final_radius - self.initial_radius)/self.radial_stepSize + 1
		self.params.simulations = total_sims
		
		# FOR_LOOP: steps throgh different radii of attack
		for radius in np.arange(self.initial_radius, self.final_radius + self.radial_stepSize, self.radial_stepSize):
			# reset variables for new run	
			self.params.reset()	
			current_sim = (radius - self.initial_radius)/self.radial_stepSize + 1
			buf = "Running %d of %d simulations" % (current_sim, total_sims)
			print(buf)
			
			# create targets
			# want to create # of targets evenly distributed angularly 
			# radius depends on radius of attack indx from current loop
			targets = []
			for indx in range(0,params.target_num):
				target = self.getTarget(params, indx, radius)
				targets.insert(indx,target)			
			
			# create uavs
			uavs = []
			for indx in range(0,params.uav_num):
				uav = self.getUav(params, indx)
				uavs.insert(indx, uav)	
				
			# initialize uav position recorder
			data.initUavsPos(uavs)
				
			
			# WHILE_LOOP till all targets are detected or successfull
			while(checkDetect.shouldContinue(params)):		
				# move targets and uavs
				for target in targets:
					if(target.status == ATTACKING):
						target.moveStep()
				
				for uav in uavs:
					uav.moveStep()
					
				# if on last simulation, record uav path
				if(current_sim == total_sims):
					data.recordUavsPos(uavs)
				
				
				# check if detected or if attack was successful
					# update targets status
				checkDetect.updateStatus(params)
					
			# record positions of successful attacks
			data.recordSuccess(params)	
			data.recordRadii(radius)
			
			
		
				
		# tentative: maybe create video where it shows an attack simulation
		# start targets at successful locations
		# non-successful angles start at farthest radius
		# different symbol for success vs failed targets
		
		
		# DATA object: save attack information 
		data.saveData()
		data.printTxt()
		
		
		