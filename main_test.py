from clustering import *

multilayeredNetwork = ml.read("test.txt")
nodeList = sorted(set(ml.vertices(multilayeredNetwork)["actor"]))
layers = ml.to_nx_dict(multilayeredNetwork)
targetsShapleyValueDict = computeMultinetShapleyForTargets(layers, nodeList)
targetsClusterDataFrame = computeClusters(targetsShapleyValueDict)
print(targetsClusterDataFrame)