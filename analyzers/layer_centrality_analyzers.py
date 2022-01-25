from pandas import DataFrame
from uunet.multinet import data, vertices, to_nx_dict
from algo.core.layer_centrality import compute_multinet_layer_centrality
from utils.DegreeCentralityHelper import DegreeCentralityHelper
from utils.HarmonicCentralityHelper import HarmonicCentralityHelper
from utils.KatzCentralityHelper import KatzCentralityHelper
from utils.SubgraphCentralityHelper import SubgraphCentralityHelper


class DegreeCentralityAnalyzer:

    nodes_layer_centrality_dict = None

    def get_degree_layer_centrality(self):
        multilayered_network = data("aucs")
        node_list = sorted(set(vertices(multilayered_network)["actor"]))
        nx_layer_dict = to_nx_dict(multilayered_network)

        centrality_helper = DegreeCentralityHelper(nx_layer_dict)

        self.nodes_layer_centrality_dict = compute_multinet_layer_centrality(
            nx_layer_dict, node_list, centrality_helper)

        results_data_frame = DataFrame.from_dict(self.nodes_layer_centrality_dict).T.sort_index(axis=1)

        results_data_frame = results_data_frame.round(2)

        return results_data_frame


class HarmonicCentralityAnalyzer:

    nodes_layer_centrality_dict = None

    def get_degree_layer_centrality(self):
        multilayered_network = data("aucs")
        node_list = sorted(set(vertices(multilayered_network)["actor"]))
        nx_layer_dict = to_nx_dict(multilayered_network)

        centrality_helper = HarmonicCentralityHelper(nx_layer_dict)

        self.nodes_layer_centrality_dict = compute_multinet_layer_centrality(
            nx_layer_dict, node_list,centrality_helper)

        results_data_frame = DataFrame.from_dict(self.nodes_layer_centrality_dict).T.sort_index(axis=1)

        results_data_frame = results_data_frame.round(2)

        return results_data_frame


class KatzCentralityAnalyzer:

    nodes_layer_centrality_dict = None

    def get_degree_layer_centrality(self):
        multilayered_network = data("aucs")
        node_list = sorted(set(vertices(multilayered_network)["actor"]))
        nx_layer_dict = to_nx_dict(multilayered_network)

        centrality_helper = KatzCentralityHelper(nx_layer_dict)

        self.nodes_layer_centrality_dict = compute_multinet_layer_centrality(
            nx_layer_dict, node_list, centrality_helper)

        results_data_frame = DataFrame.from_dict(self.nodes_layer_centrality_dict).T.sort_index(axis=1)

        results_data_frame = results_data_frame.round(2)

        return results_data_frame


class SubgraphCentralityAnalyzer:

    nodes_layer_centrality_dict = None

    def get_degree_layer_centrality(self):
        multilayered_network = data("aucs")
        node_list = sorted(set(vertices(multilayered_network)["actor"]))
        nx_layer_dict = to_nx_dict(multilayered_network)

        centrality_helper = SubgraphCentralityHelper(nx_layer_dict)

        self.nodes_layer_centrality_dict = compute_multinet_layer_centrality(
            nx_layer_dict, node_list, centrality_helper)

        results_data_frame = DataFrame.from_dict(self.nodes_layer_centrality_dict).T.sort_index(axis=1)

        results_data_frame = results_data_frame.round(2)

        return results_data_frame

