from networkx import harmonic_centrality
from utils.CentralityHelper import CentralityHelper


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
