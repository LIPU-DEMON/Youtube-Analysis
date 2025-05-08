from django.contrib import admin
from django.urls import path
from . import views
app_name = 'scrape'
urlpatterns = [
    path("",views.home,name='home'),
    path("data/",views.data,name='data'),
    path('pushing/',views.statistics,name='sts'),
    path('Scrapedinfo/',views.MoreInfomation,name='info')

    # path('dashboard/',views.dash,name='dash')
    
]
 

