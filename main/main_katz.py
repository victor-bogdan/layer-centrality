from pandas import DataFrame, Series
from uunet.multinet import data, vertices, to_nx_dict
from algo.core.layer_centrality import compute_multinet_layer_centrality
from algo.functions import compute_shannon_entropy
from algo.clustering.UncertainDBSCANHelper import UncertainDBSCANHelper
from utils.results_helper import get_number_of_layer_most_influenced_nodes, get_max_layer_contribution, \
    get_min_layer_contribution, save_results_data_frame_as_xlsx
from utils.KatzCentralityHelper import KatzCentralityHelper

DATASET_NAME = "aucs"

multilayered_network = data(DATASET_NAME)
node_list = sorted(set(vertices(multilayered_network)["actor"]))
nx_layer_dict = to_nx_dict(multilayered_network)

centrality_helper = KatzCentralityHelper(nx_layer_dict)

nodes_layer_centrality_dict = compute_multinet_layer_centrality(nx_layer_dict, node_list, centrality_helper)
nodes_shannon_entropy_dict = compute_shannon_entropy(nodes_layer_centrality_dict)

# Results DataFrame

results_data_frame = DataFrame.from_dict(nodes_layer_centrality_dict).T.sort_index(axis=1)
uncertain_dbscan_helper = UncertainDBSCANHelper(results_data_frame)

# Analysis

results_data_frame['shannon_entropy'] = Series(nodes_shannon_entropy_dict, index=results_data_frame.index)
results_data_frame['cluster_class'] = uncertain_dbscan_helper.uncertain_dbscan(0.036, 5, 0.0001)
results_data_frame.loc['mean'] = results_data_frame.mean()
results_data_frame = results_data_frame.round(2)

# Statistics

print(get_number_of_layer_most_influenced_nodes(nx_layer_dict.keys(), results_data_frame))
print(get_max_layer_contribution(nx_layer_dict.keys(), results_data_frame))
print(get_min_layer_contribution(nx_layer_dict.keys(), results_data_frame))

# Plots

'''
draw_results_layers(
    DATASET_NAME,
    centrality_helper.centrality_measure_name,
    multilayered_network,
    nodes_layer_centrality_dict,
    True
)
'''

# Save

save_results_data_frame_as_xlsx(DATASET_NAME, centrality_helper.centrality_measure_name, results_data_frame,
                                1, 1, len(results_data_frame) - 1, 5)
