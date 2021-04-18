from networkx import degree

DEGREE_CENTRALITY = "degree_centrality"


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


def get_node_degree_centrality_dict(flattened_layer):
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
