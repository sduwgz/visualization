from django.shortcuts import render, render_to_response

from django.http import HttpResponse
from django.template import RequestContext
from tools import views as toolsviews
from predictorder import views as previews
import time
import datetime
import json
import collections
from numpy import *

# Create your views here.


def index (request):
    return render_to_response ('analy/index.html', {},
                               context_instance = RequestContext (request))
