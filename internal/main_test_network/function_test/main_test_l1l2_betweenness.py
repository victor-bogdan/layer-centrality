import uunet.multinet as ml
import networkx as nx

multilayeredNetwork = ml.read("../../resources/test_network.txt")
layers = ml.to_nx_dict(multilayeredNetwork)

l1 = layers["layer1"]
print("l1", nx.betweenness_centrality(l1, normalized=False))

l2 = layers["layer2"]
print("l2", nx.betweenness_centrality(l2, normalized=False))

'''
l3 = layers["layer3"]
print(nx.katz_centrality(l3))
print(nx.degree(l3), "\n")
'''

ml_l1l2 = ml.empty()
ml.add_nx_layer(ml_l1l2, layers["layer1"], "layer1")
ml.add_nx_layer(ml_l1l2, layers["layer2"], "layer2")
ml.flatten(ml_l1l2, "flattened_l1l2", layers=ml.layers(ml_l1l2))
ml.plot(ml_l1l2, vertex_labels_bbox={"boxstyle": 'round4', "fc": 'white'})
l1l2 = ml.to_nx_dict(ml_l1l2)["flattened_l1l2"]
print("l12", nx.betweenness_centrality(l1l2, normalized=False))
