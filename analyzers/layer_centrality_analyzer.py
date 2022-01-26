from enum import Enum
from pandas import DataFrame
from uunet.multinet import data, vertices, to_nx_dict
from algo.core.layer_centrality import compute_multinet_layer_centrality
from utils.centrality_helpers import DegreeCentralityHelper, HarmonicCentralityHelper, \
    KatzCentralityHelper, SubgraphCentralityHelper


class CentralityMeasure(Enum):
    Degree = 1,
    Harmonic = 2,
    Katz = 3,
    Subgraph = 4


class CentralityAnalyzer:

    def __init__(self):
        self.nodes_layer_centrality_dict = {}
        self.results_data_frame = DataFrame.from_dict(self.nodes_layer_centrality_dict)

    def get_layer_centrality(self, centrality_measure):
        multilayered_network = data("aucs")
        node_list = sorted(set(vertices(multilayered_network)["actor"]))
        nx_layer_dict = to_nx_dict(multilayered_network)

        if centrality_measure == CentralityMeasure.Degree:
            centrality_helper = DegreeCentralityHelper(nx_layer_dict)
        elif centrality_measure == CentralityMeasure.Harmonic:
            centrality_helper = HarmonicCentralityHelper(nx_layer_dict)
        elif centrality_measure == CentralityMeasure.Katz:
            centrality_helper = KatzCentralityHelper(nx_layer_dict)
        elif centrality_measure == CentralityMeasure.Subgraph:
            centrality_helper = SubgraphCentralityHelper(nx_layer_dict)
        else:
            return self.results_data_frame

        self.nodes_layer_centrality_dict = compute_multinet_layer_centrality(
            nx_layer_dict, node_list, centrality_helper)

        self.results_data_frame = DataFrame.from_dict(self.nodes_layer_centrality_dict).T.sort_index(axis=1)

        self.results_data_frame = self.results_data_frame.round(2)

        return self.results_data_frame
