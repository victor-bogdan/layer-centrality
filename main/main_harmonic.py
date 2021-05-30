from pandas import DataFrame, Series
from uunet.multinet import data, vertices, to_nx_dict
from algo.layer_centrality import compute_multinet_layer_centrality
from algo.analysis import compute_shannon_entropy
from algo.kmeans_clustering import compute_clusters
from algo.communities_clustering import create_layer_combinations_node_communities
from utils.data_helper import draw_layers, get_node_connections_on_layers
from utils.results_helper import plot_results_histograms, draw_results_layers, \
    save_results_analysis_data_frames_as_xlsx, save_results_data_frame_as_xlsx, \
    draw_flattened_network_clustering_results, draw_network_clustering_results
from utils.HarmonicCentralityHelper import HarmonicCentralityHelper

DATASET_NAME = "aucs"

multilayered_network = data(DATASET_NAME)
node_list = sorted(set(vertices(multilayered_network)["actor"]))
nx_layer_dict = to_nx_dict(multilayered_network)

centrality_helper = HarmonicCentralityHelper(nx_layer_dict)

nodes_layer_centrality_dict = compute_multinet_layer_centrality(nx_layer_dict, node_list, centrality_helper)
nodes_shannon_entropy_dict = compute_shannon_entropy(nodes_layer_centrality_dict)

results_data_frame = DataFrame.from_dict(nodes_layer_centrality_dict).T.sort_index(axis=1)
results_data_frame['shannon_entropy'] = Series(nodes_shannon_entropy_dict, index=results_data_frame.index)
results_data_frame.loc['mean'] = results_data_frame.mean()
results_data_frame = results_data_frame.round(2)

draw_results_layers(
    DATASET_NAME,
    centrality_helper.centrality_measure_name,
    multilayered_network,
    nodes_layer_centrality_dict,
    True
)

save_results_data_frame_as_xlsx(DATASET_NAME, centrality_helper.centrality_measure_name, results_data_frame,
                                1, 1, len(results_data_frame) - 1, 5)
