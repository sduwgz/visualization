from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
import json

from pyes import *
import time
import datetime
from numpy import *  
import matplotlib.pyplot as plt  
# Create your views here.


def index (request):
    menu = ['o1', 'o2', 'o3']
    return render_to_response ('compdstr/index.html', {'menu':menu},
                               context_instance = RequestContext (request))

conn_restaurant = ES('http://115.159.157.35:9200/hackathon/restaurant')

conn_order = ES('http://115.159.157.35:9200/hackathon/order')

conn_menu = ES('http://115.159.157.35:9200/hackathon/menu')

def _QueryMenu_init():
    q = MatchAllQuery()
    results = conn_menu.search(q, 'hackathon', 'menu')

    res = [];
    for r in results:
        res.append(r)
    return res

restaurant_menus = {}
for r in _QueryMenu_init():
    for r1 in r['menu']:
        for r2 in r1['foods']:
            restaurant_id = r2['restaurant_id']
            food_id = r2['food_id']
            food_name = r2['food_name']
            if restaurant_id in restaurant_menus:
                restaurant_menus[restaurant_id].update({food_id: food_name})
            else:
                restaurant_menus.update({restaurant_id:{food_id: food_name}})

def QueryMenu(restaurant_id):
    return restaurant_menus[restaurant_id]

def QueryRestaurantOrders(restaurant_id, time_start, time_end):
    start = str(time_start)
    print(start)
    end = str(time_end)
    print(end)
    q = TermQuery("restaurant_id", str(restaurant_id))
    results = conn_order.search(q, 'hackathon', 'order')

    res = [];
    start = time.mktime(time_start.timetuple())
    end = time.mktime(time_end.timetuple())
    for r in results:
        timeStamp = datetime.datetime.strptime(r[u'created_at'],'%Y-%m-%d %H:%M:%S') 
        mkTimeStamp = time.mktime(timeStamp.timetuple())
        if mkTimeStamp >= start and mkTimeStamp < end:
            res.append(r)
    return res

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
