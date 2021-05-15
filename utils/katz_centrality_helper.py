from networkx import katz_centrality
from networkx.linalg.graphmatrix import adjacency_matrix
from numpy.linalg import eigvals


def get_node_katz_centrality_dict(flattened_layer):
    """
    Returns a dictionary which contains the katz centrality measure for each node in :param flattened_layer,
    obtained from a combination of layers.

    :param flattened_layer: Networkx network which represents a flattened multilayered network, to which
    the katz centrality measure is applied.
    :return: Dictionary of katz centrality values for all nodes in the flattened network obtained from the
    combination of layers.
    """

    flattened_layer_katz_dict = {}

    flattened_layer_adjacency_matrix = adjacency_matrix(flattened_layer)
    
    max_eigen_value = max(eigvals(flattened_layer_adjacency_matrix.todense()))
    
    alpha = (1/max_eigen_value) / 2.0

    centrality = katz_centrality(flattened_layer, alpha, normalized=False)

    for n, c in sorted(centrality.items()):
        flattened_layer_katz_dict[n] = float(c)
        # print(f"{n} {float(c):.2f}")
        
    # print("\n")

    return flattened_layer_katz_dict
