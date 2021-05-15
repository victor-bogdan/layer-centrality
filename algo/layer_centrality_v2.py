from itertools import combinations, permutations
from uunet.multinet import empty, add_nx_layer, flatten, layers, to_nx_dict, read, vertices
from utils.centrality_measure_helper import get_node_centrality_dict


def create_layer_combinations_node_centrality_dict(nx_layer_dict, centrality_measure):
    """
    Creates a dictionary containing node centrality values for all layer combinations of all possible lengths.

    :param nx_layer_dict: Multilayer network layer dictionary.
    :param centrality_measure: The centrality measure which is being used.
    :return: Dictionary containing node centrality values for all layer combinations of all possible lengths
    """

    layer_combinations_node_centrality_dict = {}

    # Generate all possible layer combinations of all possible lengths
    for i in range(len(nx_layer_dict)):
        layer_combination_tuple_list = list(combinations(nx_layer_dict.keys(), i + 1))
        compute_layer_combinations_node_centrality(
            nx_layer_dict, layer_combination_tuple_list, layer_combinations_node_centrality_dict, centrality_measure)

    return layer_combinations_node_centrality_dict


def compute_layer_combinations_node_centrality(
        nx_layer_dict,
        layer_combination_tuple_list,
        layer_combinations_node_centrality_dict,
        centrality_measure
):
    """
    Computes the node centrality for each layer combination in :param layer_combination_tuple_list. Each tuple
    is sorted in lexicographic order. In order to compute the node centrality, the layer combinations are flattened
    to avoid duplicate connections.

    :param nx_layer_dict: Multilayer network layer dictionary.
    :param layer_combination_tuple_list: List of tuples containing layer combinations of same length.
    :param layer_combinations_node_centrality_dict: Dictionary reference
    :param centrality_measure: The centrality measure which is being used.
    :return: void
    """

    for layer_combination_tuple in layer_combination_tuple_list:
        layer_combinations_node_centrality_dict[''.join(sorted(list(layer_combination_tuple)))] = \
            compute_flattened_layer_combination_node_centrality(
                nx_layer_dict, layer_combination_tuple, centrality_measure)
        # print(''.join(sorted(list(layerTuple))), layerTupleDict[''.join(sorted(list(layerTuple)))])


def compute_flattened_layer_combination_node_centrality(
        nx_layer_dict,
        layer_combination_tuple,
        centrality_measure
):
    """
    Computes the centrality values for all nodes in a flattened network obtained from the combinations of
    layers.

    :param nx_layer_dict: Multilayer network layer dictionary.
    :param layer_combination_tuple: Tuple containing a combination of layers.
    :param centrality_measure: The centrality measure which is being used.
    :return: Dictionary of centrality values for all nodes in the flattened network obtained from the
             combination of layers.
    """

    temp_multilayered_network = empty()

    for layer in layer_combination_tuple:
        add_nx_layer(temp_multilayered_network, nx_layer_dict[layer], layer)

    flatten(temp_multilayered_network, "flattened_layer", layers=layers(temp_multilayered_network))

    flattened_layer = to_nx_dict(temp_multilayered_network)["flattened_layer"]
    # print(nx.degree_centrality(flattened_layer))
    # print(nx.degree(flattened_layer), "\n")

    return get_node_centrality_dict(centrality_measure, flattened_layer)


def compute_multinet_layer_centrality(nx_layer_dict, nodes, centrality_measure):
    """
    Computes the layer centrality for each node in a given multilayer network.

    :param nx_layer_dict: Multilayer network layer dictionary.
    :param nodes: List containing all nodes for which the layer centrality is computed.
    :param centrality_measure: The centrality measure which is being used.
    :return: Dictionary of dictionaries containing the centrality of each layer for each node in :param nodes.
    """

    nodes_layer_centrality_dict = {}

    for node in nodes:

        node_nx_layer_dict = {}

        node_nx_absent_layer_list = []

        for layer_name in nx_layer_dict.keys():
            if nx_layer_dict[layer_name].has_node(node):
                node_nx_layer_dict[layer_name] = nx_layer_dict[layer_name]
            else:
                node_nx_absent_layer_list.append(layer_name)

        layer_combinations_tuple_dict = \
            create_layer_combinations_node_centrality_dict(node_nx_layer_dict, centrality_measure)

        # Generate all possible layer permutations
        layer_permutations_tuple_list = list(permutations(node_nx_layer_dict.keys(), len(node_nx_layer_dict)))

        temp_nodes_layer_centrality_dict = compute_multinet_layer_centrality_for_node(
            node_nx_layer_dict, layer_combinations_tuple_dict, layer_permutations_tuple_list, node)
        #  print("Node {0}: Shapley = {1}".format(nodes, nodes_layer_centrality_dict))

        for layer in node_nx_absent_layer_list:
            temp_nodes_layer_centrality_dict[layer] = 0

        nodes_layer_centrality_dict[node] = temp_nodes_layer_centrality_dict

    return nodes_layer_centrality_dict


def compute_multinet_layer_centrality_for_node(
        nx_layer_dict,
        layer_combinations_tuple_dict,
        layer_permutations_tuple_list,
        node
):
    """
    Computes the layer centrality for a given node in a given multilayer network.

    :param nx_layer_dict: Multilayer network layer dictionary.
    :param layer_permutations_tuple_list: List of tuples containing all layer permutations.
    :param layer_combinations_tuple_dict: Dictionary containing node centrality values for all layer combinations
           of all possible lengths.
    :param node: Nodes for which the layer centrality is computed.
    :return:
    """

    shapley_value_dict = {}

    for layer in nx_layer_dict.keys():
        shapley_value_dict[layer] = 0

    for layer_permutation_tuple in layer_permutations_tuple_list:
        compute_shapley_for_tuple(layer_permutation_tuple, layer_combinations_tuple_dict, shapley_value_dict, node)

    shapley_value_sum = sum(shapley_value_dict.values())

    # Normalize
    for key in shapley_value_dict:
        shapley_value_dict[key] = shapley_value_dict[key] / shapley_value_sum * 100

    return shapley_value_dict


def compute_shapley_for_tuple(layer_permutation_tuple, layer_combinations_tuple_dict, shapley_value_dict, node):
    """
    Computes the Shapley value of a layer permutation in order of arrival for a given node. The values used to
    compute the shapley value are taken from the :param layer_combinations_tuple_dict.

    :param layer_permutation_tuple: Tuple containing a layer permutation.
    :param layer_combinations_tuple_dict: Dictionary containing node centrality values for all layer combinations
           of all possible lengths.
    :param shapley_value_dict: Reference to dictionary containing the shapley value of each layer given by the
                               :param layer_permutation_tuple in order of arrival.
    :param node: Node for which the shapley value is computed.
    :return:
    """

    for i in range(len(layer_permutation_tuple)):
        if i == 0:
            if node in layer_combinations_tuple_dict[layer_permutation_tuple[0]]:
                shapley_value_dict[layer_permutation_tuple[0]] += \
                    layer_combinations_tuple_dict[layer_permutation_tuple[0]][node]
            # print("Perm:", layer_permutation_tuple, "First Position", layer_permutation_tuple[0], "Shapley value",
            # shapley_value_dict[layer_permutation_tuple[0]])
        else:
            if node in layer_combinations_tuple_dict[''.join(sorted(list(layer_permutation_tuple[0:i + 1])))] and \
                    node in layer_combinations_tuple_dict[''.join(sorted(list(layer_permutation_tuple[0:i])))]:
                shapley_value_dict[layer_permutation_tuple[i]] += \
                    layer_combinations_tuple_dict[''.join(sorted(list(layer_permutation_tuple[0:i + 1])))][node] - \
                    layer_combinations_tuple_dict[''.join(sorted(list(layer_permutation_tuple[0:i])))][node]
                # print(''.join(layer_permutation_tuple[0:i+1]), ''.join(layer_permutation_tuple[0:i]))


if __name__ == "__main__":
    multilayeredNetwork = read("../resources/test_network.txt")
    nodeList = sorted(set(vertices(multilayeredNetwork)["actor"]))
    layers = to_nx_dict(multilayeredNetwork)
    print(compute_multinet_layer_centrality(layers, nodeList))
