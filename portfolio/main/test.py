#!/usr/bin/env python3

import os
import json
import time
import requests
# import openpyxl
# import sqlite3
import logging
# import configparser
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# from pprint import pprint
# from bs4 import BeautifulSoup
# from binance.spot import Spot
# from collections import OrderedDict

import math
logging.basicConfig(filename='test.log', level=logging.DEBUG, format='%(levelname)s - %(message)s', filemode='w')

from collections import OrderedDict
id_dict = OrderedDict()
id_dict['id_0'] = 'раз'
id_dict['id_1'] = 'два'
id_dict['id_2'] = 'три'

def cat(n, translate, name, color):
    print(f"{translate[n]})I'm cat {name} and i {color}.")
    return

def dog(n, translate, name, age):
    print(f"{translate[n]})I'm dog {name} and me {age} year.")

list_functions_ = [
    [(cat), {'name': 'tom', 'color': 'black'}],
    # [(cat), {'name': 'tom', 'color': 'black', 'translate': id_dict,}],
    # [(dog), {'name': 'bob', 'age': 4, 'translate': id_dict}]
    [(dog), {'name': 'bob', 'age': 4}]
]
list_functions = [
    [(cat), ('tom', 'black')],
    [(dog), ('bob', 4)]
]

dict_functions = {
    cat: ('tom', 'black'),
    dog: ('bob', 4)
}

def obhod(quantites, functions, slovar):
    for id in range(quantites):
        id = 'id_' + str(id)
        for function in functions:
            function[0](n=id, **function[1], translate=slovar)
def obhod2(quantites, *functions, slovar):
    for id in range(quantites):
        id = 'id_' + str(id)
        functions[0](n=id, **functions[1], translate=slovar)

obhod(3, list_functions_, id_dict)
# obhod2(3, list_functions_, id_dict)