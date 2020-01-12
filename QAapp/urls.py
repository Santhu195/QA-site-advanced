from django.contrib import admin
from django.urls import path
from django.template import RequestContext
from . import views
app_name = 'login'
urlpatterns = [
    path('register', views.register, name='register'),
    path('', views.login,name='login'), 
    path('logout', views.logouts,name='logout'),
    ]
