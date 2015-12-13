from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
import json
import time
import datetime

import collections

# Create your views here.

from tools import views as compviews

def index (request):
    shopid = request.GET.get ('shopid', 256365)
    dashid = request.GET.get ('dashid')
    request.session['shopid'] = shopid
    menu = getMenu (shopid)
    return render_to_response ('app1/predicttoday.html', {'menu':menu, 'dashid':dashid},
                               context_instance = RequestContext (request))

def predictOrder (request):
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
    return render_to_response ('app1/predicttoday.html', {'menu':menu, 'dashid':nowdash},
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
    shopid = request.session.get ('shopid', 256365)
    nowdash = int(request.GET['dashid'])
    menu = getMenu (shopid)
    now = nnow()
    if request.GET.get ('tomorrow', '0') == '1':
        now = now + datetime.timedelta(days=1)
    before = (now - datetime.timedelta(days=7))
    res = compviews.QueryRestaurantOrders(shopid,before,now)
    data = collections.OrderedDict()
    timeStamp = datetime.datetime.strptime("00:00",'%H:%M')
    for i in range (48):
        t = (timeStamp + datetime.timedelta(minutes=30*i)).strftime("%H:%M")
        data[t] = 0
    for x in res:
        timeStamp = x.order_time
        if timeStamp.strftime('%m%d') == before.strftime('%m%d'):
            t = timeStamp.strftime('%H') + ':'
            if int(timeStamp.strftime('%M')) >= 30:
                t += '30'
            else:
                t += '00'
            for v in x.foods:
                if v.food_id == nowdash:
                    data[t] = data.get (t, 0) + 1

    response_data = {}
    response_data['categories'] = []
    response_data['values'] = []
    for k, v in data.items():
        response_data['categories'].append (k)
        response_data['values'].append (v)
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
        timeStamp = x.order_time
        t = timeStamp.strftime("%m-%d")
        for v in x.foods:
            if v.food_id == nowdash:
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
    dic = compviews.QueryMenu (shopid)[::-1]
    ans = collections.OrderedDict ()
    for x in dic:
        ans[str(x.food_id)] = x.food_name
    return ans


