# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 18:00:42 2017

@author: Chris
"""
import os
import cPickle as pickle
import time
from reading_networks_2 import dict_of_nets
from reading_networks_2 import sample_list_by_node_number 
from DDIP_Algorithm_Procedure import runsimulation
from ergm_sample_set_creator import ergm_samples_dict  # set of ergm sample graphs
from ergm_sample_set_creator import ergm_file_dict  # set of file names for the ergm graphs
# from BOBYQA_Optimization_Algorithm import alg_results
import datetime as dt


def updatePickleFile(results_file_name, object, list_of_results):
	if os.path.exists(results_file_name):
		with open(results_file_name, 'rb') as rfp:
			list_of_results = pickle.load(rfp)
	list_of_results.append(object)
	with open(results_file_name, 'wb') as wfp:
		pickle.dump(list_of_results, wfp)

node_number_list = [10, 15, 20, 25, 30, 40]

list_of_results = [] 
test_periods = 10 
test_node_index = 0
iterations = 0  
tests_per_sample = 10

start_time = time.clock()
bobyqa_gammas = [.15, .31393763, .860153, .860, .2821, 1.6098]
bobyqa_scaling = [1.49912575, 1.21323, .925535, 1.17, .90, 1.70884]
bobyqa_rounds = [15, 15, 22, 10, 15, 15]
for index in range(6):
	result_pickle_objects = []
	pickle_file_name = "%s_node_model_results.pkl" % node_number_list[test_node_index]
	test_gamma = bobyqa_gammas[test_node_index]  # what do I make this
	test_scaling_factor = bobyqa_scaling[test_node_index]  # not sure if this should be large or small,
	test_periods = bobyqa_rounds[test_node_index]
	# will have to test the model and print choices until this makes sense
	# print test_gamma
	# print test_scaling_factor
	for file_name in sample_list_by_node_number[test_node_index]:
		test_file = file_name
		test_edge_set = dict_of_nets[node_number_list[test_node_index]][test_file]['edge_set']
		for i in xrange(tests_per_sample):
			seed = dt.datetime.today().second
			list_of_results.append(runsimulation(node_number_list[test_node_index], test_gamma, test_scaling_factor,
												test_edge_set, test_periods, test_file, seed)[1])
			
			list_of_results[iterations].ReportResults()
			end_time = time.clock()

			updatePickleFile(pickle_file_name, list_of_results[iterations], result_pickle_objects)
			
			print "Total Time for Model = ", end_time - start_time 
			print "Test Node Size = ", node_number_list[test_node_index]
			print "Number of Iterations = ", iterations
			print "Unit Disk Graphs"
			print ""

			iterations += 1
	
	for file_name in ergm_file_dict[node_number_list[test_node_index]]:
		test_file = file_name
		test_edge_set = ergm_samples_dict[node_number_list[test_node_index]][test_file]['edge_set']
		for i in xrange(tests_per_sample):
			seed = dt.datetime.today().second
			list_of_results.append(runsimulation(node_number_list[test_node_index], test_gamma, test_scaling_factor,
												test_edge_set, test_periods, test_file, seed)[1])
			
			list_of_results[iterations].ReportResults()
			end_time = time.clock()
			
			print "Total Time for Model = ", end_time - start_time 
			print "Test Node Size = ", node_number_list[test_node_index]
			print "Number of Iterations = ", iterations
			iterations += 1
	test_node_index += 1




