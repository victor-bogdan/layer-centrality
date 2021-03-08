from pandas import DataFrame, Series
from uunet.multinet import data, vertices, to_nx_dict
from algo.layer_centrality import compute_multinet_layer_centrality
from algo.analysis import compute_shannon_entropy
from algo.clustering import compute_clusters
from utils.plot_helper import draw_all_layers

multilayered_network = data("aucs")
node_list = sorted(set(vertices(multilayered_network)["actor"]))
layers = to_nx_dict(multilayered_network)
nodes_layer_centrality_dict = compute_multinet_layer_centrality(layers, node_list)
nodes_shannon_entropy_dict = compute_shannon_entropy(nodes_layer_centrality_dict)
nodes_cluster_label_dict = compute_clusters(nodes_layer_centrality_dict, 3, 3, False)

draw_all_layers("aucs", multilayered_network)

results_data_frame = DataFrame.from_dict(nodes_layer_centrality_dict).T
results_data_frame['Shannon Entropy'] = Series(nodes_shannon_entropy_dict, index=results_data_frame.index)
results_data_frame['Cluster Class'] = Series(nodes_cluster_label_dict, index=results_data_frame.index)
results_data_frame.to_csv('./results/aucs/aucs_results_degree_centrality.csv', encoding='utf-16')
print(results_data_frame)

# print(pd.DataFrame.from_dict(targetsShapleyValueDict).T)
# targetsClusterDataFrame = computeClusters(targetsShapleyValueDict, 2, 3)
# print(targetsClusterDataFrame)
