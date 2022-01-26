from pandas import DataFrame
from uunet.multinet import data, vertices, to_nx_dict
from algo.core.layer_centrality import compute_multinet_layer_centrality
from utils.centrality_helpers import DegreeCentralityHelper, HarmonicCentralityHelper, \
    KatzCentralityHelper, SubgraphCentralityHelper
from utils.centrality_measure import CentralityMeasure


class AUCSCentralityAnalyzer:

    def __init__(self):
        self.__multilayered_network = data("aucs")
        self.__node_list = sorted(set(vertices(self.__multilayered_network)["actor"]))
        self.__nx_layer_dict = to_nx_dict(self.__multilayered_network)
        self.__nodes_layer_centrality_dict = {}
        self.__results_data_frame = DataFrame.from_dict(self.__nodes_layer_centrality_dict)

    def get_layer_centrality(self, centrality_measure):

        if centrality_measure == CentralityMeasure.Degree:
            centrality_helper = DegreeCentralityHelper(self.__nx_layer_dict)
        elif centrality_measure == CentralityMeasure.Harmonic:
            centrality_helper = HarmonicCentralityHelper(self.__nx_layer_dict)
        elif centrality_measure == CentralityMeasure.Katz:
            centrality_helper = KatzCentralityHelper(self.__nx_layer_dict)
        elif centrality_measure == CentralityMeasure.Subgraph:
            centrality_helper = SubgraphCentralityHelper(self.__nx_layer_dict)
        else:
            return self.__results_data_frame

        self.__nodes_layer_centrality_dict = compute_multinet_layer_centrality(
            self.__nx_layer_dict, self.__node_list, centrality_helper)

        self.__results_data_frame = DataFrame.from_dict(self.__nodes_layer_centrality_dict).T.sort_index(axis=1)

        self.__results_data_frame = self.__results_data_frame.round(2)

        return self.__results_data_frame
