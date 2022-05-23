from django.contrib import admin
from .models import Operation
from . import views
from django.urls import include, path

tiker = 'BTC'

urlpatterns = [
    path('', views.index, name='index'),
    path('operations/', views.operations, name='operations'),
    path('test/', views.test, name='test'),
    path('test2/', views.test2, name='test2'),
    path('stats/', views.stats, name='stats'),
    path('tiker/<str:name>/', views.tiker, name='tiker'),

]
