#!/usr/bin/env
"""
# Author: newSolar
# Created Time : Sat 12 Dec 2015 09:07:09 PM CST

# File Name: testKMeans.py
# Description:

"""

from numpy import *  
import time  
import matplotlib.pyplot as plt  
from KMeans import *
  
## step 1: load data  
dataSet = []  
fileIn = open('testSet.txt')  
for line in fileIn.readlines():  
    lineArr = line.strip().split()  
    dataSet.append([float(lineArr[0]), float(lineArr[1])])  
  
## step 2: clustering...  
dataSet = mat(dataSet)  
k = 4  
centroids, clusterAssment = KMeans(dataSet, k)  
  
## step 3: show the result  
showCluster(dataSet, k, centroids, clusterAssment)  
