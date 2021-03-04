import matplotlib.pyplot as plt
from seaborn import lmplot
from pandas import DataFrame, Series
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from uunet.multinet import read, vertices, to_nx_dict
from utils.layer_centrality import compute_multinet_layer_centrality


def compute_clusters(targetsShapleyValueDict, numberOfPCs, numberOfClusters):
    targets_df = DataFrame.from_dict(targetsShapleyValueDict).T
    # Normalise data
    targetsDF = StandardScaler().fit_transform(targets_df)
    clusterLables = computeKMeans(targetsDF, numberOfPCs, numberOfClusters)
    targets_df['Cluster Class'] = Series(clusterLables, index=targets_df.index)
    return targets_df


def computePCA(targetsDF, numberOfPCs):
    pca = PCA(n_components=numberOfPCs)
    principalComponents = pca.fit_transform(targetsDF)

    return DataFrame(principalComponents)


def testPCA(targetsShapleyValueDict):
    targets_df = DataFrame.from_dict(targetsShapleyValueDict).T
    # Normalise data
    targetsDF = StandardScaler().fit_transform(targets_df)
    pca = PCA(n_components=len(targetsDF[1]))
    pca.fit_transform(targetsDF)

    # Plotting the variances for each PC
    features = range(1, pca.n_components_ + 1)
    plt.bar(features, pca.explained_variance_ratio_, color='gold')
    plt.xlabel('Principal Components')
    plt.ylabel('Variance %')
    plt.xticks(features)
    plt.show()


def computeKMeans(targetsDF, numberOfPCs=1, nubmerOfClusters=1):
    principalComponents = computePCA(targetsDF, numberOfPCs)

    model = KMeans(n_clusters=nubmerOfClusters)
    clusterLabels = model.fit(principalComponents)
    model.predict(principalComponents)

    plotData = [["x", "y", "Cluster Class"]]
    for i in range(len(clusterLabels.labels_)):
        plotData.append([
            principalComponents[0][i],
            principalComponents[1][i],
            clusterLabels.labels_[i]]
        )

    plotDataDF = DataFrame(plotData, columns=plotData.pop(0))

    lmplot(data=plotDataDF, x='x', y='y', hue='Cluster Class', fit_reg=False, legend=True, legend_out=True)
    plt.show()
    '''
    plt.scatter(principalComponents[0], principalComponents[1], c=clusterLabels.labels_)
    plt.show()
    '''



    return clusterLabels.labels_


# Used for 'elbow rule'
def testNumberOfClusters(targetsShapleyValueDict, numberOfPCs, maxNumberOfClusters):
    targets_df = DataFrame.from_dict(targetsShapleyValueDict).T
    # Normalise data
    targetsDF = StandardScaler().fit_transform(targets_df)
    principalComponents = computePCA(targetsDF, numberOfPCs)
    inertias = []

    # Creating 10 K-Mean models while varying the number of clusters (k)
    for k in range(1, maxNumberOfClusters):
        model = KMeans(n_clusters=k)

        # Fit model to samples
        model.fit(principalComponents)

        # Append the inertia to the list of inertias
        inertias.append(model.inertia_)

    plt.plot(range(1, maxNumberOfClusters), inertias, '-p', color='gold')
    plt.xlabel('number of clusters, k')
    plt.ylabel('inertia')
    plt.show()


if __name__ == "__main__":
    multilayeredNetwork = read("../resources/test.txt")
    nodeList = sorted(set(vertices(multilayeredNetwork)["actor"]))
    layers = to_nx_dict(multilayeredNetwork)
    targetsShapleyValueDict = compute_multinet_layer_centrality(layers, nodeList)
    # testPCA(targetsShapleyValueDict)
    # testNumberOfClusters(targetsShapleyValueDict, 2, len(targetsShapleyValueDict))
    targetsClusterDataFrame = compute_clusters(targetsShapleyValueDict, 2, 3)
    print(targetsClusterDataFrame)
