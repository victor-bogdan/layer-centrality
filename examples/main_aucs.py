from utils.clustering import *
from utils.analysis import *

multilayeredNetwork = ml.data("aucs")
nodeList = sorted(set(ml.vertices(multilayeredNetwork)["actor"]))
layers = ml.to_nx_dict(multilayeredNetwork)
targetsShapleyValueDict = compute_multinet_layer_centrality(layers, nodeList)
targets_shannon_entropy_dict = compute_shannon_entropy(targetsShapleyValueDict)
targets_data_frame = pd.DataFrame.from_dict(targetsShapleyValueDict).T
targets_data_frame['Shannon Entropy'] = pd.Series(targets_shannon_entropy_dict, index=targets_data_frame.index)
print(targets_data_frame)
targets_data_frame.to_csv('results/results_AUCS_degree_centrality.csv', encoding='utf-16')

# print(pd.DataFrame.from_dict(targetsShapleyValueDict).T)
# targetsClusterDataFrame = computeClusters(targetsShapleyValueDict, 2, 3)
# print(targetsClusterDataFrame)
