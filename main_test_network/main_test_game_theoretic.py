from os.path import dirname
from pandas import DataFrame, Series
from uunet.multinet import read, vertices, to_nx_dict
from algo.layer_centrality import compute_multinet_layer_centrality
from algo.analysis import compute_shannon_entropy
from utils.centrality_measure_helper import GAME_THEORETIC_CENTRALITY

CENTRALITY_MEASURE = GAME_THEORETIC_CENTRALITY

project_root_path = dirname(dirname(__file__))

multi_layered_network = read("{0}/resources/test_network.txt".format(project_root_path))
nodeList = sorted(set(vertices(multi_layered_network)["actor"]))
layers = to_nx_dict(multi_layered_network)
nodes_layer_centrality_dict = compute_multinet_layer_centrality(layers, nodeList, CENTRALITY_MEASURE)
nodes_shannon_entropy_dict = compute_shannon_entropy(nodes_layer_centrality_dict)

result_data_frame = DataFrame.from_dict(nodes_layer_centrality_dict).T
result_data_frame['Shannon Entropy'] = Series(nodes_shannon_entropy_dict, index=result_data_frame.index)
print(result_data_frame)
