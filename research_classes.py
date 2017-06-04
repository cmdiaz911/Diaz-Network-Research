# -*- coding: utf-8 -*-
"""
Created on Tue May 17 17:30:10 2016

@author: Chris
"""

“””
Class UAVnet: Will be an object of type Graph, will inherit the methods and variables of the networkx class Graph. This class will be used to add instance variables and methods to the Graph object that will be necessary to complete the simulation. 

UAVnet Variables:
Edges – a list of edge objects that keeps track of the currently connected edges in the graph (list) (should be inherited from networkx Graph)
Nodes – list of node objects that keep track of the nodes in the graph
UAVs – a list of UAV objects, any node that is active in Nodes must generate a similar UAV object (list)
Total Possible Edge List – the set of all possible edges in this instance of the testbed, will be used to generate potential edge lists for the uavs (list of tuples)
Is_markov_graph – a variable that checks to make sure whether or not the graph object in question is the actual network, or just a copy (boolean) 
Markov_probabilities – a list of dictionaries that will be used to save the probabilities of each of the nodes, there will be 2, one that keeps track of the probability of any messages, and then one that keeps a dictionary of how many come from each incoming neighbor (list of 2 dictionaries)
Current_period – the current period of the simulation (int)
“””
#Methods for UAVnet:

#The constructor method, will initialize the graphs attributes, and set certain things to Null
#ARGUMENTS: Total Possible Edge List, Edges set to None, Nodes
#RETURNS: VOID
__init__(self, xnodes, xtotal_possible_edge_list, xEdges = None, xUAVs = None, xcurrent_period = 0)

#The methods for adding nodes and adding edges should be inherited from the Graph object in #networkx 
#The method for creating the UAV objects will be used to take all the nodes, and instantiate them as #objects. 
#ARGUMENTS: None
#RETURNS: VOID
CreateUAV (self) 

#This method will be used to duplicate the graph, it will allow the markov chain solver to solve for the #message transfer probabilities between any two pairs of nodes. Will also set up the markov dictionaries #needed, and set is markov graph to 1 for the copy.  
#ARGUMENTS: None
#RETURNS: VOID
CreateMarkovDuplicate(self) 




#This method will create and add auxiliary nodes to the markov chain that is used to solve the message #passing probabilities
#ARGUMENTS: source node, target node
#Returns: VOID
AddAuxNode(self, xsource_node, xtarget_node) 

#This method will solve the markov matrix for any set of target and source UAV nodes. And will pass the #results to the UAV and edge objects for the probabilities of messages reaching each other.
#ARGUMENTS: Source node, target node
#RETURNS: VOID
CreateMCMatrix(self, xsource_node, xtarget_node)


#This method will be used to iterate and solve the UAV message passing probabilities over the entire #graph. Basically it will be called to iteratively run the Markov Matrix Creator, and will give the Node #objects the probabilities that they need. 
#ARGUMENTS: None
#RETURNS: Void
SolveUAVProbs(self)

#The following methods might change if I decide to go the route snijders does when making decisions. #Or changing the way the periods run, instead of doing it in phases, combining phases and making it #more dynamic. 

#This method will take bids from the UAVs, (when adding ties), and communicate to the node being #asked to connect, who each connection is, and an estimate of their added objective after a new node is #added. The UAV being asked to add the tie will decide who gets the tie, and will add as many as they #can. 
#ARGUMENTS – The list of bids from each node that decides to add a tie
#RETURNS – VOID
BidComm (self, xbidlist)

#Once all decisions have met the criteria, that is, all nodes have decided on their choice of modification #if any, and all the bids have been decided, the next method will use networkx methods to modify the #graph according to the decisions that have been made by each of the nodes, these decisions all have #been checked for feasibility in the graph. 
#ARGUMENTS – a list of lists, the first element is the deciding node, the second element is the neighbor #that the node wants to modify their tie with, and the third element will be whether the decision is to #add or delete the tie. If the second element is 0, the node is deciding to do nothing. 
#RETURNS: VOID
GraphModifier(self, xdecision_list)

#The last method really needed for the UAVnet class is one that moves the simulation into the next #period, and passes to a few functions that the UAVs will need to update any variables necessary before #starting the next round of the simulation. 
#ARGUMENTS: None
#RETURNS: VOID
NextPeriod(self)
“””
The second class that I will need is probably the trickiest, as the amount of parameters and data that these objects needs to hold is substantial. There a quite a few lists and dictionaries of lists, as well as instance variables. The most complex challenge of this simulation, will be making sure the logic flow is organized, and that the methods do not get too bulky, as well as making sure that the correct attributes or instance variables, will be updated and changed, in a way that will not cause destruction of the graph, or create infinite while loops. 
“””
#UAV Class Variables
“””
Name – the name of the node (int or string)
Potential_edges – a list that keeps track of all of the other UAVs that are still within the allotted distance (distance is approximated for in the total_potential_edge_list, no actual coordinates need to be saved for this to work, if an edge is in the graphs possible edge list, then the pair of nodes is close enough to connect).  (list)
Outgoing_ties – a list of the current outward ties of the node (list)
Incoming-ties – a list of the current incoming ties of the node (list)
Alpha – the probability of a message being lost (float)
P – the weight of a nodes own preferences for incoming messages (float)
Cost – the cost per tie, only applies to incoming ties  
Beta own, Beta Neighbors, Beta Overall – 3 different lists, own represents the nodes preferences from messages of each other neighbor, Neighbors represents the outgoing ties preferences for messages from other neighbors, overall is the weighted sum (2 lists, 1 dictionary of lists (neighbors))
Number_of_messages_from_neighbors – a dictionary of lists, will keep track of the amount of messages received from each source node, through each incoming neighbor. (dictionary of lists)
Number_of_messages_total – a list, keeps track of the total number of messages received from every source node, including itself. 
Objective Value – the current objective value of the node, based on the current number of messages and beta values during this period of the simulation. 
Addition_estimates – Will keep track of the value of the estimate for adding each node in the potential edge list (a list of tuples)
Subtraction_estimates – Will keep track of the value of the estimate for subtracting each node that is currently in the list of incoming neighbors (a list of tuples)
Bid_decision – will give the decision of what outgoing tie will be selected. (int or string)
Node_decision – will be the two lists of addition and subtraction estimates, combined, with an added parameter that keeps track of which estimate is addition, and which is subtraction, this list will be sorted by the highest estimate to the lowest estimate. Each node will have a decision list, if the decision becomes infeasible, the decision will be removed, and the next decision will be tried.
Modification_track – will keep track of whether or not the node has made a modification, if there is one to be made, will be used as stopping criteria to go to the next period (binary) 
Restriction attributes – There might be a few of these added, they will be instance variables that will be binary, basically if there are too many outgoing ties or not enough incoming ties from a node, it will have some of these turned on. (Boolean)
“””
#Methods UAVS

#The constructor method will initialize most of the variables, some of the lists will be constructed on #their own however, as we need to makes sure the lists are each separate objects, and not pointers to #the same dictionary or lists.
#ARGUMENTS: Name of the node, potential_edge_list of the node, Beta lists, message_lists, #message_estimates, outgoing_ties, incoming_ties, node_decisions, . All other variables will be #initialized in the constructor.
#RETURNS: VOID
__init__(self, xname, xpotential_edge_list, xBeta_own, xBeta_neighbors, xBeta_overall, xmessage_list_neighbors, xmessage_list_total, xaddition_estimates, xsubtraction_estimates, xoutgoing_ties, xincoming_ties, xnode_decision,  xcost = 100.0, xalpha = .2, xp = .5, xobjective_value = 100000000.0, xmodification_track = 0, xrestriction_attributes = 0)

#This Method will be used to update the variables for the potential edge_lists, outgoing_ties, and #incoming_ties. Will be passed from the  graph modifier method. 
#ARGUMENTS: edge_list of UAV graph
#RETURNS: VOID
UpdateEdges(self, xedgelist)

#This Method will be used to update the message counts after each round of message passing, this will #also update the beta_own, beta_neighbors, and Beta_overall lists. 
#ARUGMENTS: The markov dictionaries with the updated probabilities
#RETURNS: VOID
UpdateMessages(self, xmarkov_probability_dict)

#This method will calculate the current objective value for each node. Will be done after updating all of #the betas and message counts.
#ARGUMENTS: None
#RETURNS: VOID
UpdateObjective(self)

#This Method will update the addition estimate list for the uav, 
#ARGUMENTS: None
#RETURNS: Void
EstimateAddition(self)

#This Method will update the subtraction estimate lists for the UAV,
#ARUGMENTS: None 
#RETURNS: VOID
EstimateSubtraction(self)

#This method will take both of the estimate lists and combine them. And then send the decision lists to #the UAVgraph, which simulates them just communicating with each other, this will just keep things #organized
#ARGUMENTS: None
#RETURNS: A list of the node decisions to the UAV Graph 
CreateDecisionList(self)

#This method will take the bids from the UAVgraph, and decide return to the graph who gets the tie
#ARGUMENTS: List of nodes with their estimated objective improvement 
#RETURNS: The tuple of the edge that will be modified. 
DecideBids(self, xbidlist)

#This class will be used to keep track of the current possible edges and selected edges of the network. It #will also keep track of the probability that a message is going to be lost in that edge? Maybe will keep #track of the probability of having a message sent through it, for the simulation, not the markov chain

#Class Edges
# Instance Variables:
# label: will keep track of the index of the from and the to node (Tuple)
# Is_Selected: Will keep track of whether or not the current edge is being used (Boolean)
# is_Possible: Will keep track of whether or not the edge in question is a part of the possible edge list #(Boolean)
#Probability: The probability that a message will be sent through the edge, (float)
#Message_list?: A list of the messages that are currently parked at this edge? OR is this a list of the #messages that have came through this edge? Not sure (List) Might not be needed 

# This method will initialize the edge class
# Arguments: Whether or not the edge is possible, the probability will be initialized to 0, and is selected #will be also initiliazed to 0, the label will be an argument 
# Returns: Void
__init__(self, xlabel , xIsPossible, xprobability = 0.0, xisselected = False)

# This method will be used to check whether or not the edge is possible
# Arguments: None
# Returns: Boolean
CheckPossible(self)

#This method will be used to check whether or not the edge is currently selected
# Arguments: None 
# Returns: Boolean
CheckSelected(self)

# This method will take the input of he number of outgoing ties of the from node, this will update the #probability of the edge being used in the simulation to pass the message on
# Arguments: Number of outgoing ties of the from node
# Returns: VOID
UpdateProbability (self, xnumberofoutgoing)

#This method will take a message as an argument, and possibly add it to the message lists? This could #also be used to track the messages that have already came through, and tell the node to not count it #twice?
# Arguments: A message object
# Returns: VOID
AddMessageEdge(self, xmessage)


#This class will be used to keep track of messages during simulation, this will tell the UAVs and Edges to #update their lists to make sure they record the messages that pass through the node the first time it #has been sent. Not sure whether or not to send the message back to the first node, or delete it, #whatever saves the most amount of memory.

#The Message Class
#Instance Variables 

# Source Node: The node that is sending the message (int)
# Last_Node: The last place the node has been (int)
# Current_Node: The current node that the message resides at (int)
# Is_dead: Whether or not the message has been killed in the current round of simulation (Boolean)
# Message_Label: The name of the message, used to ensure that a message is not read twice by the #same node (string?)

#Message Methods:

#This method will initialize the message
#Arguments: The label, the starting node, the current node, and the last node are all initialized and is #dead is initialized to false
#Returns: Void
__init__(self, xlabel, xsource_node, xcurrent_node, xlast_node = None, xis_dead = False)

#This method will tell the node to send the message based on the probability from the edge? 
#Arguments: None
#Returns: Void
SendMessage(self)

#This argument will be run before send message to see if the message has died on this turn
#Arguments: None
#Returns: Void
CheckifDead(self)

#This Argument will tell the new node selected to update the message count, and save the message #label to the list of labels of messages that have been sent to it in the current round
#Arguments: None
#Returns: VOID
UpdateNewUAV(self)

#This argument will tell the message to return to its source node and update the other values of the #message to ensure the simulation will run again with the same starting parameters:
#Arguments: None
#Returns: Void
ReturnToSender(self)



