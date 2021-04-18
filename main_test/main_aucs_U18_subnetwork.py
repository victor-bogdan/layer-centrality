from os.path import dirname
from pandas import DataFrame, Series
from uunet.multinet import read, vertices, to_nx_dict, plot
from algo.layer_centrality import compute_multinet_layer_centrality
from algo.analysis import compute_shannon_entropy
from utils.centrality_measure_helper import DEGREE_CENTRALITY

CENTRALITY_MEASURE = DEGREE_CENTRALITY

project_root_path = dirname(dirname(__file__))

multi_layered_network = read("{0}/resources/aucs_U18_subnetwork.txt".format(project_root_path))
# nodeList = sorted(set(vertices(multi_layered_network)["actor"]))
nodeList = ['U18']
layers = to_nx_dict(multi_layered_network)
nodes_layer_centrality_dict = compute_multinet_layer_centrality(layers, nodeList, DEGREE_CENTRALITY)
nodes_shannon_entropy_dict = compute_shannon_entropy(nodes_layer_centrality_dict)

plot(multi_layered_network, vertex_labels_bbox={"boxstyle": 'round4', "fc": 'white'})

result_data_frame = DataFrame.from_dict(nodes_layer_centrality_dict).T
result_data_frame['Shannon Entropy'] = Series(nodes_shannon_entropy_dict, index=result_data_frame.index)
print(result_data_frame)