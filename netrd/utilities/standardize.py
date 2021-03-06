"""
standardize.py
------------

Utilities for computing standardization values for distance measures.

author: Harrison Hartle/Tim LaRock
email: timothylarock at gmail dot com
Submitted as part of the 2019 NetSI Collabathon

"""

import numpy as np
import networkx as nx

def mean_GNP_distance(n, edge_probability, distance, samples=10, **kwargs):
    '''
    Compute the mean distance between _samples_ GNP graphs with
    parameters N=n,p=edge_probability using distance function _distance_,
    whose parameters are passed with **kwargs.

    NOTE: Ideally, each 'sample' would involve generating two GNP graphs,
    computing the distance between them, then throwing them both away.
    However, this will be computationally expensive, so for now we are
    reusing samples, but _not_ including distance between the same sample
    in the mean (e.g. excluding the diagonal of a distance matrix).

    Params
    ------

    n (int): Number of nodes in ER graphs to be generated
    edge_probability (float): Probability of edge in ER graphs to be generated.
    samples (int): Number of samples to average distance over.
    distance (function): Function from netrd.distances.<distance>.dist
    kwargs (dict): Keyword arguments to pass to the distance function.


    Returns
    -------

    mean (float): The average distance between the sampled ER networks.
    std (float): The standard deviation of the distances.
    dist (np.ndarray): Array storing the actual distances.

    Example
    -------
    dist_obj = netrd.distance.ResistancePerturbation()
    kwargs = {'p':2}
    mean, std, dists = netrd.utilities.mean_GNP_distance(100, 0.1, dist_obj.dist, **kwargs)

    '''
    # generate sample graphs
    a=[]
    for _ in range(samples):
       a.append(nx.fast_gnp_random_graph(n, edge_probability))

    # get distances
    dis_mat = np.zeros((samples,samples))
    dis_list = []
    for i in range(samples):
        for j in range(samples):
            # Do not compute distance between identical samples (see docstring)
            if i != j:
                dis[i,j]= distance(a[i], a[j], **kwargs)
                dis_list.append(dis[i,j])

    # get mean distances \ std distances
    mean_dist=np.mean(dis_list)
    std_dist=np.std(dis_list)

    return mean_dist, std_dist, dis_mat

