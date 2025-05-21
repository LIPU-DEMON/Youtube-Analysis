from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView,LogoutView
app_name = 'users'
urlpatterns = [
    path("",views.firstpage,name='first'),
    path("accounts/Register",views.Register,name='Register'),
    # path("accounts/",include('django.contrib.auth.urls'))
    path("accounts/login/",LoginView.as_view(template_name='registration/login.html'),name='login'),
    path("accounts/logout/",LogoutView.as_view(next_page='users:login'),name='logout'),
    path("successlogin/",views.Sucesslogin,name='success'),
    path("successlogout/",views.Successlogout,name='successl'),
    path('accounts/profile',views.profile,name='profile'),
    path('accounts/ScrapedHistory',views.scrapeddata,name='scrapedata')
    
  
]
