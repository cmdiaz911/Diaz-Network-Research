import cPickle as pickle
import DDIP_Model_Classes

file = open("10_node_model_results.pkl", 'rb')
results_objects = pickle.load(file)
for result in results_objects :
	print("Graph Name: " + result.graph_name)
	print("Edge Efficiency: " + str(result.edge_efficiency))
	print("Edge Ratio: " + str(result.ratio_of_edges))
	print("Average Distance: " + str(result.average_distance))
	print("Fully Connected Distance: " + str(result.fully_connected_graph_distance))
	print("Inverse Distance: " + str(result.average_inverse_distance))
	print("Fully Connected Inverse Distance: " + str(result.fully_connected_inverse_distance))
	print("")
	print("Edges Used: " + str(result.final_edge_list))
	print("Possible Edges: " + str(result.possible_edge_list))
	print("")
	print("")

