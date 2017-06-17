# -*- coding: utf-8 -*-
"""
Created on Sun Jun 04 15:40:09 2017

@author: Chris
"""

# import the packages used in the program
import nlopt
import numpy as np
import datetime as dt # used to set the seed for the algorithm 

# import the data sets that will be used to compute the BOBYQA
from ergm_sample_set_creator import ergm_samples_dict
from ergm_sample_set_creator import ergm_file_dict # set of file names for the ergm graphs 
from reading_networks_2 import sample_list_by_node_number
from reading_networks_2 import dict_of_nets
import DDIP_Algorithm_Procedure as model

def BOYBQA_Optimizer(xinit_parameters, xlower_bounds, xupper_bounds,xdx, xnode_sizes_list, xmax_eval = 2):
	seed = dt.datetime.today().minute # this seed will  be used to avoid the inconsistences that come with testing the model using different starting parameters 
	lists_per_set_type = 3 # not exactly a parameter to the optimization model, so will not put it in as an argument 
	node_index = 0 # starts at 10 when 0, 15 when 1 etc 
	optimimum_values = [] 
	for node_num in xnode_sizes_list:
		
		opt = nlopt.opt(nlopt.LN_BOBYQA, 3)# create the BOBYQA algorithm 
		opt.set_lower_bounds(xlower_bounds) # set the lower bounds
		opt.set_upper_bounds(xupper_bounds) # set the upper bounds 
		opt.set_default_initial_step(xdx)
		
		# set up the test sample graph name list for the function 
		file_list = sample_list_by_node_number[node_index][0:lists_per_set_type]
		for x in range(lists_per_set_type):
			file_list.append(ergm_file_dict[node_num][x])
		
		# write the objective function for the model 
		# the objective function will evaluate x number of graphs of each type
		# the objective function evaluation is equal to the sum of the efficencies of the model runs based on the parameter inputs 
		def optimization_function(parameters, grad):
			index = 0
			list_of_objectives = [] # will save the objective values 
			# block of code gets the test edge sets that corresponds to the file being looked at 
			for file_name in file_list:
				if file_name[-2] == 'x':
					xtest_list = ergm_samples_dict[node_num][file_name]['edge_set']
				else:
					xtest_list= dict_of_nets[node_num][file_name]['edge_set']
				# parameter 0 = gamma, parameter 1 = scaling factor, parameter 2 = number of iterations 
				model_results = model.runsimulation(node_num, parameters[0], parameters[1], xtest_list, parameters[2], file_name, seed)[0] # to get the result list from the procedure method
				list_of_objectives.append(model_results[2]) # gets 1 / edge efficiency to allow the algorithm to try to minimize 
			
			objective_value = sum(list_of_objectives) # calculate the sum of all model results to get the objective value 
			index += 1
			print index
			return objective_value 

		opt.set_min_objective(optimization_function) # set the objective equation_up
		opt.set_maxeval(xmax_eval) # set the stopping criteria 
		xopt = opt.optimize(xinit_parameters) # run the algorithm 
		
		# save the optimized parameters and values to a list, the result of the algorithm call, and the number of nodes it refers to 
		optimimum_values.append([xopt,opt.last_optimum_value(), node_num])
		
		# go on to the next node size if applicable 
		node_index += 1
	return optimimum_values # return the list of lists that contains the optimimum results for each node size

# set the algorithm parameters 
lower_bounds = np.array([.75, 0.5, 5])
upper_bounds = np.array([3.0, 3.0, 30])
initial_parameters = np.array([1.00, .75, 10])
initial_step_sizes = np.array([.01, .05, 1])
#node_sizes = [10,15,20,25]
node_sizes = [10] 

alg_results = BOYBQA_Optimizer(initial_parameters, lower_bounds, upper_bounds, initial_step_sizes, node_sizes)
print alg_results
best_gamma = alg_results[0][0]
best_scaling_factor =  alg_results[0][1]
best_periods = alg_results[0][1]
