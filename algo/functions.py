import numpy as np
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


def kl_divergence(p, q):
    """
    Computes the Kullback-Leibler divergence

    :param p: First probability distribution.
    :param q: second probability distribution.
    :return: KL divergence.
    """

    kl_div = p * np.log(p / q)
    return np.sum(kl_div)


def js_divergence(p, q, alpha=0.1):
    """
    Computes the Jensen-Shannon divergence

    :param p: First probability distribution.
    :param q: Second probability distribution.
    :param alpha: Floating value used to avoid by 0 division in case q has probabilities with
    value 0.
    :return: JS divergence.
    """

    p = np.asarray(p).astype(float)
    q = np.asarray(q).astype(float)

    p += alpha
    q += alpha

    # normalize
    p /= p.sum()
    q /= q.sum()

    m = (p + q) / 2

    return (kl_divergence(p, m) + kl_divergence(q, m)) / 2
