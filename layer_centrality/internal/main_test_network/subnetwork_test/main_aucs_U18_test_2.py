from os.path import dirname
from pandas import DataFrame, Series
from uunet.multinet import read, to_nx_dict
from layer_centrality.algo.core.layer_centrality import compute_multinet_layer_centrality
from layer_centrality.algo.functions import compute_shannon_entropy
from layer_centrality.utils import DEGREE_CENTRALITY

"""
Test module for node U18 layers: 'leisure' and 'work'.

Connection Order analysis after change:
Leisure: Order 1: 0, Order 2: 0, Order 3: 3
Work: Order 1: 1, Order 2: 0, Order 3: 0
"""

CENTRALITY_MEASURE = DEGREE_CENTRALITY

project_root_path = dirname(dirname(__file__))

multi_layered_network = read("{0}/resources/aucs_U18_test_2.txt".format(project_root_path))
# nodeList = sorted(set(vertices(multi_layered_network)["actor"]))
nodeList = ['U18']
layers = to_nx_dict(multi_layered_network)
nodes_layer_centrality_dict = compute_multinet_layer_centrality(layers, nodeList, DEGREE_CENTRALITY)
nodes_shannon_entropy_dict = compute_shannon_entropy(nodes_layer_centrality_dict)

result_data_frame = DataFrame.from_dict(nodes_layer_centrality_dict).T
result_data_frame['Shannon Entropy'] = Series(nodes_shannon_entropy_dict, index=result_data_frame.index)
print(result_data_frame)
