from networkx import eigenvector_centrality


def get_node_eigenvector_centrality_dict(flattened_layer):
    """
    Returns a dictionary which contains the eigenvector centrality measure for each node in :param flattened_layer,
    obtained from a combination of layers.

    :param flattened_layer: Networkx network which represents a flattened multilayered network, to which
    the eigenvector centrality measure is applied.
    :return: Dictionary of eigenvector centrality values for all nodes in the flattened network obtained from the
    combination of layers.
    """

    return eigenvector_centrality(flattened_layer, 10000)
