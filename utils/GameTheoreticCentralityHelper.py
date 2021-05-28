from algo.game_theoretic_centrality import game_theoretic_centrality
from utils.CentralityHelper import CentralityHelper


class GameTheoreticCentralityHelper(CentralityHelper):

    centrality_measure_name = "game_theoretic_centrality"

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

        flattened_layer_degree_dict = {}

        for node in flattened_layer.nodes:
            flattened_layer_degree_dict[node] = game_theoretic_centrality(flattened_layer, node)

        return flattened_layer_degree_dict
