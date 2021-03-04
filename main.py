from utils.clustering import *
from utils.analysis import *

multilayeredNetwork = ml.read("resources/test.txt")
nodeList = sorted(set(ml.vertices(multilayeredNetwork)["actor"]))
layers = ml.to_nx_dict(multilayeredNetwork)
targetsShapleyValueDict = compute_multinet_layer_centrality(layers, nodeList)
targets_shannon_entropy_dict = compute_shannon_entropy(targetsShapleyValueDict)
targets_data_frame = pd.DataFrame.from_dict(targetsShapleyValueDict).T
targets_data_frame['Shannon Entropy'] = pd.Series(targets_shannon_entropy_dict, index=targets_data_frame.index)
print(targets_data_frame)
