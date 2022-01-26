from pandas import DataFrame
from layer_centrality.algo.core.layer_centrality import compute_multinet_layer_centrality
from layer_centrality.utils.dataset_helpers import AUCSDatasetHelper
from layer_centrality.utils.centrality_helpers import DegreeCentralityHelper, HarmonicCentralityHelper, \
    KatzCentralityHelper, SubgraphCentralityHelper
from layer_centrality.utils.centrality_measure import CentralityMeasure
from layer_centrality.utils.result_helpers import get_layer_influence_class_node_color


class AUCSCentralityAnalyzer:

    def __init__(self):
        self.__dataset_helper = AUCSDatasetHelper()
        self.__nodes_layer_centrality_dict = {}
        self.__results_data_frame = DataFrame.from_dict(self.__nodes_layer_centrality_dict)

    def get_node_edges_for_layer(self, layer_name):
        return self.__dataset_helper.get_node_edges_for_layer(layer_name)

    def get_layer_centrality(self, centrality_measure):

        if centrality_measure == CentralityMeasure.Degree:
            centrality_helper = DegreeCentralityHelper(self.__dataset_helper.get_nx_layer_dict())
        elif centrality_measure == CentralityMeasure.Harmonic:
            centrality_helper = HarmonicCentralityHelper(self.__dataset_helper.get_nx_layer_dict())
        elif centrality_measure == CentralityMeasure.Katz:
            centrality_helper = KatzCentralityHelper(self.__dataset_helper.get_nx_layer_dict())
        elif centrality_measure == CentralityMeasure.Subgraph:
            centrality_helper = SubgraphCentralityHelper(self.__dataset_helper.get_nx_layer_dict())
        else:
            return self.__results_data_frame

        self.__nodes_layer_centrality_dict = compute_multinet_layer_centrality(
            self.__dataset_helper.get_nx_layer_dict(), self.__dataset_helper.get_node_list(), centrality_helper)

        self.__results_data_frame = DataFrame.from_dict(self.__nodes_layer_centrality_dict).T.sort_index(axis=1)

        self.__results_data_frame = self.__results_data_frame.round(2)

        return self.__results_data_frame

    def get_node_color(self, layer_centrality):
        return get_layer_influence_class_node_color(layer_centrality)
