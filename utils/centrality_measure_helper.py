from utils.degree_centrality_helper import get_node_degree_centrality_analysis, get_node_degree_centrality_dict
from utils.katz_centrality_helper import get_node_katz_centrality_dict
from utils.eigenvector_centrality_helper import get_node_eigenvector_centrality_dict
from utils.game_theoretic_centrality_helper import get_node_game_theoretic_centrality_dict

DEGREE_CENTRALITY = "degree_centrality"
EIGENVECTOR_CENTRALITY = "eigenvector_centrality"
KATZ_CENTRALITY = "katz_centrality"
GAME_THEORETIC_CENTRALITY = "game_theoretic_centrality"


def get_node_centrality_analysis(
        centrality_measure,
        layers_dict,
        nodes_layer_centrality_dict,
        node
):
    """
    Creates a data frame with an analysis of the :param centrality for a specific :param node.

    :param centrality_measure: The centrality measure which is being used.
    :param layers_dict: Dictionary containing networkx layers.
    :param nodes_layer_centrality_dict: Dictionary of dictionaries containing the centrality of
    each layer for a set of nodes.
    :param node: String representing a node.
    :return: Data frame containing analysis of :param node.
    """

    if centrality_measure == DEGREE_CENTRALITY:
        return get_node_degree_centrality_analysis(
            layers_dict,
            nodes_layer_centrality_dict,
            node
        )


def get_node_centrality_dict(centrality_measure, flattened_layer):
    """
    Returns a dictionary which contains the :param centrality_measure for each node in :param flattened_layer,
    obtained from a combination of layers.

    :param centrality_measure: The centrality measure which is being used.
    :param flattened_layer: Networkx network which represents a flattened multilayered network, to which
    the :param centrality measure is applied.
    :return: Dictionary of centrality values for all nodes in the flattened network obtained from a
    combination of layers.
    """

    if centrality_measure == DEGREE_CENTRALITY:
        return get_node_degree_centrality_dict(flattened_layer)
    elif centrality_measure == EIGENVECTOR_CENTRALITY:
        return get_node_eigenvector_centrality_dict(flattened_layer)
    elif centrality_measure == KATZ_CENTRALITY:
        return get_node_katz_centrality_dict(flattened_layer)
    elif centrality_measure == GAME_THEORETIC_CENTRALITY:
        return get_node_game_theoretic_centrality_dict(flattened_layer)
