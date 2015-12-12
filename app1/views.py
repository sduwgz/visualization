from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
import json

# Create your views here.

def index (request):
    menu = ['o1', 'o2', 'o3']
    return render_to_response ('app1/predicttoday.html', {'menu':menu},
                               context_instance = RequestContext (request))

def getOrderData (request):
    response_data = {}
    response_data['categories'] = []
    response_data['values'] = []
    for x in range(48):
        response_data['categories'].append (5)
        response_data['values'].append (6)
    print (response_data['categories'])
  

#    response_data['categories'] = ['111', '222', '333', '444', '555', '666']
#    response_data['values'] = [5, 6, 3, 4, 7, 22]
    return HttpResponse(json.dumps(response_data), content_type="application/json")
