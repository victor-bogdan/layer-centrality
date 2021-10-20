import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from uunet.multinet import to_nx_dict, flatten, layers
from networkx import draw, nx_agraph
from pandas import set_option, ExcelWriter
from os.path import dirname
from utils.LayerCentralityExcelModel import LayerCentralityExcelModel

# Module scope settings

# Pandas settings
set_option('display.width', 1000)
set_option('max.columns', 20)

"""
Dictionary containing settings for each class of layer influence.
"""
LAYER_INFLUENCE_CLASS_SETTINGS_DICT = {
    1: {'min_centrality_value': 75, 'node_color': '#DD3827', 'xlsx_format': {'bg_color': '#DD3827'}},
    2: {'min_centrality_value': 50, 'node_color': '#EFA811', 'xlsx_format': {'bg_color': '#EFA811'}},
    3: {'min_centrality_value': 30, 'node_color': '#F7F304', 'xlsx_format': {'bg_color': '#F7F304'}},
    4: {'min_centrality_value': 0, 'node_color': '#2CC82E', 'xlsx_format': {'bg_color': '#2CC82E'}}
}


def get_layer_influence_class(layer_centrality):
    """
    Returns the layer influence class based on the given :param layer_centrality.

    :param layer_centrality: Layer centrality for a node in a multilayered network.
    :return: Integer representing layer influence class.
    """

    for layer_influence_class in LAYER_INFLUENCE_CLASS_SETTINGS_DICT.keys():
        if layer_centrality >= LAYER_INFLUENCE_CLASS_SETTINGS_DICT[layer_influence_class]['min_centrality_value']:
            return layer_influence_class


def draw_results_layers(
        data_set_name,
        centrality_measure,
        multilayered_network,
        nodes_layer_centrality_dict,
        save_to_disk=False
):
    """
    Plots all layers in the given multilayered network and applies the settings for each node based on
    its layer influence class.

    :param data_set_name: Name of the data set.
    :param centrality_measure: Name of the used centrality measure.
    :param multilayered_network: Multilayered network.
    :param nodes_layer_centrality_dict: Dictionary of dictionaries containing the centrality of
    each layer for a set of nodes.
    :param save_to_disk: Flag for enabling/disabling saving plots to disk.
    :return: void
    """

    layer_dict = to_nx_dict(multilayered_network)

    for layer_name in layer_dict.keys():
        layer = layer_dict[layer_name]

        color_map = []

        for node in layer:
            layer_influence_class = get_layer_influence_class(nodes_layer_centrality_dict[node][layer_name])
            color_map.append(LAYER_INFLUENCE_CLASS_SETTINGS_DICT[layer_influence_class]['node_color'])

        # Construct plot legend
        legend_circles = []
        legend_labels = []

        for layer_influence_class in LAYER_INFLUENCE_CLASS_SETTINGS_DICT.keys():
            legend_circles.append(Line2D([0], [0], color='w', marker='o', markerfacecolor=
                LAYER_INFLUENCE_CLASS_SETTINGS_DICT[layer_influence_class]['node_color'], markersize=12))
            legend_labels.append('Layer influence > {0}%'.format(
                LAYER_INFLUENCE_CLASS_SETTINGS_DICT[layer_influence_class]['min_centrality_value']))

        # Set fig size 1920x1080 pixels
        plt.figure(figsize=(16, 9), dpi=120)
        plt.title("Layer: {0}".format(layer_name), fontdict={'size': 22})

        pos = nx_agraph.graphviz_layout(layer, prog='neato')

        draw(layer, node_color=color_map, pos=pos, with_labels=True)

        plt.legend(legend_circles, legend_labels)

        if save_to_disk:
            project_root_path = dirname(dirname(__file__))

            plt.savefig("{0}/results/{1}/{2}/{1}_{2}_{3}_layer".format(
                project_root_path, data_set_name, centrality_measure, layer_name))

        plt.show()


def draw_flattened_network_clustering_results(
        data_set_name,
        centrality_measure,
        multilayered_network,
        nodes_cluster_label_dict,
        save_to_disk=False
):
    """
    Plots the flattened network, obtained from :param multilayered_network with each node colored
    according to its cluster class. Cluster classes should be integers and start from 0.

    :param data_set_name: Name of the data set.
    :param centrality_measure: Name of the used centrality measure.
    :param multilayered_network: Multilayered network.
    :param nodes_cluster_label_dict: Dictionary containing nodes and their cluster classes.
    :param save_to_disk: Flag for enabling/disabling saving plots to disk.
    """

    cluster_colors = ['#00FFFF', '#FFD700', '#00FF00', '#B34D4D', '#0000FF',
                      '#D316C8', '#FF0000', '#065535', '#99FF99', '#999966']

    flatten(multilayered_network, 'flattened_network', layers(multilayered_network))

    flattened_network = to_nx_dict(multilayered_network)['flattened_network']

    color_map = []

    for node in flattened_network:
        color_map.append(cluster_colors[(nodes_cluster_label_dict[node])])

    # Construct plot legend
    legend_circles = []
    legend_labels = []

    for cluster_class in set(nodes_cluster_label_dict.values()):
        legend_circles.append(Line2D([0], [0], color='w', marker='o',
                                     markerfacecolor=cluster_colors[cluster_class], markersize=12))
        legend_labels.append('Cluster class {0}'.format(cluster_class))

    # Set fig size 1920x1080 pixels
    plt.figure(figsize=(16, 9), dpi=120)
    plt.title(data_set_name.capitalize())

    pos = nx_agraph.graphviz_layout(flattened_network, prog='neato')

    draw(flattened_network, node_color=color_map, pos=pos, with_labels=True)

    plt.legend(legend_circles, legend_labels)

    if save_to_disk:
        project_root_path = dirname(dirname(__file__))

        plt.savefig("{0}/results/{1}/{2}/{1}_{2}_flattened_network_clusters".format(
            project_root_path, data_set_name, centrality_measure))

    plt.show()


def draw_network_clustering_results(
        data_set_name,
        network_name,
        network,
        nodes_cluster_label_dict,
        save_to_disk=False
):
    """
    Plots the flattened network with each node colored according to its cluster class. Cluster classes
    should be integers and start from 0.

    :param data_set_name: Name of the data set.
    :param network_name: Name of the network.
    :param network: Networkx network class.
    :param nodes_cluster_label_dict: Dictionary containing nodes and their cluster classes.
    :param save_to_disk: Flag for enabling/disabling saving plots to disk.
    """

    cluster_colors = ['#00FFFF', '#FFD700', '#00FF00', '#B34D4D', '#0000FF',
                      '#D316C8', '#FF0000', '#065535', '#99FF99', '#999966']

    color_map = []

    for node in network:
        color_map.append(cluster_colors[(nodes_cluster_label_dict[node])])

    # Construct plot legend
    legend_circles = []
    legend_labels = []

    for cluster_class in set(nodes_cluster_label_dict.values()):
        legend_circles.append(Line2D([0], [0], color='w', marker='o',
                                     markerfacecolor=cluster_colors[cluster_class], markersize=12))
        legend_labels.append('Cluster class {0}'.format(cluster_class))

    # Set fig size 1920x1080 pixels
    plt.figure(figsize=(16, 9), dpi=120)
    plt.title("Network: {0}".format(network_name))

    pos = nx_agraph.graphviz_layout(network, prog='neato')

    draw(network, node_color=color_map, pos=pos, with_labels=True)

    plt.legend(legend_circles, legend_labels)

    if save_to_disk:
        project_root_path = dirname(dirname(__file__))

        plt.savefig("{0}/results/{1}/community_clustering/{1}_{2}_clusters".format(
            project_root_path, data_set_name, network_name))

    # plt.show()


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
            plt.title("{0} dataset".format(column_key))
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


def save_layer_centrality_excel_models_as_xlsx(
        data_set_name,
        centrality_measure,
        dataframe_excel_model_list
):
    """
    Creates a .xslx file containing all the results.

    :param data_set_name: Name of the data set.
    :param centrality_measure: Name of the used centrality measure.
    :param dataframe_excel_model_list: List containing object of type LayerCentralityExcelModel.
    :return: void
    """

    project_root_path = dirname(dirname(__file__))

    writer = ExcelWriter('{0}/results/{1}/{2}/{1}_{2}_results.xlsx'.format(
        project_root_path, data_set_name, centrality_measure), engine='xlsxwriter')

    workbook = writer.book

    for dataframe_excel_model in dataframe_excel_model_list:
        dataframe_excel_model.dataframe.to_excel(writer, dataframe_excel_model.sheet_title)
        worksheet = writer.sheets[dataframe_excel_model.sheet_title]

        for layer_influence_class in LAYER_INFLUENCE_CLASS_SETTINGS_DICT.keys():
            # TODO Only once!
            temp_format = workbook.add_format(LAYER_INFLUENCE_CLASS_SETTINGS_DICT[layer_influence_class]['xlsx_format'])

            worksheet.conditional_format(
                dataframe_excel_model.start_row,
                dataframe_excel_model.start_col,
                dataframe_excel_model.end_row,
                dataframe_excel_model.end_col,
                {
                    'type': 'cell',
                    'criteria': '>=',
                    'value': LAYER_INFLUENCE_CLASS_SETTINGS_DICT[layer_influence_class]['min_centrality_value'],
                    'format': temp_format
                }
            )

    writer.save()


def save_results_analysis_data_frames_as_xlsx(
        data_set_name,
        centrality_measure,
        results_analysis_data_frame_list
):
    """
    Saves a list of data frames containing analysis of the results as a xlsx document with multiple
    sheets

    :param data_set_name: Name of the data set.
    :param centrality_measure: Name of the used centrality measure.
    :param results_analysis_data_frame_list: List containing data frames with the results analysis
    :return: void
    """

    project_root_path = dirname(dirname(__file__))

    writer = ExcelWriter('{0}/results/{1}/{2}/{1}_{2}_results_analysis.xlsx'.format(
        project_root_path, data_set_name, centrality_measure), engine='xlsxwriter')

    for results_analysis_data_frame in results_analysis_data_frame_list:
        results_analysis_data_frame.to_excel(writer, results_analysis_data_frame.columns.name)

    writer.save()


def get_layer_centrality_excel_models(results_dataframe, cluster_labels=None):
    """
    Return a list containing object of type LayerCentralityExcelModel

    :param results_dataframe: Results DataFrame.
    :param cluster_labels: Cluster Labels.
    :return: List of LayerCentralityExcelModel objects.
    """

    excel_model_list = []

    results_dataframe_copy = results_dataframe.copy()

    results_dataframe_excel_model = LayerCentralityExcelModel(
        "Layer Centrality", results_dataframe_copy, 1, 1, len(results_dataframe_copy) - 1, 5)

    excel_model_list.append(results_dataframe_excel_model)

    if cluster_labels is None:
        cluster_labels = []

    for cluster_label in cluster_labels:
        cluster_dataframe = results_dataframe_copy.loc[results_dataframe_copy['cluster_class'] == cluster_label].copy()
        cluster_dataframe.loc['mean'] = cluster_dataframe.mean()

        excel_model = LayerCentralityExcelModel('cluster_{0}'.format(cluster_label),
                                                cluster_dataframe, 1, 1, len(cluster_dataframe) - 1, 5)

        excel_model_list.append(excel_model)

    return excel_model_list


def get_max_layer_contribution(layer_name_list, results_data_frame):
    max_layer_contribution_dict = {}

    for layer_name in layer_name_list:
        max_layer_contribution_dict[layer_name] = results_data_frame[layer_name].max()

    return max_layer_contribution_dict


def get_min_layer_contribution(layer_name_list, results_data_frame):
    max_layer_contribution_dict = {}

    for layer_name in layer_name_list:
        max_layer_contribution_dict[layer_name] = results_data_frame[layer_name].min()

    return max_layer_contribution_dict


def get_number_of_layer_most_influenced_nodes(layer_name_list, results_data_frame):
    layer_most_influenced_nodes_dict = {}

    node_most_influential_layer_list = results_data_frame.idxmax(axis=1)

    for layer_name in layer_name_list:
        layer_most_influenced_nodes_dict[layer_name] = sum(node_most_influential_layer_list == layer_name)

    return layer_most_influenced_nodes_dict
