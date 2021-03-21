import uunet.multinet as ml
import networkx as nx

multilayeredNetwork = ml.read("../resources/test.txt")
layers = ml.to_nx_dict(multilayeredNetwork)

ml.plot(multilayeredNetwork, vertex_labels_bbox={"boxstyle": 'round4', "fc": 'white'})

flattenedLayers = []

ml_l1l2l3 = ml.empty()
ml.add_nx_layer(ml_l1l2l3, layers["layer1"], "layer1")
ml.add_nx_layer(ml_l1l2l3, layers["layer2"], "layer2")
ml.add_nx_layer(ml_l1l2l3, layers["layer3"], "layer3")
ml.flatten(ml_l1l2l3, "flattened_l1l2l3", layers=ml.layers(ml_l1l2l3))
l1l2l3 = ml.to_nx_dict(ml_l1l2l3)["flattened_l1l2l3"]
print(nx.degree_centrality(l1l2l3))
print(nx.degree(l1l2l3), "\n")

ml_l1l2 = ml.empty()
ml.add_nx_layer(ml_l1l2, layers["layer1"], "layer1")
ml.add_nx_layer(ml_l1l2, layers["layer2"], "layer2")
ml.flatten(ml_l1l2, "flattened_l1l2", layers=ml.layers(ml_l1l2))
l1l2 = ml.to_nx_dict(ml_l1l2)["flattened_l1l2"]
flattenedLayers.append(l1l2)
print(nx.degree_centrality(l1l2))
print(nx.degree(l1l2), "\n")

ml_l1l3 = ml.empty()
ml.add_nx_layer(ml_l1l3, layers["layer1"], "layer1")
ml.add_nx_layer(ml_l1l3, layers["layer2"], "layer2")
ml.flatten(ml_l1l3, "flattened_l1l3", layers=ml.layers(ml_l1l3))
l1l3 = ml.to_nx_dict(ml_l1l3)["flattened_l1l3"]
flattenedLayers.append(l1l3)
print(nx.degree_centrality(l1l3))
print(nx.degree(l1l3), "\n")

ml_l2l3 = ml.empty()
ml.add_nx_layer(ml_l2l3, layers["layer1"], "layer1")
ml.add_nx_layer(ml_l2l3, layers["layer2"], "layer2")
ml.flatten(ml_l2l3, "flattened_l2l3", layers=ml.layers(ml_l2l3))
l2l3 = ml.to_nx_dict(ml_l2l3)["flattened_l2l3"]
flattenedLayers.append(l2l3)
print(nx.degree_centrality(l2l3))
print(nx.degree(l2l3), "\n")

l1 = layers["layer1"]
flattenedLayers.append(l1)
print(nx.degree_centrality(l1))
print(nx.degree(l1), "\n")

l2 = layers["layer2"]
flattenedLayers.append(l2)
print(nx.degree_centrality(l2))
print(nx.degree(l2), "\n")

l3 = layers["layer3"]
flattenedLayers.append(l3)
print(nx.degree_centrality(l3))
print(nx.degree(l3), "\n")
