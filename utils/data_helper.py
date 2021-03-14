import matplotlib.pyplot as plt
from uunet.multinet import vertices
from uunet.multinet import to_nx_dict
from networkx import draw
from os.path import dirname


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


def draw_all_layers(
        data_set_name,
        multilayered_network,
        save_to_disk=False
):
    """
    Plots all layers in the multilayered network.

    :param data_set_name: Name of the data set.
    :param multilayered_network: Multilayered network.
    :param save_to_disk: Flag for enabling/disabling saving plots to disk.
    :return: void
    """

    layers = to_nx_dict(multilayered_network)

    for layer_name in layers.keys():
        plt.title("Layer: {0}".format(layer_name))
        draw(layers[layer_name], with_labels=True)
        plt.draw()
        plt.show()

        if save_to_disk:
            project_root_path = dirname(dirname(__file__))

            plt.savefig("{0}/results/{1}/{1}_{2}_layer".format(project_root_path, data_set_name, layer_name))
