import uunet.multinet as ml
import networkx as nx
import matplotlib.pyplot as plt

n = ml.read("test.txt")

ml.plot(n, vertex_labels_bbox={"boxstyle": 'round4', "fc": 'white'})

ml.flatten(n, "flattened", layers=ml.layers(n))

ml.plot(n, vertex_labels_bbox={"boxstyle": 'round4', "fc": 'white'})

layers = ml.to_nx_dict(n)

nx.draw(layers["flattened"], with_labels=True)
plt.draw()
plt.show()

print(nx.degree_centrality(layers["flattened"]))