from pandas import DataFrame
from layer_centrality.algo.core.layer_centrality import compute_multinet_layer_centrality
from layer_centrality.utils.centrality_helpers import DegreeCentralityHelper, HarmonicCentralityHelper, \
    KatzCentralityHelper, SubgraphCentralityHelper
from layer_centrality.utils.centrality_measure import CentralityMeasure


class LayerCentralityAnalyzer:

    def __init__(self, dataset_helper):
        self.__dataset_helper = dataset_helper
        self.__nodes_layer_centrality_dict = {}
        self.__results_data_frame = DataFrame.from_dict(self.__nodes_layer_centrality_dict)

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
