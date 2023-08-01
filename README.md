# FCM
In the first step in this algorithm, like K-Means, we specify the number of clusters we want to have. Then we randomly generate that number of initial cluster centroids. Next, we must do the following two things in a loop:

1. Finding which cluster (or clusters) each data belongs to.
2. Updating the center of the clusters based on their data.

We run this loop for example 100 times to make sure that the clusters are stable and do not change much.

For the first part, each cluster is viewed as a fuzzy set, therefore each data belongs to all clusters but with different amounts of membership. The membership function for the kth data in the ith cluster is calculated according to the following formula:

![image](https://github.com/MahdiTheGreat/FCM/assets/47212121/924dbceb-8e72-4890-ba1a-b985f116f844)


where X_k is the kth data, V is the set of clusters, v_i is the center of the ith cluster and m is a parameter in the interval [2,1) that must be specified in advance. In fact, the closer this value is to one, the closer we are to k-means clustering, and the fuzzy part of this algorithm will have less impact.

For the second part, We have to calculate the average of the points that belong to each cluster and consider it as the new center of the said cluster. Since all points are essentially members of all clusters with varying degrees of membership, we must take a weighted average, as seen in the formula below:

![image](https://github.com/MahdiTheGreat/FCM/assets/47212121/6bf4380d-8675-4776-81fe-934a294ed6f4)

In this way, those data that belong more to a cluster play a greater role in determining the center of that cluster; Which is logical.

# Cost function and how to choose the optimal number of centers

In the previous part, we said we should continue the loop until the clusters become stable. The question that arises is what does it mean to achieve stability and why should this happen? The point is that the two things we are doing in the loop are minimizing the following cost function behind the scenes:

![image](https://github.com/MahdiTheGreat/FCM/assets/47212121/47b5773b-756f-422c-918a-a57ca355e518)


That is, they are minimizing the distance of each data from the centers to which they belong to (in fact, taking the derivative of this function and setting it equal to zero will lead to the same two formulas as before). So we are solving an optimization problem in clustering with FCM and iteratively proceed to reach the minimum value.

The next point to consider is, what is the effect of the number of clusters on the cost function? If we run the algorithm for the number of different centers and plot the value of the cost function, we will have a diagram like this:

![image](https://github.com/MahdiTheGreat/FCM/assets/47212121/7ddf07e1-be20-4981-bae1-275376aaadd9)

As we can see, with the increase in the number of clusters, Cost is decreasing. This is logical because when the number of cluster centers increases, the data distance from these centers also decreases.
Now the question is how many centers should we have? There is no ideal way to choose the number of centers, But there are several methods that are usually used. One of them is the Elbow method, which tells us to plot the same chart above and choose the number of centers that will not significantly reduce the cost from then on. As a result, according to the above figure, three centers can be a suitable option.

# Implementation
We implement the C-Means algorithm and run it on the four datasets we have and plot the cost in terms of C or the number of centers for each dataset and determine the optimal number of clusters through the elbow method. Since the data belongs to all the clusters, as a result, we cannot easily consider a specific color for each cluster and show and plot the data belonging to that cluster with that color (in fact, to accurately display the clustering output as Fuzzy; we need to use color gradient). As a result, for a simple display of the output, We're bringing clusters and data back to the world of Crisp data and we only consider which cluster each data belongs to more than the other clusters and give it the color of that cluster.




