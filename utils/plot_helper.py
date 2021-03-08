import matplotlib.pyplot as plt
from uunet.multinet import to_nx_dict
from networkx import draw


def draw_all_layers(data_set_name, multilayered_network):
    """
    Plots all layers in the multilayered network.

    :param data_set_name: Name of the data set.
    :param multilayered_network: Multilayered network.
    :return: void
    """

    layers = to_nx_dict(multilayered_network)

    for layer_name in layers.keys():
        plt.title("Layer: {0}".format(layer_name))
        draw(layers[layer_name], with_labels=True)
        plt.draw()
        plt.savefig("./results/{0}/{0}_{1}_layer".format(data_set_name, layer_name))
        plt.show()
