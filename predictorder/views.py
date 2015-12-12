from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
import json
import time
import datetime

import collections

# Create your views here.

from compdstr import views as compviews

def index (request):
    shopid = request.GET.get ('shopid', 256365)
    dashid = request.GET.get ('dashid')
    request.session['shopid'] = shopid
    menu = getMenu (shopid)
    return render_to_response ('app1/predicttoday.html', {'menu':menu, 'dashid':dashid},
                               context_instance = RequestContext (request))

def predictOrder (request):
    menu = ['o1', 'o2', 'o3']
    return render_to_response ('app1/predicttoday.html', {'menu':menu},
                               context_instance = RequestContext (request))

def statisticOrder (request):
    shopid = request.GET.get ('shopid', 256365)
    dashid = request.GET.get ('dashid')
    request.session['shopid'] = shopid
    menu = getMenu (shopid)
    nowdash = ""
    if 'dashid' in request.GET:
        nowdash = request.GET['dashid']
    else:
        for k, v in menu.items ():
            nowdash = k
            break
    return render_to_response ('app1/statistic.html', {'menu':menu, 'dashid':nowdash},
                               context_instance = RequestContext (request))

def getOrderData (request):
    response_data = {}
    response_data['categories'] = []
    response_data['values'] = []
    for x in range(48):
        response_data['categories'].append (5)
        response_data['values'].append (6)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def getStatisticData (request):
    shopid = request.session.get ('shopid', 256365)
    nowdash = int(request.GET['dashid'])
    menu = getMenu (shopid)
    now = nnow()
    before = (now - datetime.timedelta(days=7))
    res = compviews.QueryRestaurantOrders(shopid,before,now)
    data = collections.OrderedDict()
    for i in range (7):
        t = (now - datetime.timedelta(days=7-i)).strftime("%m-%d")
        data[t] = 0

    for x in res:
        timeStamp = datetime.datetime.strptime(x['created_at'],'%Y-%m-%d %H:%M:%S')
        t = timeStamp.strftime("%m-%d")
        group = x['detail']['group']
        for va in group:
            for v in va:
                if v['id'] == nowdash:
                    data[t] = data.get (t, 0) + 1

    response_data = {}
    response_data['dates'] = []
    response_data['values'] = []
    for k, v in data.items():
        response_data['dates'].append (k)
        response_data['values'].append (v)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def nnow ():
    return datetime.datetime.strptime("2015-12-06 01:00:00",'%Y-%m-%d %H:%M:%S')

def getMenu (shopid):
    dic = compviews.QueryMenu (shopid)
    ans = collections.OrderedDict ()
    for k, v in dic.items ():
        ans[str(k)] = v
    return ans


