from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
import json

# Create your views here.

def index (request):
    menu = ['o1', 'o2', 'o3']
    return render_to_response ('app1/predicttoday.html', {'menu':menu},
                               context_instance = RequestContext (request))

def predictOrder (request):
    menu = ['o1', 'o2', 'o3']
    return render_to_response ('app1/predicttoday.html', {'menu':menu},
                               context_instance = RequestContext (request))

def statisticOrder (request):
    menu = ['o1', 'o2', 'o3']
    return render_to_response ('app1/statistic.html', {'menu':menu},
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
    response_data = {}
    response_data['dates'] = []
    response_data['values'] = []
    for x in range(7):
        response_data['dates'].append (5)
        response_data['values'].append (6)
    return HttpResponse(json.dumps(response_data), content_type="application/json")
