from scipy.stats import entropy


def compute_shannon_entropy(node_shapley_value_dict):
    """
    Computes the shannon entropy for the shapley value given by the layers for a node. The shapley value
    is considered to be normalized to 1, therefore each layer value is considered a probability.

    :param node_shapley_value_dict: Dictionary containing the shapley value for some given nodes.
    :return: Dictionary containing the shannon entropy for each node
    """

    targets_shannon_entropy_dict = {}

    for node in node_shapley_value_dict:
        target_layer_percentages = list(node_shapley_value_dict[node].values())
        targets_shannon_entropy_dict[node] = entropy(target_layer_percentages, base=2)

    return targets_shannon_entropy_dict
