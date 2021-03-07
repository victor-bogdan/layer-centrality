import matplotlib.pyplot as plt
from seaborn import lmplot
from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from uunet.multinet import read, vertices, to_nx_dict
from utils.layer_centrality import compute_multinet_layer_centrality


def compute_clusters(nodes_layer_centrality_dict, number_of_pcs, number_of_clusters):
    """
    Computes clusters of nodes using their layer centrality.

    :param nodes_layer_centrality_dict: Dictionary of dictionaries containing the centrality of
    each layer for a set of nodes.
    :param number_of_pcs: Number of principal components.
    :param number_of_clusters: Number of clusters.
    :return:
    """

    nodes_layer_centrality_data_frame = DataFrame.from_dict(nodes_layer_centrality_dict).T
    nodes_cluster_label_dictionary = \
        perform_kmeans(nodes_layer_centrality_data_frame, number_of_pcs, number_of_clusters)

    return nodes_cluster_label_dictionary


def perform_pca(nodes_layer_centrality_data_frame, number_of_pcs):
    """
    Performs principal component analysis on.

    :param nodes_layer_centrality_data_frame: Data frame containing layer centrality values for a given
    a given set of nodes.
    :param number_of_pcs: Number of principal components.
    :return: Data frame containing the principal components.
    """

    pca = PCA(n_components=number_of_pcs)

    # Normalise data
    normalized_data_frame = StandardScaler().fit_transform(nodes_layer_centrality_data_frame)
    principal_components = pca.fit_transform(normalized_data_frame)

    return DataFrame(principal_components)


def analyze_pca(nodes_layer_centrality_dict):
    """
    Function used to analyze the influence of each principal component which is obtained from the
    input data.

    :param nodes_layer_centrality_dict: Dictionary of dictionaries containing the centrality of
    each layer for a set of nodes.
    :return: void
    """

    nodes_layer_centrality_data_frame = DataFrame.from_dict(nodes_layer_centrality_dict).T

    # Normalise data
    normalised_data_frame = StandardScaler().fit_transform(nodes_layer_centrality_data_frame)

    pca = PCA(n_components=len(normalised_data_frame[1]))
    pca.fit_transform(normalised_data_frame)

    # Plotting the variances for each PC
    features = range(1, pca.n_components_ + 1)
    plt.bar(features, pca.explained_variance_ratio_, color='gold')
    plt.xlabel('Principal Components')
    plt.ylabel('Variance %')
    plt.xticks(features)
    plt.show()


def perform_kmeans(nodes_layer_centrality_data_frame, number_of_pcs=1, number_of_clusters=1, show_plot=False):
    """
    Performs kmeans on the centrality values of a set of nodes in order to create cluster of nodes based
    on the centrality of the layers.

    :param nodes_layer_centrality_data_frame: Data frame containing layer centrality values for a given
    a given set of nodes.
    :param number_of_pcs: Number of principal components.
    :param number_of_clusters: Number of clusters.
    :param show_plot: Flag for plotting of the clusters.
    :return: Dictionary of nodes and their respective cluster class.
    """

    principal_components_data_frame = perform_pca(nodes_layer_centrality_data_frame, number_of_pcs)

    model = KMeans(n_clusters=number_of_clusters)
    cluster_labels = model.fit(principal_components_data_frame)
    model.predict(principal_components_data_frame)

    # Plotting #

    # Plots the clusters for 2 or less principal components (2D)
    if number_of_pcs <= 2 and show_plot:
        plot_data = [["x", "y", "Cluster Class"]]
        for i in range(len(cluster_labels.labels_)):
            plot_data.append([
                principal_components_data_frame[0][i],
                principal_components_data_frame[1][i],
                cluster_labels.labels_[i]]
            )

        # Create the plot data DataFrame
        plot_data_data_frame = DataFrame(plot_data, columns=plot_data.pop(0))

        lmplot(data=plot_data_data_frame, x='x', y='y', hue='Cluster Class',
               fit_reg=False, legend=True, legend_out=True)
        plt.show()

    # Plotting #

    # Create node and cluster class dictionary
    node_cluster_labels_dictionary = \
        dict(zip(nodes_layer_centrality_data_frame.index, cluster_labels.labels_))

    return node_cluster_labels_dictionary


def analyze_kmeans(nodes_layer_centrality_dict, number_of_pcs, max_number_of_clusters):
    """
    Function used to analyze the inertia for different numbers of total clusters generated from the
    :param nodes_layer_centrality_dict. It is advised to use the 'elbow rule' when choosing the number
    of clusters for further uses.

    :param nodes_layer_centrality_dict: Dictionary of dictionaries containing the centrality of
    each layer for a set of nodes.
    :param number_of_pcs: Number of principal components.
    :param max_number_of_clusters: Maximum number of clusters.
    :return: void
    """
    nodes_layer_centrality_data_frame = DataFrame.from_dict(nodes_layer_centrality_dict).T

    principal_components_data_frame = perform_pca(nodes_layer_centrality_data_frame, number_of_pcs)
    inertias = []

    # Creating 10 K-Mean models while varying the number of clusters (k)
    for k in range(1, max_number_of_clusters):
        model = KMeans(n_clusters=k)

        # Fit model to samples
        model.fit(principal_components_data_frame)

        # Append the inertia to the list of inertias
        inertias.append(model.inertia_)

    plt.plot(range(1, max_number_of_clusters), inertias, '-p', color='gold')
    plt.xlabel('number of clusters, k')
    plt.ylabel('inertia')
    plt.show()


if __name__ == "__main__":
    multilayered_network = read("../resources/test.txt")
    node_list = sorted(set(vertices(multilayered_network)["actor"]))
    layers = to_nx_dict(multilayered_network)
    nodes_layer_centrality_dict_test = compute_multinet_layer_centrality(layers, node_list)
    nodes_cluster_label_dictionary_test = compute_clusters(nodes_layer_centrality_dict_test, 2, 3)
    print(nodes_cluster_label_dictionary_test)
