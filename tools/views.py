from django.shortcuts import render

import json

from pyes import *
import time
import datetime
from numpy import *  
import matplotlib.pyplot as plt  
# Create your views here.

class food:
    def __init__(Self, foodid, foodname):
        Self.food_id = foodid
        Self.food_name = foodname

class user:
    def __init__(Self, t, longi, lati, addr):
        Self.order_time = t
        Self.longitude = longi
        Self.latitude = lati
        Self.foods = []
        Self.address = addr
    def add_food(Self,food_id, food_name):
        Self.foods.append(food(food_id, food_name))
class orders:
    def __init__(Self, rest_id):
        Self.restaurant_id = rest_id
        Self.user_infos = []

    def add_user_info(Self, userinfo):
        Self.user_infos.append(userinfo)

class menus:
    def __init__(Self, restid):
        Self.restaurant_id = restid
        Self.foods = []

    def add_food(Self, fo):
        Self.foods.append(fo)

class location:
    def __init__(Self, longi, lati):
        Self.longitude = longi
        Self.latitude = lati

restaurant_menus = {}
restaurant_orders = {}
restaurant_location = {}

f = open('/home/newsolar/gaofeng/api_menus.json')
s = json.load(f)
#print s
#print(len(s))

for r in s:
    for r1 in r:
        for r2 in r1['foods']:
            restaurant_id = r2['restaurant_id']

            r = restaurant_id
#            print (r)
            restaurant_menus[r] = (restaurant_menus.get(r, menus(r)))
            restaurant_menus[r].add_food( food(r2['food_id'],r2['food_name']))
f.close()

f = open('/home/newsolar/gaofeng/api_orders_preproc2.json')
s = json.load(f)

for r in s:
    timeStamp = datetime.datetime.strptime(r['created_at'],'%Y-%m-%d %H:%M:%S')
    i = r['restaurant_id']
    longi = r['longitude']
    lati = r['latitude']
    addr = r['address']
    restaurant_orders[i] = (restaurant_orders.get(i, orders(i)))
    userinfo = user(timeStamp,longi, lati, addr)
    for r2 in r['detail']['group'][0]:
        foodid = r2['id']
        foodname = r2['name']
        userinfo.add_food(foodid, foodname)
    restaurant_orders[i].add_user_info(userinfo)

#print(len(restaurant_orders))
f.close()

f = open('/home/newsolar/gaofeng/api_restaurants.json')
s = json.load(f)

for r in s:
    i = r['id']
    restaurant_location.update({i: location(r['longitude'], r['latitude'])})

f.close()


def QueryMenu(restaurant_id):
    return restaurant_menus[restaurant_id].foods

def QueryRestaurantOrders(restaurant_id, time_start, time_end):
    str_start = str(time_start)
    str_end = str(time_end)
    start = datetime.datetime.strptime(str_start,'%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.strptime(str_end,'%Y-%m-%d %H:%M:%S')

    mkstart = time.mktime(start.timetuple())
    mkend = time.mktime(end.timetuple())

    res = []
    for r in restaurant_orders[restaurant_id].user_infos:
        mkStamp = time.mktime(r.order_time.timetuple())
        if mkStamp >= mkstart and mkStamp < mkend:
            res.append(r)

    return res

def QueryRestaurantLocation(restaurant_id):
    return restaurant_location[restaurant_id]

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
