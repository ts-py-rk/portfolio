# import requests
# import json
# import time
# from pprint import pprint
# import openpyxl
# import os
# import sqlite3
# import logging
# # url = 'https://api.bittrex.com/api/v1.1/public/getcurrencies'
# # u = 'getticker?market=USD-BTC'
# # print(f'{html.text}')
# # price = data['result']['Ask']
#     # if price != prev_price:
#     #     print(f'{price}$')
#     #     prev_price = price
#     # time.sleep(INTERVAL).
# # prev_price = 0
#
# # INTERVAL = 1
# # j = requests.get(url)
# # data = json.loads(j.text)
# # allc = [d['Currency'] for d in data['result']]
# # print(f'{allc=}')
# # cryptos = input('введи крипту: ')
# # cryptos = [c.upper().strip() for c in cryptos.split(',')]
# # print(f'{cryptos=}')
# # notfound = [c for c in cryptos if c not in allc]
# #
# #
# # if notfound:
# #     print(f'{notfound=}')
# #
# # def get_price(crypto):
# #     url = f'https://api.bittrex.com/api/v1.1/public/getticker?market=USD-{crypto}'
# #     j = requests.get(url)
# #     data = json.loads(j.text)
# #     price = data['result']['Ask']
# #     return price
# #
# # # for c in cryptos:
# # #     print(f'{c} - {get_price(c)}')
# #
# # while True:
# #     data = [(c, get_price(c)) for c in cryptos]
# #     print(f'{data}')
# #     time.sleep(1)
# logging.basicConfig(filename='test.log', level=logging.DEBUG, format='%(levelname)s - %(message)s', filemode='w')
# from collections import OrderedDict
# #
# # operations = OrderedDict()
# # logging.debug(f'{os.getcwd()=}')
# #
# # class Operation:
# #     def __init__(self, id, position, quantity ,price):
# #         self.id = id
# #         self.position = position
# #         self.quantity = quantity
# #         self.price = price
# #
# # operations = []
# #
# # file_name = 'binance.xlsx'
# # wb = openpyxl.load_workbook(file_name)
# # sheets = wb.sheetnames
# # logging.debug(f'{wb=}')
# # logging.debug(f'{type(wb)=}')
# # logging.debug(f'{sheets=}')
# #
# # def valid_operations(file):
# #     wb = openpyxl.load_workbook(file)
# #     book = OrderedDict()
# #
# #     for list in book:
# #         wb[list]
# # # for list in sheets:
# # #     try:
# # #         # a = wb.get_sheet_by_name(list)
# # #         a = wb[list]
# # #         print(f'{a=}')
# # #         # cell =  a['A1'].value
# # #         # print(f'{cell=}')
# # #         n_cel = ['A'+str(n) for n in range(1,5)]
# # #         cells = [a[cel].value for cel in n_cel ]
# # #         print(f'{cells=}')
# # #     except:
# # #         pass
# # data = []
# # stroka = []
# #
# # i = 0
# # logging.debug(f'{data=}')
# # logging.debug(f'{i=}')
# # for name in sheets:
# #     logging.debug(f'{name=}')
# #     # name = 'XRP'
# #     # print(f'{name=}')
# #     sheet = wb[name]
# #     logging.debug(f'{sheet=}')
# #     diapazon = tuple(sheet['C4':'F33'])
# #     logging.debug(f'{diapazon=}')
# #
# #     for row in diapazon:
# #         logging.debug(f'{row=}')
# #         logging.debug(f'1){stroka=}')
# #         stroka.append(i)
# #         stroka.append(name)
# #         logging.debug(f'2){stroka=}')
# #         for cell in row:
# #             logging.debug(f'{cell=} - "{cell.value=}')
# #             if cell.value != None :
# #                 if type(cell.value) == str:
# #                     if cell.value[:1] == '=':
# #                         logging.debug(f'ПЛОХАЯ ЯчЕЙКА')
# #                         continue
# #                 logging.debug(f'ХОРОШАЯ ЯчЕЙКА')
# #                 stroka.append(cell.value)
# #                 logging.debug(f'3){stroka=}')
# #             else:
# #                 logging.debug(f'у нас тут в это строке есть NONE')
# #         logging.debug(f'4){stroka=}')
# #         if len(stroka) == 5:
# #             logging.debug(f'len(stroka) == 5')
# #             logging.debug(f'добавляем строку {stroka[:]} в список [data]')
# #             data.append(stroka[:])
# #             i+= 1
# #             logging.debug(f'i+=1 = {i}')
# #         stroka.clear()
# #         logging.debug(f'stroka.clear()')
# #     logging.debug(f'5){stroka=}')
# # pprint(data)
# # for d in data:
# #     logging.debug(f'{d=}')
# #
# # os.chdir('../')
# # conn = sqlite3.connect(r'db.sqlite3')
# # cur = conn.cursor()
# # print('читаем базу данных')
# # cur.execute("SELECT * FROM main_active;")
# # all_results = cur.fetchall()
# # for a_r in all_results:
# #     print(a_r)
# # start_id = len(all_results)+1
# # print(f'{start_id=}')
# # cur.executemany("INSERT INTO main_active VALUES(?, ?, ?, ?, ?);", data)
# # conn.commit()
# # conn.close()
#
# from bs4 import BeautifulSoup
#
# def parser_price(tiker):
#     url_head = 'https://www.binance.com/ru/trade/'
#     url_tail = '_USDT?type=spot'
#     full_url = url_head + tiker + url_tail
#     print(f'{full_url=}')
#     logging.debug(f'{full_url=}')
#     r = requests.get(full_url)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     objects = soup.find('title')
#     zagolovok = objects.string
#     zagolovok = zagolovok.split(" | ")[0]
#     return float(zagolovok)
#
# def parser_price2(tiker):
#     url_head = 'https://www.binance.com/ru/trade/'
#     url_tail = '_USDT?type=spot'
#     full_url = url_head + tiker + url_tail
#     print(f'{full_url=}')
#     logging.debug(f'{full_url=}')
#     r = requests.get(full_url)
#     # soup = BeautifulSoup(r.text, 'lxml')
#     # logging.debug(f'{soup}')
#     soup = BeautifulSoup(r.text, 'html.parser')
#     objects = soup.find('script', id='__APP_DATA')
#     zagolovok = objects.contents[0]
#     print(f'{type(zagolovok)=}')
#     # zagolovok = zagolovok.
#     zagolovok = zagolovok.split('"close":"')[1]
#     zagolovok = zagolovok.split('","high"')[0]
#     zagolovok = float(zagolovok)
#     # zagolovok = zagolovok.split(',')
#     # return float(zagolovok)
#     print(f'{zagolovok=}')
#     print(f'{type(zagolovok)=}')
#     # print(f'{len(zagolovok)=}')
#     # js = dict(zagolovok)
#     # js = json.load(zagolovok)
#     # for z in zagolovok:
#     #     print(f'{z=}')
#     # pprint(js)
#
#     logging.debug(f'{zagolovok=}')
#     return (zagolovok)
#
#
# parser_price2('ONT')
# #
# # lists = [
# # # a = [
# #     [0, 1, 2, 4, 3],
# #     [0, 1, 2, 4, 3],
# #     [0, 1, 2, 4, 3],
# # ]
# # #
# # for list in lists:
# #     print(list)
# # #
# # for i in range(len(lists)):
# #     lists[i][3], lists[i][4] = lists[i][4], lists[i][3]
# #
# # for list in lists:
# #     print(list)
#
# # def swap(lists):
# #     for i in range(len(lists)):
# #         lists[i][3], lists[i][4] = lists[i][4], lists[i][3]
# #     return lists
# #
# # pprint(a)
# # a = swap(a)
# # pprint(a)
#
# # a =
# # {"products":
# #      {"loading":'false',"products":[],"productMap":{},"filterProductMap":{},"typesProductMap":{"perpetual":[],"delivery":[]},
# # "currentProduct":
# # {"symbolDisplay":"ONT/USDT",
# # "low":"0.9564",
# # "close":"1.0488",
# # "high":"1.1038",
# # "open":"1.0178",
# # "volume":"46082872.5100",
# # "quoteVolume":"47150750.293998",
# # "symbol":"ONTUSDT",
# # "tickSize":"0.0001",
# # "minQty":"0.01000000",
# # "quoteAsset":"USDT",
# # "baseAsset":"ONT",
# # "quoteName":"TetherUS",
# # "baseAssetName":"Ontology",
# # "parentMarket":"FIAT",
# # "parentMarketName":"FIAT",
# # "circulatingSupply":862599654,
# # "tags":["pow","pos","mining-zone","BSC"],
# # "tradingStatus":"TRADING"}}
# #
# # Operation=['DoesNotExist', 'LONG', 'MultipleObjectsReturned', 'POZITION_CHOICES', 'SHORT', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_default_pk', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_expr_references', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_prepare_related_fields_for_save', '_save_parents', '_save_table', '_set_pk_val', 'active_set', 'check', 'clean', 'clean_fields', 'comission', 'comission_stavka', 'date_error_message', 'delete', 'from_db', 'full_clean', 'get_deferred_fields', 'get_pozition_display', 'id', 'objects', 'pk', 'pozition', 'prepare_database_save', 'price', 'quantity', 'quantity_real', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'summa', 'tiker', 'unique_error_message', 'validate_unique']
# # for op in sorted(Operation):
# #     print(f'{op}')
# #
# # from . models import Operation
# # from . models import Active
# #
# # actives = Operation.objects.get(pk=0)
# # print(f'{actives=}')
# #

def smart_round(data):
    print(f'START')
    finish = False
    i = 2
    print(f'{i=}')
    while finish == False:
        print(f'START WHILE')
        a = str(round(data, i))
        print(f'{a=}')
        b = a.split('.')
        for bb in b:
            if bb == '0':
                continue
            else:
                finish = True
        i+=1
        # break
        #     else:
        #         i+=1
        # print(f'{round(data, i)=}')
    return round(data, i)


a = 0.00071569741

print(f'{smart_round(a)=}')






# #{% if profilos|get_value_from_dict:t  == 'PROFIT' %}
#                                 {% for key, value in profilos_money.items %}
#                                     {% if key == t %}
#                                        !!! {{ value }} $
#                                     {% endif %}
#                                 {% endfor %}
#                             #{% else %}
#
#                             #{% endif %}

def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)

profilos_money={'ADA': 6646.0, 'BAND': 972.195, 'BNB': 43.36, 'BTC': -30.68042054, 'BTT': 1331986.667, 'DASH': 141.85422, 'DOGE': 21299.14136, 'DOT': 742.89264, 'EOS': 4636.070385999999, 'ETH': -160.5016308, 'FIL': 155.2, 'IOTA': 11620.0885, 'LINK': 315.23, 'LTC': 458.6152912000001, 'NEO': 599.05}


print(f'{get_value_from_dict(profilos_money, "ADA")}')