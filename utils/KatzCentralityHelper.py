from networkx import katz_centrality
from uunet.multinet import empty, add_nx_layer, flatten, layers, to_nx_dict
from networkx.linalg.graphmatrix import adjacency_matrix
from itertools import combinations
from numpy.linalg import eigvals
from utils.CentralityHelper import CentralityHelper


class KatzCentralityHelper(CentralityHelper):

    centrality_measure_function = "katz_centrality"

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

        alpha = (1/self.min_overall_eigenvalue) / 2.0

        print(alpha)

        centrality = katz_centrality(flattened_layer, alpha, normalized=False, max_iter=100)

        for n, c in sorted(centrality.items()):
            flattened_layer_katz_dict[n] = float(c)
            # print(f"{n} {float(c):.2f}")

        # print("\n")

        return flattened_layer_katz_dict
