'''
created: 4-11-17
creator: Doug Brown

Purpose: basically to start at a spicific location based on radius and angle
	From there it is to attack the origin
	if it reaches the origin it is successfull, if detected it failed
'''

from numba.types import none
from numpy import math
import numpy as np
import copy

DETECTED = 1
ATTACKING = 2
SUCCESSFULL = 3

class TargetAttack(object):

	# class variable for params
	params = none
	
	
	# initialize target stuffs
	def __init__(self, params, indx, radius):
		# need params
		# update params for class only once
		TargetAttack.params = params
		
		# initialize position of target 
			# need angle and radius
			# save initial posistion into a variable
		angle = indx * (2 * math.pi / params.target_num) 
		x = radius * math.cos(angle)
		y = radius * math.sin(angle)
		
		self.position = np.array([x,y])
		self.initial_position = copy.deepcopy(self.position)
		
		# update direction towards center 
		# cos and sin are already normalized...
		self.direction = np.array([-math.cos(angle), -math.sin(angle)])
		self.shift = self.direction * TargetAttack.params.target_speed / TargetAttack.params.fps
		
		# initialize status of target as ATTACKING	
		self.status = ATTACKING
	
	
	# make target move
	def moveStep(self):
		# basically get radial vector, and move towards center by step amount		
		self.position += self.shift
	
	
	# get position of target
	def getPos(self):
		return self.position
		
	# update status of target (DETECTED OR SUCCESSFULL)
	def setStatus(self, status):
		self.status = status
		
	# return what the initial posistion of the uav 
	def get_initialPos(self):
		return self.initial_position
	
	# get target status
	def getStatus(self):
		return self.status