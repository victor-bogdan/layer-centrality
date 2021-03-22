from pandas import DataFrame
from utils.data_helper import get_node_connections_on_layers


def get_node_degree_centrality_analysis(
        layers_dict,
        nodes_layer_centrality_dict,
        node
):
    """

    :param layers_dict: Dictionary containing networkx layers
    :param nodes_layer_centrality_dict: Dictionary of dictionaries containing the centrality of
    each layer for a set of nodes.
    :param node: String representing a node.
    :return:
    """

    node_layer_centrality_analysis_dict = {}

    node_layer_connections_dict = get_node_connections_on_layers(layers_dict, node)

    # Init analysis dicts
    for layer_key in node_layer_connections_dict.keys():

        temp_layer_data_dict = {
            'Total number of connections': len(node_layer_connections_dict[layer_key]),
            'Layer Centrality': nodes_layer_centrality_dict[node][layer_key],
        }

        for index in range(len(node_layer_connections_dict.keys())):
            temp_layer_data_dict['Number of nodes of order {0}'.format(index + 1)] = 0
            temp_layer_data_dict['Nodes of order {0}'.format(index + 1)] = []

        node_layer_centrality_analysis_dict[layer_key] = temp_layer_data_dict

    # Get all unique connected nodes
    connected_nodes_set = set.union(*[a for a in node_layer_connections_dict.values()])

    # For each connected node, get the layers on which it is present
    node_layers_dict = {}

    for connected_node in connected_nodes_set:

        temp_node_layer_dict = {
            'layers': []
        }

        for layer_key in node_layer_connections_dict:
            if connected_node in node_layer_connections_dict[layer_key]:
                temp_node_layer_dict['layers'].append(layer_key)

        node_layers_dict[connected_node] = temp_node_layer_dict

    # Compute for each layer how many nodes of each order it contains
    for node_key in node_layers_dict:
        number_of_layers = len(node_layers_dict[node_key]['layers'])

        for layer_name in node_layers_dict[node_key]['layers']:
            node_layer_centrality_analysis_dict[layer_name][
                'Number of nodes of order {0}'.format(number_of_layers)] += 1
            node_layer_centrality_analysis_dict[layer_name][
                'Nodes of order {0}'.format(number_of_layers)].append(node_key)

    '''
    # Compute unique node connections per layer
    for layer_key in node_layer_connections_dict.keys():

        temp_layer_connections_dict = node_layer_connections_dict.copy()
        temp_layer_connections_dict.pop(layer_key)  # exclude current layer
        temp_set = set.union(*[a for a in temp_layer_connections_dict.values()])

        # print(len(set.union(node_layer_centrality_analysis_dict[layer_key], temp_set)))

        temp_layer_data_dict = {
            'Total number of connections': len(node_layer_connections_dict[layer_key]),
            'Layer Centrality': nodes_layer_centrality_dict[node][layer_key],
            'Number of unique node connections': len(node_layer_connections_dict[layer_key] - temp_set),
            'Unique node connections': node_layer_connections_dict[layer_key] - temp_set
        }

        node_layer_centrality_analysis_dict[layer_key] = temp_layer_data_dict
    '''

    analysis_results_data_frame = DataFrame.from_dict(node_layer_centrality_analysis_dict).T.sort_index(axis=0)
    analysis_results_data_frame.columns.name = "Node " + node

    # print(results_data_frame)

    return analysis_results_data_frame
