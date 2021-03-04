from pandas import DataFrame, Series
from uunet.multinet import read, vertices, to_nx_dict
from utils.layer_centrality import compute_multinet_layer_centrality
from utils.analysis import compute_shannon_entropy

multilayeredNetwork = read("resources/test.txt")
nodeList = sorted(set(vertices(multilayeredNetwork)["actor"]))
layers = to_nx_dict(multilayeredNetwork)
targetsShapleyValueDict = compute_multinet_layer_centrality(layers, nodeList)
targets_shannon_entropy_dict = compute_shannon_entropy(targetsShapleyValueDict)
targets_data_frame = DataFrame.from_dict(targetsShapleyValueDict).T
targets_data_frame['Shannon Entropy'] = Series(targets_shannon_entropy_dict, index=targets_data_frame.index)
print(targets_data_frame)
