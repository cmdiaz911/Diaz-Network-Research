# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 18:05:41 2017

@author: cmdiaz93
"""
import UAV_network_model as model
import time 
from operator import itemgetter
import copy

class AlgorithmVertices(object):
	
	def __init__(self, xsize, xstarting_costs, xstarting_messages, xstarting_max_outdegrees, xstarting_periods, xnode_num):
		self.size = xsize # number of parameters being tested in the simplex
		self.starting_costs = xstarting_costs
		self.starting_messages = xstarting_messages
		self.starting_max_outdegrees = xstarting_max_outdegrees
		self.starting_periods = xstarting_periods
		self.parameter_list = [] 
		self.centroid = None
		self.reflection = None 
		self.worst_parameter = None
		self.second_worst_parameter = None 
		self.best_parameter = None 
		self.number_of_nodes = xnode_num
		
	
	def CreateParameters(self):
		for parameter in xrange(self.size):
			cost = self.starting_costs[parameter] # pull out cost for this parameter
			messages = self.starting_messages[parameter] # pull out starting messages for this parameter
			max_outdegree = self.starting_max_outdegrees[parameter] # pull out max outdegrees for this parameter
			max_periods = self.starting_periods[parameter]
			self.parameter_list.append(TestParameter(cost,messages,max_outdegree,max_periods, parameter + 1))
			
	def sortSimplex(self):
		sorting_list = [] # list used to sort
		for parameter in self.parameter_list: # pull out the parameter objects
			sorting_list.append([parameter.edge_efficiency,parameter.index]) # add the values we want to look at to the sorting list
		
		sorting_list = sorted(sorting_list, key = itemgetter(0)) #sort the list by the edge efficiency
		print sorting_list
		for index in xrange(len(sorting_list)): # reassign the indeces for each parameter
			for parameter in self.parameter_list:
				if parameter.edge_efficiency == sorting_list[index][0]:
					parameter.updateIndex(index+1)
		for parameter in self.parameter_list:
			print parameter.index
			if parameter.index == self.size: # now that it has a new parameter
				self.worst_parameter = parameter
			elif parameter.index == self.size-1:
				self.second_worst_parameter = parameter
			elif parameter.index == 1:
				self.best_parameter = parameter

	def getCentroid(self):
		
		eligible_parameters = [self.parameter_list[x] for x in xrange(len(self.parameter_list)-1) ] # leaves off worst parameter
		print eligible_parameters
		
		eligible_costs = [x.cost for x in eligible_parameters] # get list of costs 
		cent_cost = int(sum(eligible_costs)/float(self.size - 1)) # centroid for cost		
		print eligible_costs

		eligible_outdegrees = [x.max_outdegree for x in eligible_parameters] # get list of us
		cent_outdegree = int(sum(eligible_outdegrees)/float(self.size -1 ))# centroid for outdegree
		print eligible_outdegrees

		eligible_periods = [x.max_period for x in eligible_parameters] # get list of periods
		cent_periods = int(sum(eligible_periods)/float(self.size -1 )) # centroid for periods
		print eligible_periods

		eligible_message_numbers = [x.message_number for x in eligible_parameters] # get list of ms
		cent_messages = sum(eligible_message_numbers)/float(self.size - 1 )# centroid for message numbers
		print eligible_message_numbers
		self.centroid = TestParameter(cent_cost, cent_messages, cent_outdegree, cent_periods, 0)
		print self.centroid
		return TestParameter(cent_cost, cent_messages, cent_outdegree, cent_periods, 0) # return the parameter for the centroid 

	def getReflection(self, xalpha,xtest_list,xfile_name, xnode_number): # calculate and return the reflection point 
		print self.centroid
		print self.worst_parameter
		r_cost  = self.centroid.cost + xalpha*(self.centroid.cost - self.worst_parameter.cost)
		r_outdegree = max(int(.2*self.number_of_nodes),int(self.centroid.max_outdegree + xalpha*(self.centroid.max_outdegree - self.worst_parameter.max_outdegree)))
		r_periods = self.centroid.max_period + xalpha*(self.centroid.max_period - self.worst_parameter.max_period)
		r_messages = self.centroid.message_number + xalpha*(self.centroid.message_number - self.worst_parameter.message_number)
		self.reflection = TestParameter(r_cost, r_messages,r_outdegree, r_periods, 'r')
		self.reflection.getModelValues(xtest_list, xfile_name, xnode_number)
		reflection = self.reflection
		return reflection


	def getExpansion(self, xgamma,xtest_list,xfile_name,xnode_number): # calculate and return the expansion point
		e_cost  = self.centroid.cost + xgamma*(self.reflection.cost - self.centroid.cost)
		e_outdegree = max(int(.2*self.number_of_nodes),int(self.centroid.max_outdegree + xgamma*(self.reflection.max_outdegree - self.centroid.max_outdegree)))
		e_periods = self.centroid.max_period + xgamma*(self.reflection.max_period - self.centroid.max_period)
		e_messages = self.centroid.message_number + xgamma*(self.reflection.message_number - self.centroid.message_number)
		expansion = TestParameter(e_cost, e_messages,e_outdegree, e_periods, 'e')
		expansion.getModelValues(xtest_list, xfile_name, xnode_number)
		return expansion


	def getContraction(self, xrho, xtest_list, xfile_name, xnode_number): # calculate and return the contraction point
		c_cost  = self.centroid.cost + xrho*(self.worst_parameter.cost - self.centroid.cost)
		c_outdegree = max(int(.2*self.number_of_nodes),int(self.centroid.max_outdegree + xrho*(self.worst_parameter.max_outdegree - self.centroid.max_outdegree)))
		c_periods = self.centroid.max_period + xrho*(self.worst_parameter.max_period - self.centroid.max_period)
		c_messages = self.centroid.message_number + xrho*(self.worst_parameter.message_number - self.centroid.message_number)
		contraction = TestParameter(c_cost, c_messages, c_outdegree, c_periods, 'c')
		contraction.getModelValues(xtest_list, xfile_name, xnode_number)
		return contraction


	def computeShrink(self,xsigma):
		for parameter in(x for x in self.parameter_list if x != 1):
			parameter.cost = self.best_parameter.cost + xsigma*(parameter.cost - self.best_parameter.cost)
			parameter.max_outdegree = max(int(.2*self.number_of_nodes),int(self.best_parameter.max_outdegree + xsigma*(parameter.max_outdegree - self.best_parameter.max_outdegree)))
			parameter.max_period = self.best_parameter.max_period + xsigma*(parameter.max_period - self.best_parameter.max_period)
			parameter.message_number = self.best_parameter.message_number + xsigma*(parameter.message_number - self.best_parameter.message_number)

	def insertNewParameter(self, newParameter, xbest = False):
		self.parameter_list.remove(self.worst_parameter) # remove the occurence of the worst parameter from the paramter list
		newParameter.updateIndex(self.size) # set the index of the new parameter to the worst index
		self.parameter_list.append(newParameter) # add the new parameter to the list of parameters
		
		if xbest: # if incoming new parameter is the better than current best, make the change
			self.best_parameter = newParameter
		
class TestParameter(object):
	
	def __init__(self, xcost, xmessage_number, xmax_outdegree, xmax_period, xindex,xmodel_runs = 1):
		self.cost = xcost
		self.message_number = xmessage_number
		self.max_outdegree = xmax_outdegree
		self.max_period = xmax_period
		self.model_runs = xmodel_runs
		self.index = xindex
		self.edge_efficiency = None
		self.inverse_distance = None
		self.edge_ratio = None
	
	def getModelValues(self, xtest_list, xfile_name, xnode_number):
		edge_ratios = [] # intermediate to hold for average edge ratio
		edge_efficiencies = [] #intermediate to hold for efficiency calculation
		inverse_distances = [] # intermediate to hold for
		message_num = self.message_number
		max_periods = self.max_period
		max_outdegree = self.max_outdegree
		costs = self.cost
		
		for iteration in xrange(self.model_runs):
			model_results = model.runsimulation(xnode_number,xtest_list,message_num,max_periods,max_outdegree,costs, xfile_name)
			edge_ratios.append(model_results[0])
			edge_efficiencies.append(model_results[2])
			inverse_distances.append(model_results[1])
		self.inverse_distance = sum(inverse_distances)/float(self.model_runs) # update the inverse distance value
		self.edge_ratio =sum(edge_ratios)/float(self.model_runs) # update the edge ratio value
		self.edge_efficiency = sum(edge_efficiencies)/float(self.model_runs) # update the edge efficiency value 

	def updateIndex(self,new_index):
		self.index = new_index
	
	def returnParameterList(self):
		return [self.cost, self.message_number, self.max_outdegree, self.max_period, self.edge_efficiency]

def NelderMeadAlgorithm(xtest_list, xtest_file, xnode_number,xstarting_parameters,xstalling_parameter = 10, xrho = .5, xalpha = 1, xgamma = 2, xsigma = .5):
	number_of_vertices = len(xstarting_parameters['costs'])
	list_of_vertices = AlgorithmVertices(number_of_vertices, xstarting_parameters['costs'],xstarting_parameters['messages'], xstarting_parameters['out_degrees'], xstarting_parameters['periods'],xnode_number)
	list_of_vertices.CreateParameters() # create the vertices object and the parameters
	list_of_best_parameters = [] # will keep track of the history of the best parameters as the best parameter is updated 
	best_efficiency = 100000  # tracks best value during this iteration of the algorithm
	best_parameter_setting = None # tracks the best parameter during this iteration of the algorithm
	stalling_count = 0
	
	while stalling_count < xstalling_parameter: # start the algorithm iterations 

		for parameter in list_of_vertices.parameter_list: # calculate the values for all of the parameters
			parameter.getModelValues(xtest_list, xtest_file, xnode_number) 

		list_of_vertices.sortSimplex() # sort the simplex
		list_of_vertices.getCentroid() # calculate the centroid 

		reflection_point = list_of_vertices.getReflection(xalpha, xtest_list, xtest_file, xnode_number) # calculate the value of the reflection point
		
		if reflection_point.edge_efficiency < list_of_vertices.second_worst_parameter.edge_efficiency and reflection_point.edge_efficiency > list_of_vertices.best_parameter.edge_efficiency:
			list_of_vertices.insertNewParameter(reflection_point) # add the reflection point to the simplex. Remove worst paramter
			print "Iteration Stopped at Reflection"
		elif reflection_point.edge_efficiency < list_of_vertices.best_parameter.edge_efficiency:
			expansion_point = list_of_vertices.getExpansion(xgamma, xtest_list, xtest_file, xnode_number)
			
			if expansion_point.edge_efficiency < reflection_point.edge_efficiency: # if the expansion point is better 
				list_of_vertices.insertNewParameter(expansion_point, True) # add it to the simplex, update best parameter
				print "Iteration Stopped at Expansion"
			else:
				list_of_vertices.insertNewParameter(reflection_point, True) # add reflection point to simplex, add it to the simplex
				print "Iteration Stopped at Expansion"
		else:
			contraction_point = list_of_vertices.getContraction(xrho, xtest_list, xtest_file, xnode_number)
			if contraction_point.edge_efficiency < list_of_vertices.worst_parameter.edge_efficiency:
				list_of_vertices.insertNewParameter(contraction_point)
				print "Iteration Stopped at Contraction"
			else:
				list_of_vertices.computeShrink(xsigma)
				print "Iteration Stopped At Shrink"


		if list_of_vertices.best_parameter.edge_efficiency < best_efficiency: # if there is a new best global value
			best_efficiency = list_of_vertices.best_parameter.edge_efficiency
			list_of_best_parameters.append(copy.deepcopy(list_of_vertices.best_parameter))
			best_parameter_setting = copy.deepcopy(list_of_vertices.best_parameter)
			stalling_count = 0
			
		else:
			stalling_count += 1 
		
		print ""
		print list_of_vertices.best_parameter.returnParameterList()
		print "Current Stalling Count = ", stalling_count
		print "Best Value History = ", [x.edge_efficiency for x  in list_of_best_parameters]
		print ""
	output_dictionary = {'best_parameter': list_of_vertices.best_parameter, 'run_history':list_of_best_parameters,\
	'global min':best_efficiency, 'global min parameter': best_parameter_setting}
	
	return output_dictionary
	
