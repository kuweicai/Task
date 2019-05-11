# base on scipy or scikit-learn
# import sklearn.datasets
# import sklearn.cluster
# import scipy.cluster.vq
# import matplotlib.pyplot as plot
#
# n = 100
# k = 3
#
# # Generate fake data
# data, labels = sklearn.datasets.make_blobs(n_samples=n, n_features=2, centers=k)
#
# # scipy
# means, _ = scipy.cluster.vq.kmeans(data, k, iter=300)
#
# # scikit-learn
# kmeans = sklearn.cluster.KMeans(k, max_iter=300)
# kmeans.fit(data)
# means = kmeans.cluster_centers_
#
# plot.scatter(data[:, 0], data[:, 1], c=labels)
# plot.scatter(means[:, 0], means[:, 1], linewidths=2)
# plot.show()

# base on python only
# k--numbers of cluster


import sklearn.datasets
import numpy as np
n = 100
k = 3


def k_means(data, k, number_of_iterations):
    n = len(data)
    number_of_features = data.shape[1]
    # Pick random indices for the initial centroids.
    initial_indices = np.random.choice(range(n), k)
    # We keep the centroids as |features| x k matrix.
    means = data[initial_indices].T
    # To avoid loops, we repeat the data k times depthwise and compute the
    # distance from each point to each centroid in one step in a
    # n x |features| x k tensor.
    repeated_data = np.stack([data] * k, axis=-1)
    all_rows = np.arange(n)
    zero = np.zeros([1, 1, 2])
    for _ in range(number_of_iterations):
        # Broadcast means across the repeated data matrix, gives us a
        # n x k matrix of distances.
        distances = np.sum(np.square(repeated_data - means), axis=1)
        # Find the index of the smallest distance (closest cluster) for each
        # point.
        assignment = np.argmin(distances, axis=-1)
        # Again to avoid a loop, we'll create a sparse matrix with k slots for
        # each point and fill exactly the one slot that the point was assigned
        # to. Then we reduce across all points to give us the sum of points for
        # each cluster.
        sparse = np.zeros([n, k, number_of_features])
        sparse[all_rows, assignment] = data
        # To compute the correct mean, we need to know how many points are
        # assigned to each cluster (without a loop).
        counts = (sparse != zero).sum(axis=0)
        # Compute new assignments.
        means = sparse.sum(axis=0).T / counts.clip(min=1).T
    return means.T


# Generate fake data
data, labels = sklearn.datasets.make_blobs(n_samples=n, n_features=2, centers=k)
print(k_means(data, 3, 100000))

