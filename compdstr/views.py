from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
# Create your views here.

from tools import views as toolsviews
from predictorder import views as previews
import time
import datetime
import json
import collections
from numpy import *

def index (request):
    menu = ['商圈1', '商圈2','商圈3','商圈4']
    return render_to_response ('compdstr/index.html', {'menu':menu},
                               context_instance = RequestContext (request))

def changeData (request):
    menu = ['商圈1', '商圈2','商圈3','商圈4']
    return render_to_response ('compdstr/change.html', {'menu':menu},
                               context_instance = RequestContext (request))

def getChangeData (request):
    shopid = request.session.get ('shopid', 256365)
    menu = ['商圈1', '商圈2','商圈3','商圈4']
    now = previews.nnow()
    before = (now - datetime.timedelta(days=7))
    res = toolsviews.QueryRestaurantOrders(shopid,before,now)
    data = collections.OrderedDict()
    for i in range (7):
        t = (now - datetime.timedelta(days=7-i)).strftime("%m-%d")
        data[t] = 0

    for x in res:
        timeStamp = x.order_time
        t = timeStamp.strftime("%m-%d")
        for v in x.foods:
            data[t] = data.get (t, 0) + 1

    response_data = {}
    response_data['dates'] = []
    response_data['values'] = []
    for k, v in data.items():
        response_data['dates'].append (k)
        response_data['values'].append (v)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def getWeidData (request):
    shopid = request.GET.get ('shopid', 256365)
    now = previews.nnow()
    res1 = toolsviews.QueryRestaurantOrders(shopid, now-datetime.timedelta(days=7), now)
    data1 = []
    for x in res1:
        data1.append ([x.longitude, x.latitude])
    cent, clus = toolsviews.KMeans (mat(data1), 5)

    geocoor1 = {}
    for i, x in enumerate(cent):
        print (x)
        geocoor1['商圈'+str(i)] = [x[0], x[1]]
    weid = []

    for i in range (len(cent)):
        weid.append ({'name':'商圈' + str(i), 'value': 0})
    for x in clus:
        t = int(x[0, 0])
        weid[t]['value'] += 1
    for i in range (len(cent)):
        weid[i]['value'] /= len (clus)
    al = {'a':geocoor1, 'b': weid}
    return HttpResponse(json.dumps(weid), content_type="application/json")

def getShopData (request):
    shopid = request.GET.get ('shopid', 256365)
    now = previews.nnow()
    res1 = toolsviews.QueryRestaurantOrders(shopid, now-datetime.timedelta(days=7), now)
    data1 = []
    for x in res1:
        data1.append ([x.longitude, x.latitude])
    cent, clus = toolsviews.KMeans (mat(data1), 5)

    geocoor1 = {}
    for i, x in enumerate(cent):
        print (x)
        geocoor1['商圈'+str(i)] = [x[0], x[1]]
    weid = []

    for i in range (len(cent)):
        weid.append ({'name':'商圈' + str(i), 'value': 0})
    for x in clus:
        t = int(x[0, 0])
        weid[t]['value'] += 1
    for i in range (len(cent)):
        weid[i]['value'] /= len (clus)
    al = {'a':geocoor1, 'b': weid}
    print (geocoor1)
    return HttpResponse(json.dumps(geocoor1), content_type="application/json")


