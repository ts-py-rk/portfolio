from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
# from .models import Article
# import datetime
# import pytils
# from .models import Month
# from .models import People
# from .ips import a
# from collections import

import sqlite3
import hashlib
from pprint import pprint
from django.http import HttpResponse   		# импортируем для вывода обычного текста
from django.shortcuts import render, redirect
from . models import Operation
from . models import Active
from django.db.models import Avg
import requests
import json
from bs4 import BeautifulSoup
import logging
from .forms import OperationForm

logging.basicConfig(filename='views.log', level=logging.DEBUG, format='%(levelname)s - %(message)s', filemode='w')

def swap(lists):
    for i in range(len(lists)):
        lists[i][3], lists[i][4] = lists[i][4], lists[i][3]
    return lists

def parser_price(tiker):
    url_head = 'https://www.binance.com/ru/trade/'
    url_tail = '_USDT?layout=pro&type=spot'
    full_url = url_head + tiker + url_tail
    r = requests.get(full_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(f'{soup=}')
    objects = soup.find('title')
    # print(f'{objects=}')
    zagolovok = objects.string
    # print(f'{zagolovok=}')
    zagolovok = zagolovok.split(" | ")[0]
    return float(zagolovok)

def parser_price2(tiker):
    url_head = 'https://www.binance.com/ru/trade/'
    url_tail = '_USDT?type=spot'
    full_url = url_head + tiker + url_tail
    # print(f'{full_url=}')
    r = requests.get(full_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    objects = soup.find('script', id='__APP_DATA')
    zagolovok = objects.contents[0]
    # print(f'{type(zagolovok)=}')
    zagolovok = zagolovok.split('"close":"')[1]
    zagolovok = zagolovok.split('","high"')[0]
    zagolovok = float(zagolovok)
    # print(f'{zagolovok=}')
    # print(f'{type(zagolovok)=}')
    return (zagolovok)

def get_price(crypto):
    url = f'https://api.bittrex.com/api/v1.1/public/getticker?market=USD-{crypto}'
    j = requests.get(url)
    data = json.loads(j.text)
    try:
        price = data['result']['Ask']

    except:
        # print(f'исключение')
        price = parser_price2(crypto)
    return price

def smart_round(data):
    # print(f'START')
    finish = False
    i = 0
    # print(f'{i=}')
    while finish == False:
        # print(f'START WHILE')
        a = str(round(data, i))
        # print(f'{a=}')
        b = a.split('.')
        for bb in b:
            if bb == '0':
                continue
            else:
                finish = True
        i+=1
    return round(data, i)

def index(request):
    actives = Operation.objects.order_by('-id')
    # ordering = ['tiker']
    all_tikers_sort = Operation.objects.order_by('tiker')
    content = {
        'title': 'INDEX',
        'active': actives,
        'all_tikers_sort' : all_tikers_sort,
    }
    return render(request, 'main/index.html', content)

def tiker(request, name):
    error = ''
    if request.method == 'POST':
        form = OperationForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('index')
        else:
            error = ' АШИПКА'
    form = OperationForm()

    # if request.GET('quantity', 'defaultOrderField'):
    #     order_by = request.GET.get('quantity')
    #     # btc = Operation.objects.all().order_by(order_by)
    # else:
    #     btc = Operation.objects.filter(tiker=name)
    btc = Operation.objects.filter(tiker=name)
    summa = []
    volumes = []
    comissions = []
    for b in btc:
        summa.append(b.quantity_real)
        volumes.append(b.quantity_real * b.price)
        comissions.append(b.comission)
    itogo = btc.aggregate(Avg('quantity'))['quantity__avg'] * btc.count()
    volume = sum(volumes)
    itogo_real = sum(summa)
    course = get_price(name)
    in_position = (itogo_real) * (course)
    try:
        middle_course = volume / itogo_real
    except:
        middle_course = 66666666
    comission = sum(comissions)
    all_tikers_sort = Operation.objects.order_by('tiker')
    delta_money = in_position - volume
    if delta_money > 0:
        profilos = 'Доход'
        delta_percent = round((in_position / (volume / 100) - 100), 2)
    elif delta_money < 0:
        profilos = 'Лось'
        delta_percent = round(100 - (in_position / (volume / 100)), 2) * -1
    else:
        profilos = 'В НОЛЬ'

    content = {
        'tiker': name,
        'active': btc,
        'itogo': itogo,
        'course': course,
        'itogo_real': round(itogo_real, 4),
        'in_position': round(in_position,2),
        'middle_course': round(middle_course,2),
        'volume': round(volume,2),
        'comission' : comission,
        'all_tikers_sort': all_tikers_sort,
        'delta_money': round(delta_money, 2),
        'profilos': profilos,
        'delta_percent': delta_percent,
        'form': form,
        'error': error,
    }
    return render(request, 'main/tiker.html', content)

def stats(request):

    all_tikers_sort = Operation.objects.order_by('tiker')

    btc = Operation.objects.order_by('tiker')
    # btc = Operation.objects.filter(tiker='BTC')
    # btc = Operation.objects.get(pk=1)
    tikers = {}
    courses = {}
    volumes = {}
    quantitys = {}
    middles = {}
    in_positions = {}
    profilos_money = {}
    profilos_percent = {}
    profilos = {}


    for b in btc:

        # tikers
        # course
        if b.tiker not in tikers:
            tikers[b.tiker] = b.tiker
            courses[b.tiker] = 666
            # courses[b.tiker] = get_price(b.tiker)

        # quantitys
        if b.tiker not in quantitys:
            quantitys[b.tiker] = b.quantity_real
        else:
            quantitys[b.tiker] += b.quantity_real
        quantitys[b.tiker] = quantitys[b.tiker]

        # volumes
        if b.tiker not in volumes:
            volumes[b.tiker] = b.quantity_real * b.price
        else:
            volumes[b.tiker] += (b.quantity_real * b.price)

        #in_positions
        if b.tiker not in in_positions:
            in_positions[b.tiker] = b.quantity_real * courses[b.tiker]
        else:
            in_positions[b.tiker] += b.quantity_real * courses[b.tiker]


    for t in tikers.values():

        # middles
        try:
            middles[t] = volumes[t] / quantitys[t]
        except:
            middles[t] = 66666
        # profilos_money
        # profilos_percent
        profilos_money[t] = in_positions[t] - volumes[t]
        if profilos_money[t] < 0:
            profilos[t] = 'ЛОСЬ'
            profilos_percent[t] = (in_positions[t] / (volumes[t]/100)) - 100
        else:
            profilos[t] = 'PROFIT'
            profilos_percent[t] = (in_positions[t] / (volumes[t] / 100)) - 100


    content = {
        'tikers': tikers,
        'courses': courses,
        'quantitys': quantitys,
        'middles': middles,
        'in_positions': in_positions,
        'volumes': volumes,
        'all_tikers_sort': all_tikers_sort,
        'profilos_money': profilos_money,
        'profilos_percent': profilos_percent,
        'profilos': profilos,

    }

    for k, v in content.items():
        if type(v) == dict:
            for kk, vv in v.items():
                try:
                    content[k][kk] = smart_round(vv)
                except:
                    pass

    return render(request, 'main/stats.html', content)

def test(request):
    error = ''
    if request.method == 'POST':
        form = OperationForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('index')
        else:
            error = ' АШИПКА'
    form = OperationForm()
    form = {
        'form': form,
        'error': error,
    }
    return render(request, 'main/test.html', form)

def test2(request):
    tikers = set()
    cripta = {}
    operations = set(Operation.objects.all())
    for tiker in operations:
        cripta[tiker.id] = tiker.tiker
    tikers = sorted(list(tikers))
    all_tikers_sort = Operation.objects.order_by('tiker')
    content = {
        'title': 'TEST',
        'active': Operation.objects.all(),
        'all_tikers_sort': all_tikers_sort,
    }
    return render(request, 'main/test.html', content)

