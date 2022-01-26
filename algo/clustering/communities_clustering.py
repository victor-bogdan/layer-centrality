from itertools import combinations
from uunet.multinet import empty, add_nx_layer, flatten, layers, to_nx_dict
from networkx.algorithms.community import greedy_modularity_communities
from utils.result_helpers import draw_network_clustering_results


def create_layer_combinations_node_communities(
        data_set_name,
        nx_layer_dict,
        save_to_path=""
):
    """
    Creates plots containing node communities for all layer combinations of all possible lengths.

    :param data_set_name: Name of the data set.
    :param nx_layer_dict: Multilayer network layer dictionary.
    :param save_to_path: Disk path for saving the plots.
    :return: List of dictionaries containing nodes and their cluster labels for each network in
    """

    node_cluster_label_dict_list = []

    # Generate all possible layer combinations of all possible lengths
    for i in range(len(nx_layer_dict)):
        layer_combination_tuple_list = list(combinations(nx_layer_dict.keys(), i + 1))
        compute_layer_combinations_node_communities(data_set_name, nx_layer_dict,
            layer_combination_tuple_list, node_cluster_label_dict_list, save_to_path)

    return node_cluster_label_dict_list


def compute_layer_combinations_node_communities(
        data_set_name,
        nx_layer_dict,
        layer_combination_tuple_list,
        node_cluster_label_dict_list,
        save_to_path
):
    """
    Computes the node communities for each layer combination in :param layer_combination_tuple_list. Each tuple
    is sorted in lexicographic order. The layer combinations are flattened to avoid duplicate connections.

    :param data_set_name: Name of the data set.
    :param nx_layer_dict: Multilayer network layer dictionary.
    :param layer_combination_tuple_list: List of tuples containing layer combinations of same length.
    :param node_cluster_label_dict_list: List of dictionaries containing node clusters.
    :param save_to_path: Disk path for saving the plots.
    :return: void
    """

    for layer_combination_tuple in layer_combination_tuple_list:
        compute_flattened_layer_combination_node_community(data_set_name,
            nx_layer_dict, layer_combination_tuple, node_cluster_label_dict_list, save_to_path)
        # print(''.join(sorted(list(layerTuple))), layerTupleDict[''.join(sorted(list(layerTuple)))])


def compute_flattened_layer_combination_node_community(
        data_set_name,
        nx_layer_dict,
        layer_combination_tuple,
        node_cluster_label_dict_list,
        save_to_path
):
    """
    Computes the node community in a flattened network obtained from the combinations of layers.

    :param data_set_name: Name of the data set.
    :param nx_layer_dict: Multilayer network layer dictionary.
    :param layer_combination_tuple: Tuple containing a combination of layers.
    :param node_cluster_label_dict_list: List of dictionaries containing node clusters.
    :param save_to_path: Disk path for saving the plots.
    :return: void
    """

    temp_multilayered_network = empty()

    for layer in layer_combination_tuple:
        add_nx_layer(temp_multilayered_network, nx_layer_dict[layer], layer)

    flatten(temp_multilayered_network, "flattened_layer", layers=layers(temp_multilayered_network))

    flattened_layer_name = ''

    for layer_name_index in range(0, len(layer_combination_tuple)):
        flattened_layer_name += layer_combination_tuple[layer_name_index]
        if layer_name_index != (len(layer_combination_tuple)-1):
            flattened_layer_name += '_'

    flattened_layer = to_nx_dict(temp_multilayered_network)["flattened_layer"]

    c = list(greedy_modularity_communities(flattened_layer))

    node_cluster_label_dict = {}

    for community_class in range(0, len(c)):
        node_cluster_label_dict.update(dict.fromkeys(c[community_class], community_class))

    draw_network_clustering_results(
        data_set_name,
        flattened_layer_name,
        flattened_layer,
        node_cluster_label_dict,
        save_to_path
    )

    layer_node_cluster_label_dict = {flattened_layer_name: node_cluster_label_dict}

    node_cluster_label_dict_list.append(layer_node_cluster_label_dict)
