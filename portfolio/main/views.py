import os
import json
import requests
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
import logging
import configparser
import matplotlib
import matplotlib.pyplot as plt
from .models import Active
from .models import Operation
from .forms import OperationForm
from django.db.models import Avg
from binance.spot import Spot
from datetime import datetime
from django.shortcuts import render, redirect

matplotlib.use('Agg')

logging.basicConfig(filename='views.log',
                    level=logging.ERROR,
                    format='%(levelname)s - %(message)s',
                    filemode='w')

config = configparser.ConfigParser()
config.read('api.cfg', encoding='utf-8')

api_key = config["BINANCE"]["ACTUAL_API_KEY"]
api_secret = config["BINANCE"]["ACTUAL_SECRET_KEY"]

client = Spot(key=api_key, secret=api_secret)
balances = client.account()['balances']
portfolio = {}


def get_price_binance(crypto):
    logging.debug(f'START GET_PRICE_BINANCE - {crypto}')
    tiker = crypto
    tiker_2 = "USDT"
    para = tiker + tiker_2
    if tiker != tiker_2:
        price = float(client.book_ticker(para)['askPrice'])
    else:
        price = 1
    logging.debug(f'{tiker}: {price}$')
    logging.debug(f'STOP')
    return price


def smart_round(data, i):
    logging.info(f'START SMART ROUND')
    logging.debug(f'{data=} - {type(data)=}')
    if data == 0.0:
        return 0
    else:
        finish = False
        while finish == False:
            a = str(round(data, i))
            b = a.split('.')
            for bb in b:
                if bb == '0':
                    continue
                else:
                    finish = True
            i += 1
        logging.debug(f'STOP - {round(data, i)=}')
        return round(data, i)


def index(request):
    start_time = datetime.now().timestamp()
    all_tikers_sort = Operation.objects.order_by('tiker')
    btc = Operation.objects.order_by('tiker')

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
        logging.debug(f'{b=}')
        # tikers
        # course
        if b.tiker not in tikers:
            tikers[b.tiker] = b.tiker
            courses[b.tiker] = get_price_binance(b.tiker)
        # quantitys
        if b.tiker not in quantitys:
            logging.debug(f'if_2')
            quantitys[b.tiker] = b.quantity_real
        else:
            quantitys[b.tiker] += b.quantity_real
        quantitys[b.tiker] = quantitys[b.tiker]
        # volumes
        if b.tiker not in volumes:
            logging.debug(f'if_3')
            volumes[b.tiker] = b.quantity_real * b.price
        else:
            volumes[b.tiker] += (b.quantity_real * b.price)
        # in_positions
        if b.tiker not in in_positions:
            logging.debug(f'if_4')
            in_positions[b.tiker] = b.quantity_real * courses[b.tiker]
        else:
            in_positions[b.tiker] += b.quantity_real * courses[b.tiker]

    for t in tikers.values():
        logging.debug(f'{t=}')
        # middles
        try:
            middles[t] = volumes[t] / quantitys[t]
        except:
            middles[t] = 66666
            logging.error(f'chet fignya so srednej')
        # profilos_money
        # profilos_percent
        profilos_money[t] = in_positions[t] - volumes[t]
        if profilos_money[t] < 0:
            profilos[t] = 'ЛОСЬ'
            profilos_percent[t] = (in_positions[t] / (volumes[t] / 100)) - 100
        else:
            profilos[t] = 'PROFIT'
            profilos_percent[t] = (in_positions[t] / (volumes[t] / 100)) - 100

    logging.debug(f'{tikers=}')
    logging.debug(f'{courses=}')
    logging.debug(f'{volumes=}')
    logging.debug(f'{quantitys=}')
    logging.debug(f'{middles=}')
    logging.debug(f'{in_positions=}')
    logging.debug(f'{profilos_money=}')
    logging.debug(f'{profilos_percent=}')
    logging.debug(f'{profilos=}')

    one_hundread_percent = sum(in_positions.values())
    bitcoin_depo = '₿' + str(round(sum(in_positions.values()) / get_price_binance('BTC'), 5))
    usdt_depo = '$' + str(round(one_hundread_percent, 2))


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
        'usdt': usdt_depo,
        'btc': bitcoin_depo,
    }

    for k, v in content.items():
        if type(v) == dict:
            for kk, vv in v.items():
                try:
                    content[k][kk] = smart_round(vv, 0)
                except:
                    pass
                    logging.error(f'ERROR!')

    page_load = f'--- page loads {round(datetime.now().timestamp() - start_time, 0)} seconds ---'
    content['page_load'] = page_load
    return render(request, 'main/index.html', content)


def stats(request):
    start_time = datetime.now().timestamp()
    all_tikers_sort = Operation.objects.order_by('tiker')
    btc = Operation.objects.order_by('tiker')
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
            courses[b.tiker] = get_price_binance(b.tiker)
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
        # in_positions
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
            logging.error(f'chet ne to so srednej')
        # profilos_money
        # profilos_percent
        profilos_money[t] = in_positions[t] - volumes[t]
        if profilos_money[t] < 0:
            profilos[t] = 'ЛОСЬ'
            profilos_percent[t] = (in_positions[t] / (volumes[t] / 100)) - 100
        else:
            profilos[t] = 'PROFIT'
            profilos_percent[t] = (in_positions[t] / (volumes[t] / 100)) - 100

    percents = {}
    data_names = []
    data_values = []
    one_hundread_percent = sum(in_positions.values())
    one_percent = one_hundread_percent / 100
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(900 / dpi, 900 / dpi))
    matplotlib.rcParams.update({'font.size': 9})
    bitcoin_depo = str(round(sum(in_positions.values()) / get_price_binance('BTC'), 5))
    usdt_depo = str(round(one_hundread_percent, 2))
    data = datetime.now().strftime("%m.%d.%Y %H:%M")
    zagolovok = data + '\nB' + bitcoin_depo + ' \n$' + usdt_depo
    plt.title(zagolovok)
    for k, v in in_positions.items():
        if quantitys[k] > 0:
        # if quantitys[k] != 0:
            data_names.append(k)
            # data_names.append(k + ' - ' + str(smart_round(v/one_percent, 1)) + '%')
            data_values.append(v)

    color = [
        '#FAEBD7',
        '#00FFFF',
        '#7FFF00',
        '#0000FF',
        '#8A2BE2',
        '#B8860B',
        '#006400',
        '#FF8C00',
        '#8B0000',
        '#8FBC8F',
        '#2F4F4F',
        '#00BFFF',
        '#FF00FF',
        '#DCDCDC',
        '#7CFC00',
        '#FFB6C1',
        '#FF0000',
        '#D2B48C',
        '#FF7F50',
        '#6495ED',
        '#BDB76B',
        '#FFD700',
    ]

    plt.pie(data_values,
            labels=data_names,
            autopct='%1.1f%%',
            radius=1,
            pctdistance=1.04,
            labeldistance=1.12,
            rotatelabels=bool,
            colors=color,
            )

    plt.legend(
        bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
        loc='lower left', labels=data_names)
    fig.savefig('./static/img/pie.png')
    fig.savefig(f"./static/img/stats/pie-{data.replace(':', '-')}.png")

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
        'usdt': usdt_depo,
        'btc': bitcoin_depo,
    }

    for k, v in content.items():
        if type(v) == dict:
            for kk, vv in v.items():
                try:
                    content[k][kk] = smart_round(vv, 1)
                except:
                    pass
    page_load = f'--- page loads {round(datetime.now().timestamp() - start_time, 1)} seconds ---'
    content['page_load'] = page_load
    return render(request, 'main/stats.html', content)


def operations(request):
    start_time = datetime.now().timestamp()
    actives = Operation.objects.order_by('-id')
    all_tikers_sort = Operation.objects.order_by('tiker')
    content = {
        'title': 'Операции',
        'active': actives,
        'all_tikers_sort': all_tikers_sort,
    }
    page_load = f'--- page loads {round(datetime.now().timestamp() - start_time, 5)} seconds ---'
    content['page_load'] = page_load
    return render(request, 'main/operations.html', content)


def tiker(request, name):
    start_time = datetime.now().timestamp()
    error = ''
    del_triger = False
    print(f'{Operation.objects.all().last().id=}')
    if request.method == 'POST':
        ids = 120
        for id in range(ids):
            oper = 'del_' + str(id)
            if oper in request.POST:
                print(f'!!!!!!!!!{oper}!!!!!!!!!!')
                del_triger = True
                Operation.objects.filter(id=id).delete()
        form = OperationForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('index')
        else:
            if del_triger == False:
                error = ' АШИПКА'
            else:
                error = ''
    form = OperationForm()
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
    course = get_price_binance(name)
    in_position = (itogo_real) * (course)
    try:
        middle_course = volume / itogo_real
    except:
        middle_course = 66666666
        logging.error(f'chet ne to s kyrsom - {middle_course = }')
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
        'in_position': round(in_position, 2),
        'middle_course': smart_round(middle_course, 2),
        'volume': smart_round(volume, 2),
        'comission': round(comission, 2),
        'all_tikers_sort': all_tikers_sort,
        'delta_money': round(delta_money, 2),
        'profilos': profilos,
        'delta_percent': delta_percent,
        'form': form,
        'error': error,
    }
    page_load = f'--- page loads {round(datetime.now().timestamp() - start_time, 1)} seconds ---'
    content['page_load'] = page_load
    return render(request, 'main/tiker.html', content)


def test(request):
    start_time = datetime.now().timestamp()
    all_tikers_sort = Operation.objects.order_by('tiker')
    btc = Operation.objects.order_by('tiker')

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
        logging.debug(f'{b=}')
        # tikers
        # course
        if b.tiker not in tikers:
            tikers[b.tiker] = b.tiker
            courses[b.tiker] = get_price_binance(b.tiker)
        # quantitys
        if b.tiker not in quantitys:
            logging.debug(f'if_2')
            quantitys[b.tiker] = b.quantity_real
        else:
            quantitys[b.tiker] += b.quantity_real
        quantitys[b.tiker] = quantitys[b.tiker]
        # volumes
        if b.tiker not in volumes:
            logging.debug(f'if_3')
            volumes[b.tiker] = b.quantity_real * b.price
        else:
            volumes[b.tiker] += (b.quantity_real * b.price)
        # in_positions
        if b.tiker not in in_positions:
            logging.debug(f'if_4')
            in_positions[b.tiker] = b.quantity_real * courses[b.tiker]
        else:
            in_positions[b.tiker] += b.quantity_real * courses[b.tiker]

    for t in tikers.values():
        logging.debug(f'{t=}')
        # middles
        try:
            middles[t] = volumes[t] / quantitys[t]
        except:
            middles[t] = 66666
            logging.error(f'chet fignya so srednej')
        # profilos_money
        # profilos_percent
        profilos_money[t] = in_positions[t] - volumes[t]
        if profilos_money[t] < 0:
            profilos[t] = 'ЛОСЬ'
            profilos_percent[t] = (in_positions[t] / (volumes[t] / 100)) - 100
        else:
            profilos[t] = 'PROFIT'
            profilos_percent[t] = (in_positions[t] / (volumes[t] / 100)) - 100

    logging.debug(f'{tikers=}')
    logging.debug(f'{courses=}')
    logging.debug(f'{volumes=}')
    logging.debug(f'{quantitys=}')
    logging.debug(f'{middles=}')
    logging.debug(f'{in_positions=}')
    logging.debug(f'{profilos_money=}')
    logging.debug(f'{profilos_percent=}')
    logging.debug(f'{profilos=}')

    one_hundread_percent = sum(in_positions.values())
    bitcoin_depo = '₿' + str(round(sum(in_positions.values()) / get_price_binance('BTC'), 5))
    usdt_depo = '$' + str(round(one_hundread_percent, 2))


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
        'usdt': usdt_depo,
        'btc': bitcoin_depo,
    }

    for k, v in content.items():
        if type(v) == dict:
            for kk, vv in v.items():
                try:
                    content[k][kk] = smart_round(vv, 0)
                except:
                    pass
                    logging.error(f'ERROR!')

    page_load = f'--- page loads {round(datetime.now().timestamp() - start_time, 0)} seconds ---'
    content['page_load'] = page_load
    return render(request, 'main/test.html', content)


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
