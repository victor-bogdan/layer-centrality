from pandas import DataFrame, Series
from uunet.multinet import data, vertices, to_nx_dict
from layer_centrality.algo.core.layer_centrality import compute_multinet_layer_centrality
from layer_centrality.algo.functions import compute_shannon_entropy
from layer_centrality.algo.clustering.UncertainDBSCANHelper import UncertainDBSCANHelper
from layer_centrality.utils.result_helpers import get_number_of_layer_most_influenced_nodes, get_max_layer_contribution, \
    get_min_layer_contribution, get_layer_centrality_excel_models, save_layer_centrality_excel_models_as_xlsx
from layer_centrality.utils.centrality_helpers import HarmonicCentralityHelper

DATASET_NAME = "aucs"

multilayered_network = data(DATASET_NAME)
node_list = sorted(set(vertices(multilayered_network)["actor"]))
nx_layer_dict = to_nx_dict(multilayered_network)

centrality_helper = HarmonicCentralityHelper(nx_layer_dict)

nodes_layer_centrality_dict = compute_multinet_layer_centrality(nx_layer_dict, node_list, centrality_helper)
nodes_shannon_entropy_dict = compute_shannon_entropy(nodes_layer_centrality_dict)

# Analysis

results_data_frame = DataFrame.from_dict(nodes_layer_centrality_dict).T.sort_index(axis=1)

uncertain_dbscan_helper = UncertainDBSCANHelper(results_data_frame)
cluster_labels = uncertain_dbscan_helper.uncertain_dbscan(0.014, 5, 0.0001)

results_data_frame['shannon_entropy'] = Series(nodes_shannon_entropy_dict, index=results_data_frame.index)
results_data_frame['cluster_class'] = cluster_labels
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
    "{0}/internal/results".format(dirname(dirname(__file__)))
)
'''

# Save

dataframe_excel_model_list = get_layer_centrality_excel_models(results_data_frame, set(cluster_labels))

save_layer_centrality_excel_models_as_xlsx(
    DATASET_NAME, centrality_helper.centrality_measure_name, dataframe_excel_model_list)

print(results_data_frame)
