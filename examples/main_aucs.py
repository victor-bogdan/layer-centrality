from pandas import DataFrame, Series
from uunet.multinet import data, vertices, to_nx_dict
from utils.layer_centrality import compute_multinet_layer_centrality
from utils.analysis import compute_shannon_entropy

multilayered_network = data("aucs")
node_list = sorted(set(vertices(multilayered_network)["actor"]))
layers = to_nx_dict(multilayered_network)
nodes_layer_centrality_dict = compute_multinet_layer_centrality(layers, node_list)
nodes_shannon_entropy_dict = compute_shannon_entropy(nodes_layer_centrality_dict)

results_data_frame = DataFrame.from_dict(nodes_layer_centrality_dict).T
results_data_frame['Shannon Entropy'] = Series(nodes_shannon_entropy_dict, index=results_data_frame.index)
results_data_frame.to_csv('results/results_AUCS_degree_centrality.csv', encoding='utf-16')
print(results_data_frame)

# print(pd.DataFrame.from_dict(targetsShapleyValueDict).T)
# targetsClusterDataFrame = computeClusters(targetsShapleyValueDict, 2, 3)
# print(targetsClusterDataFrame)
