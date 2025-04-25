from django.contrib import admin
from django.urls import path,include
from .views import store_post,dashboard_embedd
app_name = 'DB'
urlpatterns = [
    path("pushed/",store_post,name='post'),
    path("Dashboard/",dashboard_embedd,name='dashboard')
]
