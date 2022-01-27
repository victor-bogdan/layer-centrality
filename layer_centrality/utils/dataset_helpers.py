from uunet.multinet import data, vertices, to_nx_dict


UUNET_DATASETS = ["aucs"]


class DatasetHelper:

    def __init__(self, dataset_name):
        self.__load_dataset(dataset_name)

    # TODO support external datasets loading
    def __load_dataset(self, dataset_name):
        self.__multilayered_network = data(dataset_name)
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
        return set([tuple(sorted(i)) for i in node_edges])
