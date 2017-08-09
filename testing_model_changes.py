# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 18:00:42 2017

@author: Chris
"""

import time
from reading_networks_2 import dict_of_nets
from reading_networks_2 import sample_list_by_node_number 
from DDIP_Algorithm_Procedure import runsimulation
from ergm_sample_set_creator import ergm_samples_dict # set of ergm sample graphs 
from ergm_sample_set_creator import ergm_file_dict # set of file names for the ergm graphs 
from BOBYQA_Optimization_Algorithm import alg_results
import datetime as dt 

node_number_list = [10,15,20,25,30,40]
#
list_of_results = [] 
test_periods = 10 
test_node_index = 0
iterations = 0 
tests_per_sample = 10
seed = dt.datetime.today().minute
start_time = time.clock()
#nelder_mead_gammas = [.6424, .555, 1.288, 5.0475,2.786,2.8098 ]
#nelder_mead_scaling = [1.0964, 1.21,.8637,.526,.70884]
for index in range(0,3):
	test_gamma = alg_results[index][0][0] # what do I make this 
	test_scaling_factor = alg_results[index][0][1] # not sure if this should be large or small, will have to test the model and print choices until this makes sense
	print test_gamma
	print test_scaling_factor
	for file_name in sample_list_by_node_number[test_node_index]:
		test_file = file_name
		test_edge_set = dict_of_nets[node_number_list[test_node_index]][test_file]['edge_set']
		for i in xrange(tests_per_sample):

			list_of_results.append(runsimulation(node_number_list[test_node_index],test_gamma,test_scaling_factor,test_edge_set,test_periods, test_file, seed)[1])
			
			list_of_results[iterations].ReportResults()
			end_time = time.clock()
			
			print "Total Time for Model = ", end_time - start_time 
			print "Test Node Size = ",node_number_list[test_node_index]
			print "Number of Iterations = ",iterations
			print "Unit Disk Graphs"
			print "" 
			iterations +=1
	
	for file_name in ergm_file_dict[node_number_list[test_node_index]]:
		test_file = file_name
		test_edge_set = ergm_samples_dict[node_number_list[test_node_index]][test_file]['edge_set']
		for i in xrange(tests_per_sample):

			list_of_results.append(runsimulation(node_number_list[test_node_index],test_gamma,test_scaling_factor,test_edge_set,test_periods, test_file, seed)[1])
			
			list_of_results[iterations].ReportResults()
			end_time = time.clock()
			
			print "Total Time for Model = ", end_time - start_time 
			print "Test Node Size = ",node_number_list[test_node_index]
			print "Number of Iterations = ",iterations
			iterations +=1
	test_node_index +=1