from uunet.multinet import data, vertices, to_nx_dict


class AUCSDatasetHelper:

    def __init__(self):
        self.__multilayered_network = data("aucs")
        self.__node_list = sorted(set(vertices(self.__multilayered_network)["actor"]))
        self.__nx_layer_dict = to_nx_dict(self.__multilayered_network)

    def get_multilayered_network(self):
        return self.__multilayered_network

    def get_node_list(self):
        return self.__node_list

    def get_nx_layer_dict(self):
        return self.__nx_layer_dict

    def get_layer_names_list(self):
        return self.__nx_layer_dict.keys()

    def get_node_edges_for_layer(self, layer_name):
        node_edges = []
        layer_graph = self.__nx_layer_dict[layer_name]
        for node in self.__node_list:
            node_edges = node_edges + list(layer_graph.edges(node))
        return node_edges
