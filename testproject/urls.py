"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^predictorder/index', 'predictorder.views.index', name='predictorderindex'),
    url(r'^predictorder/predictorder', 'predictorder.views.predictOrder', name='predictOrder'),
    url(r'^predictorder/statisticorder', 'predictorder.views.statisticOrder', name='statisticOrder'),
    url(r'^predictorder/orderdata', 'predictorder.views.getOrderData', name='getOrderData'),
    url(r'^predictorder/statisticdata', 'predictorder.views.getStatisticData', name='getStatisticData'),
    url(r'^compdstr/index', 'compdstr.views.index', name='compdstrindex'),
    url(r'^compdstr/getshopdata', 'compdstr.views.getShopData', name='getShopData'),
    url(r'^compdstr/getweiddata', 'compdstr.views.getWeidData', name='getWeidData'),
    url(r'^compdstr/changedata', 'compdstr.views.changeData', name='changeData'),
    url(r'^compdstr/getchangedata', 'compdstr.views.getChangeData', name='getChangeData'),
    url(r'^analy/index', 'analy.views.index', name='analyindex'),
]
