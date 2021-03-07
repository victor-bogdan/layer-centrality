from pandas import DataFrame, Series
from uunet.multinet import read, vertices, to_nx_dict
from utils.layer_centrality import compute_multinet_layer_centrality
from utils.analysis import compute_shannon_entropy
from utils.clustering import compute_clusters

multi_layered_network = read("resources/test.txt")
nodeList = sorted(set(vertices(multi_layered_network)["actor"]))
layers = to_nx_dict(multi_layered_network)
nodes_layer_centrality_dict = compute_multinet_layer_centrality(layers, nodeList)
nodes_shannon_entropy_dict = compute_shannon_entropy(nodes_layer_centrality_dict)
nodes_cluster_label_dict = compute_clusters(nodes_layer_centrality_dict, 2, 3)

result_data_frame = DataFrame.from_dict(nodes_layer_centrality_dict).T
result_data_frame['Shannon Entropy'] = Series(nodes_shannon_entropy_dict, index=result_data_frame.index)
result_data_frame['Cluster Class'] = Series(nodes_cluster_label_dict, index=result_data_frame.index)
print(result_data_frame)
