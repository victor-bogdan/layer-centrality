from uunet.multinet import read, vertices, to_nx_dict
from utils.layer_centrality import compute_multinet_layer_centrality
from utils.clustering import compute_clusters

multilayeredNetwork = read("../resources/test.txt")
nodeList = sorted(set(vertices(multilayeredNetwork)["actor"]))
layers = to_nx_dict(multilayeredNetwork)
nodes_layer_centrality_dict = compute_multinet_layer_centrality(layers, nodeList)
nodes_cluster_data_frame = compute_clusters(nodes_layer_centrality_dict, 2, 3)
print(nodes_cluster_data_frame)