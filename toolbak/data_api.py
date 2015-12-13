#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyes import *
import time
import datetime

conn_restaurant = ES('http://115.159.157.35:9200/hackathon/restaurant')

conn_order = ES('http://115.159.157.35:9200/hackathon/order')

conn_menu = ES('http://115.159.157.35:9200/hackathon/menu')
def QueryRestaurantTest(id):
    q = TermQuery("id",str(id))
    results = conn_restaurant.search(query = q)

    res = [];
    for r in results:
        res.append(r)
    return res

#results = QueryRestaurantTest(30586)
#for r in results:
#    print r

#def compare_time(l_time,start_t,end_t):
#    s_time = time.mktime(time.strptime(start_t,'%Y-%m-%d %H:%M:%S')) # get the seconds for specify date
#    e_time = time.mktime(time.strptime(end_t,'%Y-%m-%d %H:%M:%S'))
#    log_time = time.mktime(time.strptime(l_time,'%Y-%m-%d %H:%M:%S'))
#    if (float(log_time) >= float(s_time)) and (float(log_time) <= float(e_time)):
#        return True
#    return False

def QueryRestaurantOrders(restaurant_id, time_start, time_end):
    start = str(time_start)
    print(start)
    end = str(time_end)
    print(end)
    q = TermQuery("restaurant_id", str(restaurant_id))
    results = conn_order.search(q)

    res = [];
    start = time.mktime(time_start.timetuple())
    end = time.mktime(time_end.timetuple())
    for r in results:
        timeStamp = datetime.datetime.strptime(r[u'created_at'],'%Y-%m-%d %H:%M:%S') 
        mkTimeStamp = time.mktime(timeStamp.timetuple())
        if mkTimeStamp >= start and mkTimeStamp < end:
            res.append(r)
    return res

#time_start = datetime.datetime(2014,11,10,0,0,0)
#time_end = datetime.datetime(2015,11,30,12,0,0)
#res = QueryRestaurantOrders(256365,time_start,time_end)
#print(len(res))
#for r in res:
#    print(r)



