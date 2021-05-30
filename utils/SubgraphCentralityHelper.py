from networkx import subgraph_centrality
from utils.CentralityHelper import CentralityHelper


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
