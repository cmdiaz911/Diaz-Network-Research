# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 10:35:43 2017

@author: cmdiaz93
"""

import networkx as nx
import math
import matplotlib.pyplot as plt 

unconnected_graph_list = []

node_sizes = [10,15,20]
unit_disk_results = {}
for size in node_sizes:
	unit_disk_results[size]={}
	unit_disk_results[size]['avg_dist'] = []
	unit_disk_results[size]['fully_con_dist'] = []
	unit_disk_results[size]['possible_edge'] = []
	unit_disk_results[size]['percent_edges'] = []
	unit_disk_results[size]['number_of_ties'] = [] 
	unit_disk_results[size]['inverse dist'] = []
	unit_disk_results[size]['con inversed dist'] = [] 
	unit_disk_results[size]['connect edge eff'] = []
	unit_disk_results[size]['edge eff '] = []

ergm_results = {}
for size in node_sizes:
	ergm_results[size]={}
	ergm_results[size]['avg_dist'] = []
	ergm_results[size]['possible_edge'] = []
	ergm_results[size]['fully_con_dist'] = []
	ergm_results[size]['percent_edges'] = []
	ergm_results[size]['number_of_ties'] = [] 
	ergm_results[size]['inverse dist'] = [] 
	ergm_results[size]['con inversed dist'] = [] 
	ergm_results[size]['connect edge eff'] = []
	ergm_results[size]['edge eff '] = []



for size in node_sizes:
	fin = open("%s_node_newest_model_results_analysis.txt" % (size),'r')
	output_lines = fin.readlines()
	fin.close()
	for i in range(len(output_lines)):
		if output_lines[i][0:6] == 'Sample':
			
			model_dist = output_lines[i-9].split()
			try:
				a_dist = float(model_dist[-1])
			except ValueError:
				
				if output_lines[i][-3] == 'x':
					unconnected_graph_list.append([size,'ergm',output_lines[i]])
				else:
					unconnected_graph_list.append([size,'unit',output_lines[i]])
				continue
			edges = output_lines[i-14].split()
			#print edges
			#3print edges
			e_used = int(edges[-1])
			#print e_used
			#print e_used
			percent = output_lines[i-5].split()
			p_used = float(percent[-1])
			fully_dist = output_lines[i-8].split()
			f_dist = float(fully_dist[-1])
			
			pos_edges = output_lines[i-17].split()
			
			t_edges = int(pos_edges[-1])
			#print t_edges
			#print t_edges
			#print output_lines[i][-3]
			inv_dist = output_lines[i-7].split()
			i_dist = float(inv_dist[-1])
			
			connected_inv = output_lines[i - 6].split()
			con_inv = float(connected_inv[-1])
			
			connected_eff = output_lines[i-2].split()
			eta_con = float(connected_eff[-1])
			
			final_eff = output_lines[i-3].split()
			eta_final = float(final_eff[-1])

			if output_lines[i][-3] == 'x':
				
				ergm_results[size]['avg_dist'].append(a_dist)
				#print t_edges
				#print ergm_results[size]['possible_edge']
				#print t_edges
				ergm_results[size]['possible_edge'].append(t_edges)
				#print ergm_results[size]['possible_edge']
				#print ""
				ergm_results[size]['fully_con_dist'].append(f_dist)
				ergm_results[size]['percent_edges'].append(p_used)
				ergm_results[size]['number_of_ties'].append(e_used)
				ergm_results[size]['inverse dist'].append(i_dist)
				ergm_results[size]['connect edge eff'].append(eta_con)
				ergm_results[size]['edge eff '].append(eta_final)
				ergm_results[size]['con inversed dist'].append(con_inv)
			else:
				unit_disk_results[size]['avg_dist'].append(a_dist)
				unit_disk_results[size]['possible_edge'].append(t_edges)
				unit_disk_results[size]['fully_con_dist'].append(f_dist)
				unit_disk_results[size]['percent_edges'].append(p_used)
				unit_disk_results[size]['number_of_ties'].append(e_used)
				unit_disk_results[size]['inverse dist'].append(i_dist)
				unit_disk_results[size]['con inversed dist'].append(con_inv)
				unit_disk_results[size]['connect edge eff'].append(eta_con)
				unit_disk_results[size]['edge eff '].append(eta_final)
"""
finished_pc_sizes = [10,15, 20,25,30,40]

for size in finished_pc_sizes:
	fin = open("%s_node_results_ergm/%s_node_results_lists_final_pc.txt" % (size,size),'r')
	output_lines = fin.readlines()
	for i in range(len(output_lines)):
		if output_lines[i][0:6] == 'Sample':
			model_dist = output_lines[i-6].split()
			try:
				a_dist = float(model_dist[-1])
			except ValueError:
				
				#print output_lines[i][-4]
				if output_lines[i][-4] == 'x':
					unconnected_graph_list.append([size,'ergm',output_lines[i]])
				else:
					unconnected_graph_list.append([size,'unit',output_lines[i]])
				continue
			edges = output_lines[i-11].split()
			e_used = int(edges[-1])
			percent = output_lines[i-2].split()
			p_used = float(percent[-1])
			fully_dist = output_lines[i-5].split()
			#print fully_dist
			f_dist = float(fully_dist[-1])
			pos_edges = output_lines[i - 14].split()
			#print pos_edges
			
			t_edges = int(pos_edges[-1])
			#print output_lines[i][-4]
			inv_dist = output_lines[i-4].split()
			i_dist = float(inv_dist[-1])
			
			connected_inv = output_lines[i - 3].split()
			con_inv = float(connected_inv[-1])
			if output_lines[i][-4] == 'x':
				
				ergm_results[size]['avg_dist'].append(a_dist)
				ergm_results[size]['possible_edge'].append(t_edges)
				ergm_results[size]['fully_con_dist'].append(f_dist)
				ergm_results[size]['percent_edges'].append(p_used)
				ergm_results[size]['number_of_ties'].append(e_used)
				ergm_results[size]['inverse dist'].append(i_dist)
				ergm_results[size]['con inversed dist'].append(con_inv)
			else:
				unit_disk_results[size]['avg_dist'].append(a_dist)
				unit_disk_results[size]['possible_edge'].append(t_edges)
				unit_disk_results[size]['fully_con_dist'].append(f_dist)
				unit_disk_results[size]['percent_edges'].append(p_used)
				unit_disk_results[size]['number_of_ties'].append(e_used)
				unit_disk_results[size]['inverse dist'].append(i_dist)
				unit_disk_results[size]['con inversed dist'].append(con_inv)
	fin.close()
"""
for size in node_sizes:
	unit_disk_results[size]['total ave dist'] = sum(unit_disk_results[size]['avg_dist'])/len(unit_disk_results[size]['avg_dist'])
	unit_disk_results[size]['avg con dist'] = sum(unit_disk_results[size]['fully_con_dist'])/len(unit_disk_results[size]['fully_con_dist'])
	unit_disk_results[size]['avg possible edge numbers'] = sum(unit_disk_results[size]['possible_edge'])/float(len(unit_disk_results[size]['possible_edge']))
	unit_disk_results[size]['average percent'] = sum(unit_disk_results[size]['percent_edges'])/len(unit_disk_results[size]['percent_edges'])
	unit_disk_results[size]['average ties used'] = sum(unit_disk_results[size]['number_of_ties'])/float(len(unit_disk_results[size]['number_of_ties']))
	unit_disk_results[size]['average inverse dist'] = sum(unit_disk_results[size]['inverse dist'])/float(len(unit_disk_results[size]['inverse dist']))
	unit_disk_results[size]['average con inverse dist'] = sum(unit_disk_results[size]['con inversed dist'])/float(len(unit_disk_results[size]['con inversed dist']))
	unit_disk_results[size]['average edge eff '] =sum(unit_disk_results[size]['edge eff '])/float(len(unit_disk_results[size]['edge eff ']))
	unit_disk_results[size]['ave connect edge eff'] = sum(unit_disk_results[size]['connect edge eff'])/float(len(unit_disk_results[size]['connect edge eff']))
for size in node_sizes:

	ergm_results[size]['total ave dist'] = sum(ergm_results[size]['avg_dist'])/len(ergm_results[size]['avg_dist'])
	ergm_results[size]['avg con dist'] = sum(ergm_results[size]['fully_con_dist'])/len(ergm_results[size]['fully_con_dist'])
	ergm_results[size]['avg possible edge numbers'] = sum(ergm_results[size]['possible_edge'])/float(len(ergm_results[size]['possible_edge']))
	ergm_results[size]['average percent'] = sum(ergm_results[size]['percent_edges'])/len(ergm_results[size]['percent_edges'])
	ergm_results[size]['average ties used'] = sum(ergm_results[size]['number_of_ties'])/float(len(ergm_results[size]['number_of_ties']))
	ergm_results[size]['average inverse dist'] = sum(ergm_results[size]['inverse dist'])/float(len(ergm_results[size]['inverse dist']))
	ergm_results[size]['average con inverse dist'] = sum(ergm_results[size]['con inversed dist'])/float(len(ergm_results[size]['con inversed dist']))
	ergm_results[size]['average edge eff '] =sum(ergm_results[size]['edge eff '])/float(len(ergm_results[size]['edge eff ']))
	#ergm_results[size]['connect edge eff'] = ergm_results[size]['average con inverse dist']/float(1)
	ergm_results[size]['ave connect edge eff'] = sum(ergm_results[size]['connect edge eff'])/float(len(ergm_results[size]['connect edge eff']))


#inverse_dist_40 = 1/unit_disk_results[40]['total ave dist']
#unit_disk_results[40]['average edge eff '] = unit_disk_results[40]['average percent']/inverse_dist_40
for size in node_sizes:
	count_bad = 0
	fout = open("%s_results_summary.txt" % size, 'w')
	fout.write("Number of Unit Disk Graphs Sampled: " + str(len(unit_disk_results[size]['avg_dist'])) +"\n")
	for unconnected_sample in unconnected_graph_list:
		if unconnected_sample[0] == size and unconnected_sample[1] == 'unit':
			count_bad += 1 
	fout.write("Number of Unit Disk Unconnected Samples = " + str(count_bad) + "\n")
	fout.write("Unit Disk Average Distance = " + str(unit_disk_results[size]['total ave dist']) + "\n")
	fout.write("Unit Disk Average Fully Connected Distance = " + str(unit_disk_results[size]['avg con dist']) + "\n")
	fout.write("Unit Disk Average Possible Edge Numbers = " + str(unit_disk_results[size]['avg possible edge numbers']) + "\n")
	fout.write("Unit Disk Average Ties Used = "+ str(unit_disk_results[size]['average ties used']) + "\n")
	fout.write("Unit Disk Average Percent Ties Used = " + str(unit_disk_results[size]['average percent']) + "\n")
	fout.write("Unit Disk Average Edge Distance Efficiency = " + str(unit_disk_results[size]['average edge eff '])+ "\n")
	fout.write("Unit Disk Average Connected Edge Distance Efficiency = " + str(unit_disk_results[size]['ave connect edge eff']) +"\n")
	fout.write("Unit Disk Average Inverse Distance = " + str(unit_disk_results[size]['average inverse dist']) + "\n")
	fout.write("Unit Disk Average Fully Connected Inverse Distance = " + str(unit_disk_results[size]['average con inverse dist'])+ "\n")
	fout.write("\n")
	fout.close()


for size in node_sizes:

	count_bad = 0
	fout = open("%s_results_summary.txt" % size, 'a')
	fout.write("Number of ERGM Graphs Sampled: " + str(len(ergm_results[size]['avg_dist']))+ "\n")
	for unconnected_sample in unconnected_graph_list:
		if unconnected_sample[0] == size and unconnected_sample[1] == 'ergm':
			count_bad += 1 
	fout.write("Number of ERGM Unconnected Samples = " + str(count_bad) + "\n")		
	fout.write("ERGM Average Distance = " + str(ergm_results[size]['total ave dist']) + "\n")
	fout.write("ERGM Average Fully Connected Distance = " + str(ergm_results[size]['avg con dist']) + "\n")
	fout.write("ERGM Average Possible Edge Numbers = " + str(ergm_results[size]['avg possible edge numbers']) + "\n")
	fout.write("ERGM Average Ties Used = "+ str(ergm_results[size]['average ties used']) + "\n")
	fout.write("ERGM Average Percent Ties Used = " + str(ergm_results[size]['average percent']) + "\n")
	fout.write("ERGM Average Edge Distance Efficiency = " + str(ergm_results[size]['average edge eff '])+ "\n")
	fout.write("ERGM Average Connected Edge Distance Efficiency = " + str(ergm_results[size]['ave connect edge eff']) +"\n")
	fout.write("ERGM Average Inverse Distance = "  +str(ergm_results[size]['average inverse dist']) + "\n")
	fout.write("ERGM Average Fully Connected Inverse Distance = " + str(ergm_results[size]['average con inverse dist'])+ "\n")	
	fout.write("\n")
	fout.close()


#print unconnected_graph_list

#print "" 
#print unit_disk_results[40]['average edge eff ']
#inverse_dist_40 = 1/unit_disk_results[40]['total ave dist']
#unit_disk_results[40]['aveage edge eff'] = unit_disk_results[40]['average percent']/inverse_dist_40

"""

checked_parameters = ['avg_dist','fully_con_dist','percent_edges','possible_edge','number_of_ties','inverse dist', 'con inversed dist']
node_sizes = [10,20,30]
restriction_parameters = [.1,.2,.3,.4,.5]
unit_disk_results = {}
for size in node_sizes:
	unit_disk_results[size] = {}
	for restrict in restriction_parameters:
		unit_disk_results[size][restrict] = {}
		for parameter in checked_parameters:
			unit_disk_results[size][restrict][parameter] = [] 



for size in node_sizes:
	fin = open("%s_node_restriction_analysis.txt" % size,'r')
	output_lines = fin.readlines()
	fin.close()
	for i in range(len(output_lines)):
		if output_lines[i][0:6] == 'Sample':
			
			model_dist = output_lines[i-6].split()
			try:
				a_dist = float(model_dist[-1])
			except ValueError:
				max_ties = output_lines[i-15].split()
				checked_parameter = float(max_ties[-1])/size
				unconnected_graph_list.append([size,checked_parameter,output_lines[i]])
				continue
			edges = output_lines[i-11].split()
			#print edges
			#print edges
			e_used = int(edges[-1])
			#print e_used
			#print e_used
			percent = output_lines[i-2].split()
			p_used = float(percent[-1])
			fully_dist = output_lines[i-5].split()
			f_dist = float(fully_dist[-1])
			if output_lines[i-15][0:3] == "Max":
				pos_edges = output_lines[i-13].split()
			else:
				pos_edges = output_lines[i-14].split()
			
			t_edges = int(pos_edges[-1])
			#print t_edges
			#print t_edges
			#print output_lines[i][-3]
			inv_dist = output_lines[i-4].split()
			i_dist = float(inv_dist[-1])
			
			connected_inv = output_lines[i - 3].split()
			con_inv = float(connected_inv[-1])
			max_ties = output_lines[i-15].split()
			
			checked_parameter = float(max_ties[-1])/size
			#print checked_parameter 
			
			if checked_parameter not in restriction_parameters:
				continue
				#checked_parameter =.25
				#print checked_parameter
				#print float(max_ties[-1])/size
			#print output_lines[i],i
			
			#elif 
			
			
			unit_disk_results[size][checked_parameter]['avg_dist'].append(a_dist)
			unit_disk_results[size][checked_parameter]['possible_edge'].append(t_edges)
			unit_disk_results[size][checked_parameter]['fully_con_dist'].append(f_dist)
			unit_disk_results[size][checked_parameter]['percent_edges'].append(p_used)
			unit_disk_results[size][checked_parameter]['number_of_ties'].append(e_used)
			unit_disk_results[size][checked_parameter]['inverse dist'].append(i_dist)
			unit_disk_results[size][checked_parameter]['con inversed dist'].append(con_inv)


for size in node_sizes:
	for restrict in restriction_parameters:
		unit_disk_results[size][restrict]['total ave dist'] = sum(unit_disk_results[size][restrict]['avg_dist'])/len(unit_disk_results[size][restrict]['avg_dist'])
		unit_disk_results[size][restrict]['avg con dist'] = sum(unit_disk_results[size][restrict]['fully_con_dist'])/len(unit_disk_results[size][restrict]['fully_con_dist'])
		unit_disk_results[size][restrict]['avg possible edge numbers'] = sum(unit_disk_results[size][restrict]['possible_edge'])/float(len(unit_disk_results[size][restrict]['possible_edge']))
		unit_disk_results[size][restrict]['average percent'] = sum(unit_disk_results[size][restrict]['percent_edges'])/len(unit_disk_results[size][restrict]['percent_edges'])
		unit_disk_results[size][restrict]['average ties used'] = sum(unit_disk_results[size][restrict]['number_of_ties'])/float(len(unit_disk_results[size][restrict]['number_of_ties']))
		unit_disk_results[size][restrict]['average inverse dist'] = sum(unit_disk_results[size][restrict]['inverse dist'])/float(len(unit_disk_results[size][restrict]['inverse dist']))
		unit_disk_results[size][restrict]['average con inverse dist'] = sum(unit_disk_results[size][restrict]['con inversed dist'])/float(len(unit_disk_results[size][restrict]['con inversed dist']))
		unit_disk_results[size][restrict]['average edge eff'] = 1/(unit_disk_results[size][restrict]['average inverse dist']/unit_disk_results[size][restrict]['average percent'])
		#unit_disk_results[size][restrict]['connect edge eff'] = unit_disk_results[size][restrict]['average con inverse dist']/float(1)

for size in node_sizes:
	fout = open("%s_restriction_results_summary.txt" % size, 'w')
	for restrict in restriction_parameters:
		fout.write("Max Outdegree Pameter = "+ str(restrict) + "\n")
		count_bad = 0
		fout.write("Number of Unit Disk Graphs Sampled: " + str(len(unit_disk_results[size][restrict]['avg_dist'])) +"\n")
		for unconnected_sample in unconnected_graph_list:
			if unconnected_sample[0] == size and unconnected_sample[1] == restrict:
				count_bad += 1 
		fout.write("Number of Unit Disk Unconnected Samples = " + str(count_bad) + "\n")
		fout.write("Unit Disk Average Distance = " + str(unit_disk_results[size][restrict]['total ave dist']) + "\n")
		fout.write("Unit Disk Average Fully Connected Distance = " + str(unit_disk_results[size][restrict]['avg con dist']) + "\n")
		fout.write("Unit Disk Average Possible Edge Numbers = " + str(unit_disk_results[size][restrict]['avg possible edge numbers']) + "\n")
		fout.write("Unit Disk Average Ties Used = "+ str(unit_disk_results[size][restrict]['average ties used']) + "\n")
		fout.write("Unit Disk Average Percent Ties Used = " + str(unit_disk_results[size][restrict]['average percent']) + "\n")
		fout.write("Unit Disk Average Edge Distance Efficiency = " + str(unit_disk_results[size][restrict]['average edge eff'])+ "\n")
		#fout.write("Unit Disk Average Connected Edge Distance Efficiency = " + str(unit_disk_results[size][restrict]['connect edge eff']) +"\n")
		fout.write("\n")
	fout.close()
plt.close()
for size in node_sizes:
	
	inter_list = []
	
	for restriction in restriction_parameters:
		inter_list.append(unit_disk_results[size][restriction]['total ave dist'])
	
	plt.plot([x for x in restriction_parameters],inter_list, label = "n = %s" % size)
	plt.title("Average Distance Vs Max Outdegree")
	plt.xlabel("Max Outdegree to Graph Size Ratio")
	plt.xticks([x for x in restriction_parameters])
	plt.legend()
	plt.axis([.1,.5,1.75,4])
	plt.ylabel("Average Distance")
plt.show()
plt.savefig('Average_Distance_Sensitivity.png')
plt.close()

for size in node_sizes:
	
	inter_list = []
	
	for restriction in restriction_parameters:
		inter_list.append(unit_disk_results[size][restriction]['average percent'])
	
	plt.plot([x for x in restriction_parameters],inter_list, label = "n = %s" % size)
	plt.title("Edge Ratio Vs Max Outdegree")
	plt.xlabel("Max Outdegree to Graph Size Ratio")
	plt.xticks([x for x in restriction_parameters])
	plt.legend()
	plt.axis([.1,.5,.3,1])
	plt.ylabel(" Average Ratio of Edges Used")
plt.show()
plt.savefig('Edge_Ratio_Sensitivity.png')
plt.close()

for size in node_sizes:
	
	inter_list = []
	
	for restriction in restriction_parameters:
		inter_list.append(unit_disk_results[size][restriction]['average edge eff'])
	
	plt.plot([x for x in restriction_parameters],inter_list, label = "n = %s" % size)
	plt.title("Edge Distance Efficiency Vs Max Outdegree")
	plt.xlabel("Max Outdegree to Graph Size Ratio")
	plt.xticks([x for x in restriction_parameters])
	plt.legend()
	plt.axis([.1,.5,1,3.5])
	plt.ylabel("Average Edge Distance Efficiency")
plt.show()
plt.savefig('Edge_Efficiency.png')
plt.close()

"""

"""
for size in node_sizes:
	print unit_disk_results[size]
	
	"""