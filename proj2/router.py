from physical import physical_layer
from link import link_layer
from network import Network_layer
from package import package
from master import master
import weakref
import math
import logging

class router:

	_instances = set()	#atribute protect to save all instances of host

	def __init__(self,ip1, ip2, mac1, mac2, master):	#delfaut constructor
		self.physical = physical_layer(self)
		self.link = link_layer(self)
		self.network = Network_layer(self)
		self.master = master
		# self.reach = reach
		self.ip1 = ip1
		self.ip2 = ip2
		self.mac1 = mac1
		self.mac2 = mac2
		# self.positionx = x
		# self.positiony = y
		self._instances.add(weakref.ref(self))

	@classmethod	#to list all instances of host class
	def get_instances(cls):
		dead = set()
		for ref in cls._instances:
			obj = ref()
			if obj is not None:
				yield obj
			else:
				dead.add(ref)
		cls._instances -= dead

	def send_message(self,message,destination):	#send the package to network layer
		self.network.send_pck(message,destination)		
		

	# def is_reacheable(self,neighbor):	#check if neighbor host is reacheable
	# 	first_part = ((self.positionx - neighbor.positionx)**2) #(1,0)->1,9=3.16, (2,3)->1,4=2.23, (3,5)->4,25=5.38
	# 	second_part = ((self.positiony - neighbor.positiony)**2)
	# 	distance = math.sqrt(first_part + second_part)
		
	# 	if distance == 0: 	# to not add itself on the neighbors list
	# 		return distance
	# 	else:
	# 		return distance <= self.reach #returns true if is reacheable

	# def get_neighbors(self):	#get all neighbors of a host
	# 	neighbors = []
	# 	for obj in host.get_instances():
	# 		if(self.is_reacheable(obj)):	#check if a node is reacheable
	# 			neighbors.append(obj)	#add to the list of neighbors
	# 	return neighbors #returns the list

	def get_neighbors(self):	#get all neighbors of a host
		neighbors = []
		for obj in host.get_instances():
			if(self.is_reacheable(obj)):	#check if a node is reacheable
				neighbors.append(obj)	#add to the list of neighbors
		return neighbors #returns the list

	def get_ip(self):	#returns the mac address
		return self.ip	

	def get_mac(self):	#returns the mac address
		return self.mac 	

	# def get_positionx(self):	#returns the first coordinate location
	# 	return self.positionx

	# def get_positiony(self):	#returns the second coordinate location
	# 	return self.positiony

	def get_reach(self):	#returns the reach
		return self.reach