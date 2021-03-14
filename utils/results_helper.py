import matplotlib.pyplot as plt
from uunet.multinet import to_nx_dict
from networkx import draw, nx_agraph
from os.path import dirname

"""
Dictionary containing settings for each class of nodes.
"""
NODE_CLASS_SETTINGS_DICT = {
    1: {'primary_color': '#DD3827'},
    2: {'primary_color': '#EFA811'},
    3: {'primary_color': '#F7F304'},
    4: {'primary_color': '#2CC82E'},
}


def get_node_class(max_layer_centrality):
    """
    Returns the node class based on the maximum layer centrality of the respective node in a multilayered
    network.

    :param max_layer_centrality: Maximum layer centrality for a node in a multilayered network
    :return: String representing node class
    """

    if max_layer_centrality >= 75:
        return 1
    elif max_layer_centrality >= 50:
        return 2
    elif max_layer_centrality >= 35:
        return 3
    else:
        return 4


def get_nodes_class_dict(nodes_layer_centrality_dict):
    """
    Creates a dictionary containing the node class for each node in :param nodes_layer_centrality_dict

    :param nodes_layer_centrality_dict: Dictionary of dictionaries containing the centrality of
    each layer for a set of nodes.
    :return: Dictionary containing the node class for each node in :param nodes_layer_centrality_dict
    """

    nodes_class_dict = {}

    for node_key in nodes_layer_centrality_dict:
        nodes_class_dict[node_key] = get_node_class(max(nodes_layer_centrality_dict[node_key].values()))

    return nodes_class_dict


def draw_results_layers(
        data_set_name,
        centrality_measure,
        multilayered_network,
        results_data_frame,
        save_to_disk=False
):
    """
    Plots all layers in the given multilayered network and applies the settings for each node based on
    its class.

    :param data_set_name: Name of the data set.
    :param centrality_measure: Name of the used centrality measure.
    :param multilayered_network: Multilayered network.
    :param results_data_frame: Dataframe containing all results.
    :param save_to_disk: Flag for enabling/disabling saving plots to disk.
    :return: void
    """

    layers = to_nx_dict(multilayered_network)

    for layer_name in layers.keys():
        layer = layers[layer_name]

        color_map = []

        for node in layer:
            color_map.append(
                NODE_CLASS_SETTINGS_DICT[results_data_frame.loc[node]['node_class']]['primary_color'])

        # Set fig size 1920x1080 pixels
        plt.figure(figsize=(16, 9), dpi=120)
        plt.title("Layer: {0}".format(layer_name))
        # plt.figure(figsize=(16, 9), dpi=120)
        pos = nx_agraph.graphviz_layout(layer, prog='neato')
        draw(layer, node_color=color_map, pos=pos, with_labels=True)

        if save_to_disk:
            project_root_path = dirname(dirname(__file__))

            plt.savefig("{0}/results/{1}/{2}/{1}_{2}_{3}_layer".format(
                project_root_path, data_set_name, centrality_measure, layer_name))

        plt.show()


def plot_results_histograms(
        data_set_name,
        centrality_measure,
        results_data_frame,
        selected_columns,
        x_axis_label,
        y_axis_label,
        number_of_bins,
        step_size,
        save_to_disk=False
):
    """
    Plots the histograms for the selected columns.

    :param data_set_name: Name of the data set.
    :param centrality_measure: Name of the used centrality measure.
    :param results_data_frame: Dataframe containing all results.
    :param selected_columns: The selected columns for which the histograms are plotted.
    :param x_axis_label: String for the x axis histogram label
    :param y_axis_label: String for the y axis histogram label
    :param number_of_bins: Number of bins for the histogram.
    :param step_size: Step size for creating the bins.
    :param save_to_disk: Flag for enabling/disabling saving plots to disk.
    :return: void
    """

    bins = [i for i in range(0, number_of_bins * step_size + step_size, step_size)]

    results_data_frame_dict = results_data_frame.to_dict()

    for column_key in results_data_frame_dict.keys():
        if column_key in selected_columns:
            plt.title("{0}".format(column_key))
            plt.xlabel(x_axis_label)
            plt.ylabel(y_axis_label)
            plt.hist(list(results_data_frame_dict[column_key].values()),
                     bins, histtype='bar', edgecolor='black')

            if save_to_disk:
                project_root_path = dirname(dirname(__file__))

                plt.savefig("{0}/results/{1}/{2}/{1}_{2}_{3}_histogram".format(
                    project_root_path, data_set_name, centrality_measure, column_key))

            plt.show()


def save_results_data_frame(data_set_name, centrality_measure, results_data_frame):
    """
    Creates a .csv file containing all the results

    :param data_set_name: Name of the data set.
    :param centrality_measure: Name of the used centrality measure.
    :param results_data_frame: Dataframe containing all results.
    :return: void
    """

    project_root_path = dirname(dirname(__file__))

    results_data_frame.to_csv('{0}/results/{1}/{2}/{1}_{2}_results.csv'.format(
        project_root_path, data_set_name, centrality_measure), encoding='utf-16')

    print(results_data_frame)
