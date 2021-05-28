from networkx import eigenvector_centrality
from utils.CentralityHelper import CentralityHelper


class EigenvectorCentralityHelper(CentralityHelper):

    centrality_measure_name = "eigenvector_centrality"

    def __init__(self, nx_layer_dict):
        super().__init__(nx_layer_dict)

    def get_node_centrality_dict(self, flattened_layer):
        """
        Returns a dictionary which contains the eigenvector centrality measure for each node in :param flattened_layer,
        obtained from a combination of layers.

        :param flattened_layer: Networkx network which represents a flattened multilayered network, to which
        the eigenvector centrality measure is applied.
        :return: Dictionary of eigenvector centrality values for all nodes in the flattened network obtained from the
        combination of layers.
        """

        return eigenvector_centrality(flattened_layer, 10000)
