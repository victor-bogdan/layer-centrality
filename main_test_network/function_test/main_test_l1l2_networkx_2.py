import networkx as nx
import matplotlib.pyplot as plt

G1 = nx.Graph()

G1.add_node(1)
G1.add_node(2)
G1.add_node(3)
G1.add_node(4)
G1.add_node(5)

G1.add_edge(1, 2)
G1.add_edge(1, 4)
G1.add_edge(2, 3)
G1.add_edge(2, 5)

#centrality = nx.katz_centrality(G1, normalized=False)
centrality = nx.degree_centrality(G1)

nx.draw(G1, with_labels=True)
plt.title("Layer 1")
plt.show()

print(centrality)

G2 = nx.Graph()

G2.add_node(1)
G2.add_node(2)
G2.add_node(3)
G2.add_node(5)
G2.add_node(6)

G2.add_edge(1, 5)
G2.add_edge(1, 6)
G2.add_edge(6, 2)
G2.add_edge(2, 3)

#centrality = nx.katz_centrality(G2, normalized=False)
centrality = nx.degree_centrality(G2)

nx.draw(G2, with_labels=True)
plt.title("Layer 2")
plt.show()

print(centrality)

G3 = nx.Graph()

G3.add_node(1)
G3.add_node(2)
G3.add_node(3)
G3.add_node(4)
G3.add_node(5)
G3.add_node(6)

G3.add_edge(1, 4)
G3.add_edge(1, 5)
G3.add_edge(1, 6)
G3.add_edge(1, 2)
G3.add_edge(2, 5)
G3.add_edge(2, 6)
G3.add_edge(2, 3)

#centrality = nx.katz_centrality(G3, normalized=False)
centrality = nx.degree_centrality(G3)

nx.draw(G3, with_labels=True)
plt.title("Layer 1_2")
plt.show()

print(centrality)

