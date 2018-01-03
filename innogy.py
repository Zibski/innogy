#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 18:40:09 2018

@author: zibski
"""

import ezodf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


doc = ezodf.opendoc('innogy.ods')
sheet = doc.sheets[0]
df_dict = {}
for i, row in enumerate(sheet.rows()):
    if i ==0:
        df_dict = {cell.value:[] for cell in row}
        col_index = {j:cell.value for j, cell in enumerate(row)}
        continue
    for j, cell in enumerate(row):
        df_dict[col_index[j]].append(cell.value)
        
df = pd.DataFrame(df_dict)
df['Odczyt'] = df['Odczyt'].str.replace(r',', '.')
df['Odczyt'] = df['Odczyt'].str.replace(r' kWh', '').astype('float')
df['Poprzedni odczyt'] = df['Odczyt'].shift(-1)
df['Zużycie'] = df['Odczyt'] - df['Poprzedni odczyt']
df['Data odczytu '] = pd.to_datetime(df['Data odczytu '], dayfirst=True)
df['Data poprzedniego odczytu'] = df['Data odczytu '].shift(-1)
df['Okres'] = df['Data odczytu '] - df['Data poprzedniego odczytu']
df['Okres']= (df['Okres'] / np.timedelta64(1, 'D')).astype(float)

df['kWh/msc'] = (df['Zużycie']/df['Okres'].astype('float'))*30.5

x = df['Data odczytu ']
y = df['kWh/msc']

plt.figure()
plt.plot(x,y)
plt.xticks(rotation=70)
plt.show()