import matplotlib.pyplot as plt
from uunet.multinet import to_nx_dict
from networkx import draw, nx_agraph
from pandas import ExcelWriter
from os.path import dirname

"""
Dictionary containing settings for each class of nodes.
"""
NODE_CLASS_SETTINGS_DICT = {
    1: {'min_centrality_value': 75, 'node_color': '#DD3827', 'xlsx_format': {'bg_color': '#DD3827'}},
    2: {'min_centrality_value': 50, 'node_color': '#EFA811', 'xlsx_format': {'bg_color': '#EFA811'}},
    3: {'min_centrality_value': 30, 'node_color': '#F7F304', 'xlsx_format': {'bg_color': '#F7F304'}},
    4: {'min_centrality_value': 0, 'node_color': '#2CC82E', 'xlsx_format': {'bg_color': '#2CC82E'}}
}


def get_node_class(layer_centrality):
    """
    Returns the node class based on the layer centrality of the respective node in a multilayered
    network.

    :param layer_centrality: Maximum layer centrality for a node in a multilayered network
    :return: String representing node class
    """

    for node_class in NODE_CLASS_SETTINGS_DICT.keys():
        if layer_centrality >= NODE_CLASS_SETTINGS_DICT[node_class]['min_centrality_value']:
            return node_class


def draw_results_layers(
        data_set_name,
        centrality_measure,
        multilayered_network,
        nodes_layer_centrality_dict,
        save_to_disk=False
):
    """
    Plots all layers in the given multilayered network and applies the settings for each node based on
    its class.

    :param data_set_name: Name of the data set.
    :param centrality_measure: Name of the used centrality measure.
    :param multilayered_network: Multilayered network.
    :param nodes_layer_centrality_dict: Dictionary of dictionaries containing the centrality of
    each layer for a set of nodes.
    :param save_to_disk: Flag for enabling/disabling saving plots to disk.
    :return: void
    """

    layers = to_nx_dict(multilayered_network)

    for layer_name in layers.keys():
        layer = layers[layer_name]

        color_map = []

        for node in layer:
            node_class = get_node_class(nodes_layer_centrality_dict[node][layer_name])
            color_map.append(NODE_CLASS_SETTINGS_DICT[node_class]['node_color'])

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


def save_results_data_frame_as_csv(data_set_name, centrality_measure, results_data_frame):
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

    # print(results_data_frame)


def save_results_data_frame_as_xlsx(
        data_set_name,
        centrality_measure,
        results_data_frame,
        start_row,
        start_col,
        end_row,
        end_col
):
    """
    Creates a .xslx file containing all the results

    :param data_set_name: Name of the data set.
    :param centrality_measure: Name of the used centrality measure.
    :param results_data_frame: Dataframe containing all results.
    :param start_row: Row index from where the formatting rules start
    :param start_col: Column index from where the formatting rules start
    :param end_row: Row index from where the formatting rules end
    :param end_col: Column index from where the formatting rules end
    :return: void
    """

    project_root_path = dirname(dirname(__file__))

    writer = ExcelWriter('{0}/results/{1}/{2}/{1}_{2}_results.xlsx'.format(
        project_root_path, data_set_name, centrality_measure), engine='xlsxwriter')

    results_data_frame.to_excel(writer, "LayerCentrality")

    workbook = writer.book
    worksheet = writer.sheets['LayerCentrality']

    for node_class in NODE_CLASS_SETTINGS_DICT.keys():
        temp_format = workbook.add_format(NODE_CLASS_SETTINGS_DICT[node_class]['xlsx_format'])

        worksheet.conditional_format(
            start_row,
            start_col,
            end_row,
            end_col,
            {
                'type': 'cell',
                'criteria': '>=',
                'value': NODE_CLASS_SETTINGS_DICT[node_class]['min_centrality_value'],
                'format': temp_format
            }
        )

    writer.save()

    print(results_data_frame)
