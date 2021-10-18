import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import neighbors
from algo.functions import js_divergence


class UncertainDBSCANHelper:

    def __init__(self, dataframe):
        self._dataframe = dataframe.copy()

    def uncertain_knn(self, alpha):
        """
        Computes the KNN using the Jensen-Shannon divergence and display a graph representing the
        "elbow rule".

        :param alpha: floating value used to avoid by 0 division in case q has probabilities with
        value 0.
        :return: void
        """

        dataframe = self._dataframe.copy()

        neighbours = neighbors.NearestNeighbors(n_neighbors=5, metric=js_divergence,
                                                metric_params={"alpha": alpha}).fit(dataframe)
        distances, indices = neighbours.kneighbors(dataframe)

        print("shape of distances matrix: " + str(distances.shape) + "\n")
        for enum, row in enumerate(distances[:5]):
            print("observation " + str(enum) + ": " + str([round(x, 5) for x in row]))

        dataframe['knn_farthest_dist'] = distances[:, -1]
        dataframe.head()

        dataframe.sort_values('knn_farthest_dist', ascending=False).reset_index()[['knn_farthest_dist']].plot()
        plt.xlabel("index")
        plt.ylabel("distance")
        plt.grid(True)
        plt.show()

    def uncertain_dbscan(self, eps, min_samples, alpha):
        """
        Computes Uncertain DBSCAN.

        :param eps: The maximum distance between two samples
        :param min_samples: The number of samples in a neighborhood for a point to be considered
        as a core point.
        :param alpha: floating value used to avoid by 0 division in case q has probabilities with
        value 0.
        :return: Cluster labels in order.
        """

        db = DBSCAN(eps=eps, min_samples=min_samples, metric=js_divergence,
                    metric_params={"alpha": alpha}).fit(self._dataframe.to_numpy())
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_

        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)

        print('Estimated number of clusters: %d' % n_clusters_)
        print('Estimated number of noise points: %d' % n_noise_)

        return labels
