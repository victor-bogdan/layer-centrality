import networkx as nx
import matplotlib.pyplot as plt

G1 = nx.Graph()

G1.add_node(1)
G1.add_node(2)
G1.add_node(3)
G1.add_node(4)
G1.add_node(5)

G1.add_edge(1, 2)
G1.add_edge(2, 3)
G1.add_edge(3, 4)
G1.add_edge(4, 5)

centrality = nx.betweenness_centrality(G1, normalized=False)

# nx.draw(G1, with_labels=True)
# plt.title("Layer 1")
# plt.show()

print(centrality)

G2 = nx.Graph()

G2.add_node(1)
G2.add_node(2)
G2.add_node(3)
G2.add_node(4)
G2.add_node(5)
G2.add_node(6)

G2.add_edge(1, 2)
G2.add_edge(2, 3)
G2.add_edge(3, 4)
G2.add_edge(4, 5)
G2.add_edge(2, 6)
# G2.add_edge(6, 7)
# G2.add_edge(6, 8)
# G2.add_edge(6, 9)

centrality = nx.betweenness_centrality(G2, normalized=False)

# nx.draw(G2, with_labels=True)
# plt.title("Layer 2")
# plt.show()

print(centrality)

