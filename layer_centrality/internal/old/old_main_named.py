import uunet.multinet as ml
import networkx as nx
import matplotlib.pyplot as plt

n = ml.read("../resources/test_network_named.txt")

ml.plot(n, vertex_labels_bbox={"boxstyle": 'round4', "fc": 'white'})

ml.flatten(n, "flattened", layers=ml.layers(n))

ml.plot(n, vertex_labels_bbox={"boxstyle": 'round4', "fc": 'white'})

layers = ml.to_nx_dict(n)

nx.draw(layers["flattened"], with_labels=True)
plt.draw()
# plt.show()

print(nx.degree(layers["Facebook"]))
print(nx.degree(layers["Twitter"]))
print(nx.degree(layers["flattened"]))
print(nx.katz_centrality(layers["Facebook"], normalized=False))

'''
# Degree

facebook_layer_degree_dict = {}

degree_view = nx.degree_centrality(layers["Facebook"])

for degree_tuple in degree_view:
    facebook_layer_degree_dict[degree_tuple[0]] = degree_tuple[1]

print(facebook_layer_degree_dict)

'''

# Katz
