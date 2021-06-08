from django.urls import include, path
from django.contrib import admin
from . import views
from . models import Operation

tiker = 'BTC'

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('test2/', views.test2, name='test2'),
    path('stats/', views.stats, name='stats'),
    path('tiker/<str:name>/', views.tiker, name='tiker'),

]