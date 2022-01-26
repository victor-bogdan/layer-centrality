import abc
from itertools import combinations
from networkx import degree, harmonic_centrality, katz_centrality, adjacency_matrix, subgraph_centrality
from numpy.linalg import eigvals
from pandas import DataFrame
from layer_centrality.utils.data_helpers import get_node_connections_on_layers
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


class DegreeCentralityHelper(CentralityHelper):
    centrality_measure_name = "degree_centrality"

    def __init__(self, nx_layer_dict):
        super().__init__(nx_layer_dict)

    def get_node_degree_centrality_analysis(
            self,
            layers_dict,
            nodes_layer_centrality_dict,
            node
    ):
        """
        Creates a data frame with an analysis of the degree centrality for a specific :param node.

        :param layers_dict: Dictionary containing networkx layers
        :param nodes_layer_centrality_dict: Dictionary of dictionaries containing the centrality of
        each layer for a set of nodes.
        :param node: String representing a node.
        :return: Data frame containing analysis of :param node.
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
        analysis_results_data_frame = analysis_results_data_frame.round(2)

        # print(results_data_frame)

        return analysis_results_data_frame

    def get_node_centrality_dict(self, flattened_layer):
        """
        Returns a dictionary which contains the degree centrality measure for each node in :param flattened_layer,
        obtained from a combination of layers.

        :param flattened_layer: Networkx network which represents a flattened multilayered network, to which
        the degree centrality measure is applied.
        :return: Dictionary of degree centrality values for all nodes in the flattened network obtained from the
        combination of layers.
        """

        flattened_layer_degree_dict = {}

        degree_view = degree(flattened_layer)

        for degree_tuple in degree_view:
            flattened_layer_degree_dict[degree_tuple[0]] = degree_tuple[1]

        return flattened_layer_degree_dict


class HarmonicCentralityHelper(CentralityHelper):

    centrality_measure_name = "harmonic_centrality"

    def __init__(self, nx_layer_dict):
        super().__init__(nx_layer_dict)

    def get_node_centrality_dict(self, flattened_layer):
        """
        Returns a dictionary which contains the game theoretic centrality measure for each node in :param flattened_layer,
        obtained from a combination of layers.

        :param flattened_layer: Networkx network which represents a flattened multilayered network, to which
        the game theoretic centrality measure is applied.
        :return: Dictionary of game theoretic centrality values for all nodes in the flattened network obtained from the
        combination of layers.
        """

        return harmonic_centrality(flattened_layer)


class KatzCentralityHelper(CentralityHelper):

    centrality_measure_name = "katz_centrality"

    min_overall_eigenvalue = 0.01

    def __init__(self, nx_layer_dict):
        self.compute_min_overall_eigen_value(nx_layer_dict)
        super().__init__(nx_layer_dict)

    def compute_min_overall_eigen_value(self, nx_layer_dict):

        max_eigenvalue_list = []

        # Generate all possible layer combinations of all possible lengths
        for i in range(len(nx_layer_dict)):
            layer_combination_tuple_list = list(combinations(nx_layer_dict.keys(), i + 1))
            for layer_combination_tuple in layer_combination_tuple_list:
                max_eigenvalue_list.append(
                    self.compute_max_eigenvalue_for_layer_combination_tuple(nx_layer_dict, layer_combination_tuple))

        self.min_overall_eigenvalue = min(max_eigenvalue_list)

        print("Min ", self.min_overall_eigenvalue)

    def compute_max_eigenvalue_for_layer_combination_tuple(
            self,
            nx_layer_dict,
            layer_combination_tuple
    ):

        temp_multilayered_network = empty()

        for layer in layer_combination_tuple:
            add_nx_layer(temp_multilayered_network, nx_layer_dict[layer], layer)

        flatten(temp_multilayered_network, "flattened_layer", layers=layers(temp_multilayered_network))

        flattened_layer = to_nx_dict(temp_multilayered_network)["flattened_layer"]

        flattened_layer_adjacency_matrix = adjacency_matrix(flattened_layer)

        max_eigen_value = max(eigvals(flattened_layer_adjacency_matrix.todense()))

        print("Max Eigenv: ", layer_combination_tuple, max_eigen_value)

        return max_eigen_value

    def get_node_centrality_dict(self, flattened_layer):
        """
        Returns a dictionary which contains the katz centrality measure for each node in :param flattened_layer,
        obtained from a combination of layers.

        :param flattened_layer: Networkx network which represents a flattened multilayered network, to which
        the katz centrality measure is applied.
        :return: Dictionary of katz centrality values for all nodes in the flattened network obtained from the
        combination of layers.
        """

        print(len(flattened_layer.nodes))

        flattened_layer_katz_dict = {}

        alpha = 1 / self.min_overall_eigenvalue / 10.0

        print(alpha)

        centrality = katz_centrality(flattened_layer, alpha, normalized=False)

        for n, c in sorted(centrality.items()):
            flattened_layer_katz_dict[n] = float(c)
            # print(f"{n} {float(c):.2f}")

        # print("\n")

        return flattened_layer_katz_dict


class SubgraphCentralityHelper(CentralityHelper):

    centrality_measure_name = "subgraph_centrality"

    def __init__(self, nx_layer_dict):
        super().__init__(nx_layer_dict)

    def get_node_centrality_dict(self, flattened_layer):
        """
        Returns a dictionary which contains the subgraph centrality measure for each node in :param flattened_layer,
        obtained from a combination of layers.

        :param flattened_layer: Networkx network which represents a flattened multilayered network, to which
        the subgraph centrality measure is applied.
        :return: Dictionary of subgraph centrality values for all nodes in the flattened network obtained from the
        combination of layers.
        """

        return subgraph_centrality(flattened_layer)
