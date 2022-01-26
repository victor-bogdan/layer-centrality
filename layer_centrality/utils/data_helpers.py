import matplotlib.pyplot as plt
from networkx import degree
from uunet.multinet import vertices, to_nx_dict
from networkx import draw, nx_agraph, neighbors
from os.path import dirname


def get_node_connections_on_layers(layers_dict, node):
    """

    :param layers_dict: Dictionary containing networkx layers.
    :param node: String representing a node.
    :return: Dictionary containing all nodes connected to the given node on all layers in
    :param layers_dict as sets.
    """

    node_layer_connections_dict = {}

    for layer in layers_dict.keys():
        if layers_dict[layer].has_node(node):
            node_layer_connections_dict[layer] = set([n for n in neighbors(layers_dict[layer], node)])

    return node_layer_connections_dict


def print_node_layers(node, multilayered_network):
    """
    Prints all the layers on which the node is present

    :param node: String representing the node in the multilayered network.
    :param multilayered_network: Multinet multilayered network.
    :return:
    """

    test_dict = dict(zip(vertices(multilayered_network)["actor"], vertices(multilayered_network)["layer"]))

    for key in test_dict.keys():
        if key == node:
            print(key, test_dict[key])


def draw_layers(
        data_set_name,
        multilayered_network,
        save_to_path=""
):
    """
    Plots all layers in the given multilayered network.

    :param data_set_name: Name of the data set.
    :param multilayered_network: Multilayered network.
    :param save_to_path: Disk path for saving the plots.
    :return: void
    """

    layers = to_nx_dict(multilayered_network)

    for layer_name in layers.keys():
        layer = layers[layer_name]

        # Set fig size 1920x1080 pixels
        plt.figure(figsize=(16, 9), dpi=120)
        plt.title("Layer: {0}".format(layer_name), fontdict={'size': 22})
        pos = nx_agraph.graphviz_layout(layer, prog='neato')
        draw(layer, pos=pos, with_labels=True)
        plt.draw()

        if save_to_path != "":
            plt.savefig("{0}/{1}/{1}_{2}_layer".format(save_to_path, data_set_name, layer_name))

        plt.show()


def get_layer_total_number_of_nodes(multilayered_network):

    layers = to_nx_dict(multilayered_network)

    layer_number_of_nodes_dict = {}

    for layer_name in layers.keys():
        layer = layers[layer_name]

        layer_number_of_nodes_dict[layer_name] = layer.number_of_nodes()

    return layer_number_of_nodes_dict


def get_layer_total_number_of_edges(multilayered_network):

    layers = to_nx_dict(multilayered_network)

    layer_number_of_nodes_dict = {}

    for layer_name in layers.keys():
        layer = layers[layer_name]

        layer_number_of_nodes_dict[layer_name] = layer.number_of_edges()

    return layer_number_of_nodes_dict


def get_layer_most_connected_node(multilayered_network):

    layers = to_nx_dict(multilayered_network)

    layer_number_of_nodes_dict = {}

    for layer_name in layers.keys():
        layer = layers[layer_name]

        layer_number_of_nodes_dict[layer_name] = max([val for (node, val) in degree(layer)])

    return layer_number_of_nodes_dict


def get_layer_number_of_isolated_nodes(multilayered_network):

    layers = to_nx_dict(multilayered_network)

    layer_number_of_nodes_dict = {}

    for layer_name in layers.keys():
        layer = layers[layer_name]

        number_of_isolated_nodes = 0

        degree_view = degree(layer)

        for degree_tuple in degree_view:
            if degree_tuple[1] == 1:
                number_of_isolated_nodes += 1

        layer_number_of_nodes_dict[layer_name] = number_of_isolated_nodes

    return layer_number_of_nodes_dict
