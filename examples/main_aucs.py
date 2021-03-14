from pandas import DataFrame, Series
from uunet.multinet import data, vertices, to_nx_dict
from algo.layer_centrality import compute_multinet_layer_centrality
from algo.analysis import compute_shannon_entropy
from algo.clustering import compute_clusters
from utils.data_helper import draw_all_layers
from utils.results_helper import plot_results_histograms
from utils.results_helper import save_results_data_frame

DATASET_NAME = "aucs"
CENTRALITY_MEASURE = "degree_centrality"

multilayered_network = data(DATASET_NAME)
node_list = sorted(set(vertices(multilayered_network)["actor"]))
layers = to_nx_dict(multilayered_network)

nodes_layer_centrality_dict = compute_multinet_layer_centrality(layers, node_list)
nodes_shannon_entropy_dict = compute_shannon_entropy(nodes_layer_centrality_dict)
nodes_cluster_label_dict = compute_clusters(nodes_layer_centrality_dict, 3, 3, False)

draw_all_layers("aucs", multilayered_network, True)

results_data_frame = DataFrame.from_dict(nodes_layer_centrality_dict).T.sort_index(axis=1)
results_data_frame['Shannon Entropy'] = Series(nodes_shannon_entropy_dict, index=results_data_frame.index)
results_data_frame['Cluster Class'] = Series(nodes_cluster_label_dict, index=results_data_frame.index)

plot_results_histograms(DATASET_NAME, CENTRALITY_MEASURE, results_data_frame,
                        vertices(multilayered_network)["layer"], 20, 5, True)
plot_results_histograms(DATASET_NAME, CENTRALITY_MEASURE, results_data_frame,
                        "Shannon Entropy", 3, 1, True)

save_results_data_frame(DATASET_NAME, CENTRALITY_MEASURE, results_data_frame)

# print(pd.DataFrame.from_dict(targetsShapleyValueDict).T)
# targetsClusterDataFrame = computeClusters(targetsShapleyValueDict, 2, 3)
# print(targetsClusterDataFrame)
