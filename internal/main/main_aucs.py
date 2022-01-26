from os.path import dirname
from uunet.multinet import data
from utils.data_helpers import draw_layers, get_layer_total_number_of_nodes, get_layer_total_number_of_edges, \
    get_layer_most_connected_node, get_layer_number_of_isolated_nodes

DATASET_NAME = "aucs"

multilayered_network = data(DATASET_NAME)

# draw_layers("aucs", multilayered_network, "{0}/internal/results".format(dirname(dirname(__file__))))
print(get_layer_total_number_of_nodes(multilayered_network))
print(get_layer_total_number_of_edges(multilayered_network))
print(get_layer_most_connected_node(multilayered_network))
print(get_layer_number_of_isolated_nodes(multilayered_network))