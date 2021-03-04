import uunet.multinet as ml
from combinations import *
from clustering import *
from analysis import *

multilayeredNetwork = ml.data("aucs")
# print(multilayeredNetwork)
print(ml.layers(multilayeredNetwork))
nodeList = sorted(set(ml.vertices(multilayeredNetwork)["actor"]))
print(nodeList)
layers = ml.to_nx_dict(multilayeredNetwork)
targetsShapleyValueDict = computeMultinetShapleyForTargets(layers, nodeList)
targets_shannon_entropy_dict = compute_shannon_entropy(targetsShapleyValueDict)
targets_data_frame = pd.DataFrame.from_dict(targetsShapleyValueDict).T
targets_data_frame['Shannon Entropy'] = pd.Series(targets_shannon_entropy_dict, index=targets_data_frame.index)
print(targets_data_frame)
targets_data_frame.to_csv('results_AUCS.csv', encoding='utf-16')

# print(pd.DataFrame.from_dict(targetsShapleyValueDict).T)
# targetsClusterDataFrame = computeClusters(targetsShapleyValueDict, 2, 3)
# print(targetsClusterDataFrame)
