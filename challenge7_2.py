#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import pandas as pd
import matplotlib.pyplot as plt
from decimal import Decimal, ROUND_FLOOR

file_loc = "ClimateChange.xlsx"
data_code = {'CO2': 'EN.ATM.CO2E.KT', 'GDP': 'NY.GDP.MKTP.CD'}
df_data = pd.read_excel(file_loc, sheetname='Data', index_col=0, na_values=['NA'], parse_cols="A,C,G:AB")
nations = ['CHN', 'USA', 'GBR', 'FRA', 'RUS']


def nation_data(data):
    '''以國為單位將資料加總,輸出df'''
    df = df_data.loc[df_data['Series code'] == data_code[data]].replace(
        {'..': pd.np.NaN}).drop('Series code', 1)  # 選擇data，並將表中的".."替換成NaN，刪除"Series code" col
    df = df.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)  # 填NaN數據
    df.dropna(how='all', inplace=True)
    df[data + '-SUM'] = df.values.sum(1)  # 以國為單位將資料加總
    return df


def co2_gdp_plot():
    df = pd.concat([nation_data('CO2')['CO2-SUM'], nation_data('GDP')['GDP-SUM']], axis=1)
    df_co2_gdp = (df - df.min()) / (df.max() - df.min())  # normalize the data
    fig = plt.subplot()
    nation_loc = [df_co2_gdp.index.get_loc(n) for n in nations]
    df_co2_gdp.plot()
    plt.legend(loc='best')
    plt.xlabel('Countries')
    plt.ylabel('Values')
    plt.title('GDP-CO2')
    plt.xticks(nation_loc, nations, rotation=90)
    china = [float(Decimal(Decimal(n).quantize(Decimal('.001'), rounding=ROUND_FLOOR))) for n in df_co2_gdp.loc['CHN']]
    return fig, china
