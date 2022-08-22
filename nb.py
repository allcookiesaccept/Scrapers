import pandas as pd

from browser import Browser
from selenium.webdriver.common.by import By

import json



# <script id="__NEXT_DATA__" type="application/json">


with open('nbproductexample.json', 'r', encoding='utf-8') as file:
    next = json.load(file)

props = next['props']['pageProps']['item']['PROPERTIES']
keys = []

for name, properties in props.items():
    _ = name
    pr = properties['GROUP_PROPERTIES']
    for k in pr.keys():
        keys.append(k)

keys = ['OPERATSIONNAYA_SISTEMA', 'PROIZVODITEL', 'RAZRESHENIE_EKRANA', 'TIP_EKRANA', 'CHASTOTA_OBNOVLENIYA_EKRANA',
        'AVTOMATICHESKIY_POVOROT_IZOBRAZHENIYA', 'DIAGONAL', 'MODEL_PROTSESSORA', 'VSTROENNAYA_PAMYAT_2',
        'RAZRESHENIE_FRONTALNOY_KAMERY', 'KOLICHESTVO_OSNOVNYKH_KAMER', 'RAZRESHENIYA_OSNOVNYKH_KAMER',
        'DIAFRAGMY_OSNOVNYKH_KAMER', 'VSPYSHKA_1', 'RAZEM_DLYA_NAUSHNIKOV', 'GEOPOZITSIONIROVANIE', 'LTE', 'WI_FI',
        'BLUETOOTH', 'RAZEM_DLYA_ZARYADKI', 'TIP_AKKUMULYATORA', 'EMKOST_AKKUMULYATORA_2', 'VREMYA_RAZGOVORA_DO',
        'VREMYA_OZHIDANIYA_DO', 'RAZMERY_SHXVXG', 'VES_1', 'GARANTIYA']

