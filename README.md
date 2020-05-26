# Agglomerative Hierarchical Clustering
This assignment aims to familiarize you with the mechanism of two widely-used clustering methods: AGNES (a single-link based agglomerative nesting) algorithms.


For AGNES, you are asked to employ the hierarchical clustering algorithm to cluster N data points into k clusters. In other words, you shall always compute the agglomerative clustering via single linkage, and then stop the clustering when number of clusters reaches k, where k < N.

For AGNES, the input shall comprise of N points. The points are 0-indexed. In the absence of external clusters in case of AGNES, we shall assign cluster-id to a cluster of points as the minimum index of the points in the cluster. For example, if a cluster is composed of points {2, 3, 8, 9}, the cluster-id of the above group of nodes will be 2.

## Model Specification

**The following design choice in implementation purely aims to ease auto- grading on HackerRank.** Since we are to use HackerRank for grading, we have to eliminate additional random- ness and generate the deterministic results. We therefore enforce the following rule in this assignment:
- For AGNES, we resolve the ties when merging two clusters using their cluster-ids. For example, consider two separate cluster pairs P1 = (c1,c2) and P2 = (c3,c4) that have the the same link separation i.e. distance between c1 and c2 is same as that between c3 and c4. We shall choose the smaller pair to combine in this case. We define the smaller pair by the following rule:
    - if min(c1, c2) < min(c3, c4), then P1 is smaller
    - if min(c1, c2) == min(c3, c4) and max(c1, c2) < max(c3, c4), then P1 is smaller else P2 is smaller.
    
For example, if P1 = (0,2) and P2 = (1,2), then P1 is smaller. If P1 = (0,2) and P2 = (0,1), then P2 is smaller.

## Input Format and Sample
We ensure that the labels for N input points and k cluster are named by **non-negative
integer** following zero-based numbering.

The first line of input will be N and k (space in between). This will be followed by N input points where the points co-ordinates are space separated. The data type of the input points is floating number. The k initial cluster points for shall follow the input points.

    10 2
    8.98320053625 -2.08946304844 
    2.61615632899 9.46426282022 
    1.60822068547 8.29785986996 
    8.64957587261 -0.882595891607 
    1.01364234605 10.0300852081 
    1.49172651098 8.68816850944 
    7.95531802235 -1.96381815529 
    0.527763520075 9.22731148332 
    6.91660822453 -3.2344537134 
    6.48286208351 -0.605353440895
    
In this example the goal of the clustering task is to find the groups among 10 data points.

## Output Format and Sample
The output is the clustering results on the provided data made by AGNES. For each method, print the cluster-id corresponding to each point on separate lines.

As an example, the outputs of the toy example are as follows. For AGNES, the sample output is:

    1 
    0 
    0 
    1 
    0 
    0 
    1 
    0 
    1 
    1