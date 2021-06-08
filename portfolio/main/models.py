from django.db import models
from django.utils import timezone
import datetime
import requests
from bs4 import BeautifulSoup
import json


# class Active(models.Model):
#     tiker = models.CharField('Тикер', max_length=15)
#     LONG = 'купил'
#     SHORT = 'продал'
#     POZITION_CHOICES = [(LONG, 'Купил'),(SHORT, 'Продал')]
#     pozition = models.CharField(
#         verbose_name='Тип позиции',
#         max_length=6,
#         choices=POZITION_CHOICES,
#         default=LONG,
#     )
#     quantity = models.FloatField(verbose_name='Количество', null=True, default=0)
#     price = models.FloatField(verbose_name='Цена', null=True, default=0)
#     comission_stavka = 0.001
#     # test = models.CharField('test', max_length=15, default=0)
#
#     @property
#     def comission(self):
#         return round((self.summa()) * (self.comission_stavka), 2)
#
#     @property
#     def quantity_real(self):
#         # print(f'@property\ndef quantity_real(self)\n{self.pozition=}')
#         if self.pozition == 'купил':
#             return self.quantity
#         else:
#             return self.quantity * (-1)
#
#     # @property
#     def summa(self):
#         return round((self.quantity_real) * (self.price), 2)
#
#
#     def __str__(self):
#         if self.tiker == None:
#             return 'tiker is NULL'
#         return self.tiker
#
#     class Meta:
#         verbose_name = 'Тикер'
#         verbose_name_plural = 'Тикер'

# from portfolio.main.views import parser_price2


class Operation(models.Model):
    tiker = models.CharField('Тикер', max_length=15)
    LONG = 'купил'
    SHORT = 'продал'
    POZITION_CHOICES = [(LONG, 'Купил'), (SHORT, 'Продал')]
    pozition = models.CharField(
        verbose_name='Тип позиции',
        max_length=6,
        choices=POZITION_CHOICES,
        default=LONG,
    )
    quantity = models.FloatField(verbose_name='Количество', null=True)
    price = models.FloatField(verbose_name='Цена', null=True)
    comission_stavka = 0.001

    # test = models.CharField('test', max_length=15, default=0)

    @property
    def comission(self):
        if self.pozition != 'купил':
            return round((self.summa()) * (self.comission_stavka), 2) * -1
        else:
            return round((self.summa()) * (self.comission_stavka), 2)

    @property
    def quantity_real(self):
        if self.pozition == 'купил':
            return self.quantity
        else:
            return self.quantity * (-1)

    # @property
    def summa(self):
        return round((self.quantity_real) * (self.price), 2)

    # def delta_money(self):
    #     return self.

    def __str__(self):
        if self.tiker == None:
            return 'tiker is NULL'
        return self.tiker

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'


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
        # price = parser_price2(crypto)

    except:
        print(f'исключение')
        price = parser_price2(crypto)
    return price


class Active(models.Model):

    operation = models.ForeignKey(Operation, on_delete=models.DO_NOTHING)


    tikers = list(set(Operation.objects.all()))

    middle = models.FloatField(verbose_name='Средняя', null=True, default=0)
    volume = models.FloatField(verbose_name='Объем', null=True, default=0)
    in_pozition= models.FloatField(verbose_name='В позиции', null=True, default=0)

    # middle = Operation.quantity_real * get_price(Operation.tikers)


    # @property
    # def volume(self):
    #     a = 1
    #     return 'self.operation'

    # tests = Operation.objects.all()
    # print(f'{len(tests)=}')
    # print(f'{Operation.objects.get(pk=1)=}')
    # print(f'{Operation.objects.get(pk=1).pozition=}')
    # for i in range(20):
    #     print(f'Operation.objects.get(pk={i}) = {Operation.objects.get(pk=i)}')
    #
    # for t in tests:
    #     print(f'{t.pozition=}')

    # tiker = models.Model(Active, on_delete='CASCADE')


    def __str__(self):
        if self.tikers == None:
            return 'tiker is NULL'
        return str(self.tikers)

    class Meta:
        verbose_name = 'Актив'
        verbose_name_plural = 'Активы'
