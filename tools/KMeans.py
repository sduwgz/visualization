"""
# Author: newSolar
# Created Time : Sat 12 Dec 2015 09:06:11 PM CST

# File Name: KMeans.py
# Description:

"""
from numpy import *  
import time  
import matplotlib.pyplot as plt  
  
  
# calculate Euclidean distance  
def euclDistance(vector1, vector2):  
    return sqrt(sum(power(vector2 - vector1, 2)))  
  
# init centroids with random samples  
def initCentroids(dataSet, k):  
    numSamples, dim = dataSet.shape  
    centroids = zeros((k, dim))  
    for i in range(k):  
        index = int(random.uniform(0, numSamples))  
        centroids[i, :] = dataSet[index, :]  
    return centroids  
  
def KMeans(dataSet, k):  
    numSamples = dataSet.shape[0]  
    clusterAssment = mat(zeros((numSamples, 2)))  
    clusterChanged = True  
  
    ## step 1: init centroids  
    centroids = initCentroids(dataSet, k)  
  
    while clusterChanged:  
        clusterChanged = False  
        ## for each sample  
        for i in range(numSamples):  
            minDist  = -1 
            minIndex = 0  
            ## for each centroid  
            ## step 2: find the centroid who is closest  
            for j in range(k):  
                distance = euclDistance(centroids[j, :], dataSet[i, :])  
                if minDist < 0 or distance < minDist:  
                    minDist  = distance  
                    minIndex = j  
              
            ## step 3: update its cluster  
            if clusterAssment[i, 0] != minIndex:  
                clusterChanged = True  
                clusterAssment[i, :] = minIndex, minDist**2  
  
        ## step 4: update centroids  
        for j in range(k):  
            pointsInCluster = dataSet[nonzero(clusterAssment[:, 0].A == j)[0]]  
            centroids[j, :] = mean(pointsInCluster, axis = 0)  
  
    return centroids, clusterAssment  
  
def showCluster(dataSet, k, centroids, clusterAssment):  
    numSamples, dim = dataSet.shape  
    if dim != 2:  
        return 1  
  
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']  
    if k > len(mark):  
        return 1  
    for i in range(numSamples):  
        markIndex = int(clusterAssment[i, 0])  
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])  
  
    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']  
    for i in range(k):  
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize = 12)  
  
    plt.show() 

