from itertools import permutations
from uunet.multinet import to_nx_dict, read, vertices


def compute_multinet_layer_centrality(nx_layer_dict, nodes, centrality_helper):
    """
    Computes the layer centrality for each node in a given multilayer network.

    :param nx_layer_dict: Multilayer network layer dictionary.
    :param nodes: List containing all nodes for which the layer centrality is computed.
    :param centrality_helper: The centrality helper which is being used.
    :return: Dictionary of dictionaries containing the centrality of each layer for each node in :param nodes.
    """

    nodes_layer_centrality_dict = {}

    layer_combinations_tuple_dict = \
        centrality_helper.layer_combinations_node_centrality_dict

    # Generate all possible layer permutations
    layer_permutations_tuple_list = list(permutations(nx_layer_dict.keys(), len(nx_layer_dict)))

    for node in nodes:
        nodes_layer_centrality_dict[node] = compute_multinet_layer_centrality_for_node(
            nx_layer_dict, layer_combinations_tuple_dict, layer_permutations_tuple_list, node)
        #  print("Node {0}: Shapley = {1}".format(nodes, nodes_layer_centrality_dict))

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

    # Marginal Contribution: divide by number of total combinations
    for key in shapley_value_dict:
        shapley_value_dict[key] = shapley_value_dict[key] / len(layer_permutations_tuple_list)

    # Transform to percentages
    shapley_value_sum = sum(shapley_value_dict.values())

    for key in shapley_value_dict:
        if shapley_value_sum != 0:
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
    multilayeredNetwork = read("../../internal/resources/test_network.txt")
    nodeList = sorted(set(vertices(multilayeredNetwork)["actor"]))
    layers = to_nx_dict(multilayeredNetwork)
    print(compute_multinet_layer_centrality(layers, nodeList))
