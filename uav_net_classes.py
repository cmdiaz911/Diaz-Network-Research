# -*- coding: utf-8 -*-
"""
Created on Tue May 17 17:37:24 2016

@author: Chris
"""

import networkx as nx
import numpy as np
import math
import random

# This class is going to keep track of the entire graph, it will inherit the methods and variables from networkx

class UAVnet(nx.Graph):
	
	def __init__(self):
		self.edge_objs = []
		self.node_objs = []
		self.is_markov_graph = False
		self.Markov_Probabilities = {}
		self.current_period = 0
		self.total_possible_edge_list = []
		self.bid_list = []
		self.decision_list = []
		super(UAVnet, self).__init__()
		
# This method will add uav objects to the list of uavs,
# It will also add uavs to the list of uavs
	def CreateUAV(self, xuav_obj):
		self.add_node(xuav_obj.label)
		self.node_objs.append(xuav_obj)
	
	# This method will set up the matrix used to create a markov matrix, this markov matrix will be used
	# To find the probabilities of messages reaching other nodes in the system
	# converts the array of arrays to a numpy matrix? 
	def create_MC_matrix(self):
		pass
	
	# this method adds the auxilary nodes to the markov graph, dependent on a source and target node
	def AddAuxNode(self, xsource_node, xtarget_node):
		pass

	# this method will solve the markov matrix for any set of target and source nodes
	# it will also pass the results to the uav objects in the list of objects 
	def Update_MC_Matrix(self, xsource_node, xtarget_node):
		if self.is_markov_graph:
			self.AddAuxNode(xsource_node, xtarget_node)
			pass
	# this method will iterate over all of the target and source node combinations
	# it will find the probability of messages reaching each pair in the simulation 
	# it passes these probabilities to the dictionary, and then passes that information to the uavs
	def SolveUAVProbs(self):
		for source_uav in self.node_objs:
			for target_uav in self.node_objs:
				pass
	
	# this metgod will take bids from the uavs and communicate to the node being asked to connect to
	# the uav being asked will decide who gets the tie, based on the information passed to it.
	def CommunicateBids(self):
		for bid in self.bid_list:
			pass
	
	# once all the decisions meet the correct criteria, and all changes are valid the graph will have to be modified
	# this method will make sure that the changes in the decision list are made
	def ModifyGraph(self):
		for decision in self.decision_list:
			pass
	
	# this method will run the simulation based on the number of periods and number of messages to be passed
	def Simulate_Network_Modification(self, xtotal_number_of_periods, xmessages_per_period):
		while self.current_period <= xtotal_number_of_periods:
			pass
			self.current_period += 1
			

############################ UAV CLASS ##############################################################
"""
Class Variables:

Name - the name of the UAV (node) (int)
Potential Edges - list of edges that are possible to this node, given the current instance of simulation (list of ints)
Outgoing Ties - list of uavs that are connected in outward ties (list)
Incoming Ties - list of uavs that are connected in inward ties (list)

Alpha - the probability of a message being lost (float) (instance variable?)
P - The weight of a uav's preference between outgoing neighbors preferences and their own (float)(instance variable)
Cost - the cost per tie (member variable)

Beta_own, Beta_Neighbors, Beta_overall - the lists and dictionary of lists that keeps track of a nodes prefrences, and those of the outward ties
(list, dictionary of lists, list)

Number_of_Messages_from_Neighbors - a dictionary of lists, will keep track of the amount of messages received from each source node, through a neighbor node
( dictionary of lists)
Number_of_Messages_total - a list of all the messages received from every source node include itself (list)

Objective_Value - the current "happiness level" based on the total number of received messages and the beta values
Addition_estimates - a list of the objective equation after making any valid addition estimate, if any (list of tuples)
Subtraction_estimates - a list of the objective equation value after makign any valid subtraction of tie, if any (list of tuples )

Bid Decision - a tuple that keeps track of the randomly decided bid decision, based on the objective value of that decision (tuple)
Node Decision - the final decision the node makes after bidding is complete, and a valid decision has been made (tuple)
Modification_Track - will keep track of whether or not the node has made a modification, if there is one to be made (boolean)

list_of_messages - a list of the message objects currently at the UAV, used in the dynamic simulation only
"""

# Methods for UAVS 
class UAV(object):

	cost = 1000.0 # find a better value for this? just a place holder
	def __init__(self, xname, xpotential_edge_list):
		self.name = xname
		self.potential_edges = xpotential_edge_list
		self.alpha = .2 # placeholder, might need to be changed
		self.P = .5 # placeholder, might need to be changed
		self.outgoing_ties = [] 
		self.incoming_ties = [] 
		self.message_list_neighbors = {}
		self.message_list_total = []
		self.Beta_own = []
		self.Beta_Overall = []
		self.Beta_neighbors = {}
		self.addition_estimates = []
		self.subtraction_estimates = []
		self.Bid_Decision = None
		self.Node_Decision = None
		self.modification_track = False
		self.max_outward_ties = False
		self.objective_value = -100000000000.000 # just a placeholder, will be changed tp reflect something else 
		self.too_isolated = False
		self.list_of_messages = [] # this is a list of message objects currently at the node
		self.message_labels = [] # a list of message labels that have been saved at the node, help keep track of whether or not the message has been seen at the node or not
	
	# this method will be used to update the variable potential edge_lists 
	def UpdateEdges(self, xuavnetwork): #might not need any argument? 
		for edge in xuavnetwork.potential_edges:
			if edge not in self.potential_edges:
				self.potential_edges.append(edge)
		pass # this needs to be edited, look at the logic and finalize it before moving on tomorrow
	
	# this method will update all of the attributes of the uav
	def UpdateAttributes(self):
		pass
	
	# this method will update the beta overall values as well as the beta neighbors attributes 
	def UpdateBetaAttributes(self):
		pass
	
	# this method will calculate the current objective value after a round of message passing 
	def CalculateObjective(self):
		pass
	
	# this method will choose the next node for the message object to be passed on to (for dynamic simulation)
	def pass_message(self):
		for message in self.list_of_messages:
			pass
		
	# this method will update the list of estimates for adding a valid node to the incoming ties
	def EstimateAdditions(self):
		for uav in self.potential_edges:
			pass
	
	
	# this method will update the list of estimates for subtraction a valid node from the current incoming ties
	def EstimateSubtraction(self):
		for uav in self.incoming_ties:
			pass
		
	# this method will create the random bid choice, 
	def DecideBid(self):
		for decision in self.decision_list:
			pass
	
	# this method will pass the final decision of the uav
	
	def FinalDecision(self):
		pass

####################################### ClASS EDGES #########################################################

""" 
Instance Variables:

label - will keep track of the label of the source node and targert node (tuple)
source_UAV - the uav object of the source uav (UAV object)
target_UAV - the uave object of the target uav (UAV object)
is_selected - will keep track of whether or not the current edge is being used (Boolean)
is_possible - will keep track of whether or not the edge is even possible in this instance of the simulation
probability - the probability that a message will be sent through that edge (not sure if needed) (float)? 
message_list - a list of the messages that are currently parked at this edge? Not sure if needed again (list)

"""

class UAVedges(object):
	
	def __init__(self, xlabel, xis_possible):
		self.label = xlabel
		self.is_possible = xis_possible
		self.is_selected = False
		self.message_list = [] 
		self.probability = 1.00 # placeholder, figure out a better way to define this 
	
	# this method will add the edge to the list of possible edges in both the UAV, and the UAV network 
	# this method will also turn on the appropriate attributes 
	def addEdge(self):
		self.is_possible = True
		self.is_selected = True
		pass
	
	# This method will be used to check whether or not the edge is possible
	def checkPossible(self):
		return self.is_possible
	
	# this method will be used to check whether or not the edge is selected: 
	def checkSelected(self):
		return self.is_selected
	
	# this message will take the input from the source nodes to decide and update the probability 
	
	def UpdateProbability(self):
		pass
		
	# this method will take a message as an argument and add it to the message lists? Not sure why or if needed
	def AddMessagetoEdge(self, xmessage):
		self.message_list.append(xmessage)
	

##################################### MESSAGE CLASS ##############################################

"""
Instance Variables 

Source_Node - the node that is sending the message first ( int or obj)
Last_Node - the last node that the message has visited (int or obj)
current_node - the currentn node that the message resides at (int or obj)
is_dead - whether or not the message has been killed in the current round of simulation (Boolean)
message_label - the name of the message, used to ensure that a message is not read twice by the same node (string )

"""

class Message(object):
	
	def __init__(self, xsource_node,xlabel,xlast_node = None):
		self.source_node = xsource_node
		self.current_node = xsource_node
		self.last_node = xlast_node
		self.label = xlabel
		self.is_dead = False

	# This message will tell the node to send the message based on the probability from the edge?
	def SendMessage(self):
		pass
	
	# This method will be run before sending a message to see if the message has died on this turn
	def CheckifDead(self):
		return self.is_dead
	
	# this method will tell the new node selected to update the message cournt and save the message label to the list of labesl 
	def UpdateNewUAV(self, xnew_uav):
		pass
	
	# this method will tell the message to return to the source node
	def ReturnToSender(self):
		self.current_node = self.source_node
		self.last_node = None
		self.is_dead = False

	


test_uav_network = UAVnet()
test_uav_network.add_nodes_from([x for x in range(15)])
test_2_uav_network = test_uav_network.copy()
test_2_uav_network.is_markov_graph = True
print test_2_uav_network.nodes()
print test_2_uav_network.is_markov_graph
print test_uav_network.is_markov_graph
