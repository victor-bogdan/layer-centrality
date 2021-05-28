import abc
from itertools import combinations
from uunet.multinet import empty, add_nx_layer, flatten, layers, to_nx_dict


class CentralityHelper:

    layer_combinations_node_centrality_dict = {}

    def __init__(self, nx_layer_dict):
        self.create_layer_combinations_node_centrality_dict(nx_layer_dict)

    def create_layer_combinations_node_centrality_dict(
            self,
            nx_layer_dict
    ):
        """
        Creates a dictionary containing node centrality values for all layer combinations of all possible lengths.

        :param nx_layer_dict: Multilayer network layer dictionary.
        :return: Dictionary containing node centrality values for all layer combinations of all possible lengths
        """

        # Generate all possible layer combinations of all possible lengths
        for i in range(len(nx_layer_dict)):
            layer_combination_tuple_list = list(combinations(nx_layer_dict.keys(), i + 1))
            self.compute_layer_combinations_node_centrality(
                nx_layer_dict, layer_combination_tuple_list, self.layer_combinations_node_centrality_dict)

        return self.layer_combinations_node_centrality_dict

    def compute_layer_combinations_node_centrality(
            self,
            nx_layer_dict,
            layer_combination_tuple_list,
            layer_combinations_node_centrality_dict
    ):
        """
        Computes the node centrality for each layer combination in :param layer_combination_tuple_list. Each tuple
        is sorted in lexicographic order. In order to compute the node centrality, the layer combinations are flattened
        to avoid duplicate connections.

        :param nx_layer_dict: Multilayer network layer dictionary.
        :param layer_combination_tuple_list: List of tuples containing layer combinations of same length.
        :param layer_combinations_node_centrality_dict: Dictionary reference
        :return: void
        """

        for layer_combination_tuple in layer_combination_tuple_list:
            layer_combinations_node_centrality_dict[''.join(sorted(list(layer_combination_tuple)))] = \
                self.compute_flattened_layer_combination_node_centrality(
                    nx_layer_dict, layer_combination_tuple)
            # print(''.join(sorted(list(layerTuple))), layerTupleDict[''.join(sorted(list(layerTuple)))])

    def compute_flattened_layer_combination_node_centrality(
            self,
            nx_layer_dict,
            layer_combination_tuple
    ):
        """
        Computes the centrality values for all nodes in a flattened network obtained from the combinations of
        layers.

        :param nx_layer_dict: Multilayer network layer dictionary.
        :param layer_combination_tuple: Tuple containing a combination of layers.
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

        return self.get_node_centrality_dict(flattened_layer)

    @abc.abstractmethod
    def get_node_centrality_dict(self, flattened_layer):
        return {}
