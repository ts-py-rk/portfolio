import openpyxl
import os
import sqlite3
import logging
from pprint import pprint

logging.basicConfig(filename='excel_to_SQL.log', level=logging.DEBUG, format='%(levelname)s - %(message)s', filemode='w')
from collections import OrderedDict

operations = OrderedDict()
print(f'{os.getcwd()=}')

file_name = 'portfolio/main/binance.xlsx'
wb = openpyxl.load_workbook(file_name)
sheets = wb.sheetnames
data = []
stroka = []
i = 0

logging.debug(f'{os.getcwd()=}')
logging.debug(f'{wb=}')
logging.debug(f'{type(wb)=}')
logging.debug(f'{sheets=}')
logging.debug(f'{data=}')
logging.debug(f'{i=}')


for name in sheets:
    logging.debug(f'{name=}')
    sheet = wb[name]
    diapazon = tuple(sheet['C4':'F33'])

    logging.debug(f'{sheet=}')
    logging.debug(f'{diapazon=}')

    for row in diapazon:
        stroka.append(i)
        stroka.append(name)

        logging.debug(f'{row=}')
        logging.debug(f'1){stroka=}')
        logging.debug(f'2){stroka=}')

        for cell in row:

            logging.debug(f'{cell=} - "{cell.value=}')

            if cell.value != None :
                if type(cell.value) == str:
                    if cell.value[:1] == '=':

                        logging.debug(f'ПЛОХАЯ ЯчЕЙКА')

                        continue

                stroka.append(cell.value)

                logging.debug(f'ХОРОШАЯ ЯчЕЙКА')
                logging.debug(f'3){stroka=}')

            else:

                logging.debug(f'у нас тут в это строке есть NONE')

        logging.debug(f'4){stroka=}')

        if len(stroka) == 5:
            data.append(stroka[:])
            i+= 1

            logging.debug(f'len(stroka) == 5')
            logging.debug(f'добавляем строку {stroka[:]} в список [data]')
            logging.debug(f'i+=1 = {i}')

        stroka.clear()

        logging.debug(f'stroka.clear()')

    logging.debug(f'5){stroka=}')
#
pprint(data)
for d in data:
    logging.debug(f'{d=}')
#
# os.chdir('../../../')
# conn = sqlite3.connect(r'db.sqlite3')
# cur = conn.cursor()
# print('читаем базу данных')
# cur.execute("SELECT * FROM main_active2;")
# all_results = cur.fetchall()
# for a_r in all_results:
#     print(a_r)
# start_id = len(all_results)+1
# print(f'{start_id=}')
# # cur.executemany("INSERT INTO main_active2 VALUES(?, ?, ?, ?, ?);", data)
# # conn.commit()
# conn.close()