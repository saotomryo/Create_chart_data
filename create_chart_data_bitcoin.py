#coding: utf-8

import requests
import json
import sys
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from plotly.subplots import make_subplots
from plotly.graph_objs import *
from dateutil.relativedelta import relativedelta


if len(sys.argv) != 4:
    sys.stderr.write("Invalid command line argument.\n")
    sys.exit()

# Create 1-month data
def create_1_month():
    day_1_df = pd.DataFrame(data['result'][periods], columns=col)
    day_1_df['date_time'] = pd.to_datetime(day_1_df['close_time'], unit='s')
    day_1_df['month'] = day_1_df['date_time'].dt.month
    day_1_df['year'] = day_1_df['date_time'].dt.year
    day_1_df['year-month'] = day_1_df['year'].astype('str') + '-' + day_1_df['month'].astype('str')
    day_1_df

    temp_month_1_df = day_1_df.groupby('year-month').aggregate(['min', 'max','first','last'])
    month_1_df = pd.concat([
                            temp_month_1_df['close_price']['last'],
                            temp_month_1_df['open_price']['first'],
                            temp_month_1_df['high_price']['max'],
                            temp_month_1_df['low_price']['min']
                            ],axis=1)
    month_1_df = month_1_df.reset_index()
    month_1_df['year-month'] = pd.to_datetime(month_1_df['year-month'])
    month_1_df.columns = ['date_time','close_price','open_price','high_price','low_price']
    month_1_df = month_1_df.sort_values('date_time')
    return month_1_df

# Create 3-month data
def create_3_month():
    day_1_df = pd.DataFrame(data['result'][periods], columns=col)
    day_1_df['date_time'] = pd.to_datetime(day_1_df['close_time'], unit='s')

    
    temp_quarter_df = day_1_df.groupby(day_1_df['date_time'].dt.to_period('Q')).aggregate(['min', 'max','first','last'])

    quarter_df = pd.concat([
                            temp_quarter_df['close_price']['last'],
                            temp_quarter_df['open_price']['first'],
                            temp_quarter_df['high_price']['max'],
                            temp_quarter_df['low_price']['min']
                            ],axis=1)

    quarter_df = quarter_df.reset_index()
    quarter_df['date_time'] 

    quarter_df['date_time'] = [pd.Period.to_timestamp(x) for x in quarter_df['date_time'].values]

    quarter_df.columns = ['date_time','close_price','open_price','high_price','low_price']
    quarter_df = quarter_df.sort_values('date_time')
    return quarter_df

# Create 6-month data
def combine_quarter_data(row):
    if row['date_time'].month == 4 or row['date_time'].month == 10:
        row['date_time'] = row['date_time'] + relativedelta(months=-3)
    return row


def create_6_month():
    quarter_df = create_3_month()
    quarter_df = quarter_df.apply(combine_quarter_data,axis=1)

    temp_6_month_df = quarter_df.groupby('date_time').aggregate(['min', 'max','first','last'])

    month_6_df = pd.concat([
                        temp_6_month_df['close_price']['last'],
                        temp_6_month_df['open_price']['first'],
                        temp_6_month_df['high_price']['max'],
                        temp_6_month_df['low_price']['min']
                        ],axis=1)

    month_6_df = month_6_df.reset_index()
    month_6_df['date_time'] = pd.to_datetime(month_6_df['date_time'])

    month_6_df.columns = ['date_time','close_price','open_price','high_price','low_price']
    month_6_df = month_6_df.sort_values('date_time')
    return month_6_df

# Create 1-year data
def create_1_year():
    day_1_df = pd.DataFrame(data['result'][periods], columns=col)
    day_1_df['date_time'] = pd.to_datetime(day_1_df['close_time'], unit='s')
    day_1_df['year'] = day_1_df['date_time'].dt.year

    temp_year_1_df = day_1_df.groupby('year').aggregate(['min', 'max','first','last'])
    year_1_df = pd.concat([
                            temp_year_1_df['close_price']['last'],
                            temp_year_1_df['open_price']['first'],
                            temp_year_1_df['high_price']['max'],
                            temp_year_1_df['low_price']['min']
                            ],axis=1)
    year_1_df = year_1_df.reset_index()

    year_1_df.columns = ['date_time','close_price','open_price','high_price','low_price']
    year_1_df = year_1_df.sort_values('date_time')
    return year_1_df

# Create 2-year data

def create_2_years_data(row):
    min_year = int(row['min_year'])
    year = int(row['year'])
    if ((min_year % 2) == 0) & ((year % 2) != 0):
        year -= 1
    elif ((min_year % 2) != 0) & ((year % 2) == 0):
        year -= 1
    return str(year)

def create_2_year():
    year_1_df = create_1_year()
    year_1_df['min_year'] = year_1_df['date_time'].values.min()
    year_1_df['year'] = year_1_df['date_time']

    year_1_df['year_2'] = year_1_df.apply(create_2_years_data,axis=1)
    

    temp_year_2_df = year_1_df.groupby('year_2').aggregate(['min', 'max','first','last'])
    year_2_df = pd.concat([
                            temp_year_2_df['close_price']['last'],
                            temp_year_2_df['open_price']['first'],
                            temp_year_2_df['high_price']['max'],
                            temp_year_2_df['low_price']['min']
                            ],axis=1)
    year_2_df = year_2_df.reset_index()

    year_2_df.columns = ['date_time','close_price','open_price','high_price','low_price']
    year_2_df = year_2_df.sort_values('date_time')
    return year_2_df

# Create 3-year data

def create_3_years_data(row):
    min_year = int(row['min_year'])
    year = int(row['year'])
    diff = year - min_year
    if ((diff % 3) == 1):
        year -= 1
    elif ((diff % 3) == 2):
        year -= 2
    return str(year)

def create_3_year():
    year_1_df = create_1_year()
    year_1_df['min_year'] = year_1_df['date_time'].values.min()
    year_1_df['year'] = year_1_df['date_time']

    year_1_df['year_3'] = year_1_df.apply(create_3_years_data,axis=1)
    

    temp_year_3_df = year_1_df.groupby('year_3').aggregate(['min', 'max','first','last'])
    year_3_df = pd.concat([
                            temp_year_3_df['close_price']['last'],
                            temp_year_3_df['open_price']['first'],
                            temp_year_3_df['high_price']['max'],
                            temp_year_3_df['low_price']['min']
                            ],axis=1)
    year_3_df = year_3_df.reset_index()

    year_3_df.columns = ['date_time','close_price','open_price','high_price','low_price']
    year_3_df = year_3_df.sort_values('date_time')
    return year_3_df

# Create 5-year data

def create_5_years_data(row):
    min_year = int(row['min_year'])
    year = int(row['year'])
    diff = year - min_year
    if ((diff % 5) == 1):
        year -= 1
    elif ((diff % 5) == 2):
        year -= 2
    elif ((diff % 5) == 3):
        year -= 3
    elif ((diff % 5) == 4):
        year -= 4
    return str(year)

def create_5_year():
    year_1_df = create_1_year()
    year_1_df['min_year'] = year_1_df['date_time'].values.min()
    year_1_df['year'] = year_1_df['date_time']

    year_1_df['year_5'] = year_1_df.apply(create_5_years_data,axis=1)
    

    temp_year_5_df = year_1_df.groupby('year_5').aggregate(['min', 'max','first','last'])
    year_5_df = pd.concat([
                            temp_year_5_df['close_price']['last'],
                            temp_year_5_df['open_price']['first'],
                            temp_year_5_df['high_price']['max'],
                            temp_year_5_df['low_price']['min']
                            ],axis=1)
    year_5_df = year_5_df.reset_index()

    year_5_df.columns = ['date_time','close_price','open_price','high_price','low_price']
    year_5_df = year_5_df.sort_values('date_time')
    return year_5_df

#python get_1_minites_bitcoin_data.py [period] [start(YYYY-mm-dd)] [end(YYYY-mm-dd/0)] [csvfile]

#parameter
market = "bitstamp/"
pricetype = "btcusd/"
periodslist = {"1m":"60", "5m":"300", "1h":"3600", "4h":"14400", "1d":"86400", 
            "1w":"604800","1m":"604800","3m":"604800",
            "6m":"604800","1y":"604800","2y":"604800",
            "3y":"604800","5y":"604800"}
period = sys.argv[1]
start = sys.argv[2]
end = sys.argv[3] 
periods = periodslist[period]

tstr = start.split("/") #dd/mm/yyyy
after = datetime(int(tstr[2]), int(tstr[1]), int(tstr[0]), 0, 0, 0, 0).timestamp()

if end != "0":
    tstr = end.split("/")
    before = datetime(int(tstr[2]), int(tstr[1]), int(tstr[0]), 0, 0, 0, 0).timestamp()#コマンドライン引数の日付

# create url
url = "https://api.cryptowat.ch/markets/" + market + pricetype + "ohlc?periods=" + periods + "&after=" + str(int(after)) + "&before=" + str(int(before))

res = requests.get(url)
data = json.loads(res.text)

col = ['close_time', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'quote_volume']
if sys.argv[1] == '1m':
    df = create_1_month()
elif sys.argv[1] == '3m':
    df = create_3_month()
elif sys.argv[1] == '6m':
    df = create_6_month()
elif sys.argv[1] == '1y':
    df = create_1_year()
elif sys.argv[1] == '2y':
    df = create_2_year()
elif sys.argv[1] == '3y':
    df = create_3_year()
elif sys.argv[1] == '5y':
    df = create_5_year()
else:
    df = pd.DataFrame(data['result'][periods], columns=col)
    df['date_time'] = pd.to_datetime(df['close_time'], unit='s')

fig = make_subplots(rows=1, cols=1,
                    vertical_spacing=0.25,
                    subplot_titles=period)
                    
trace1 = {
    'type': 'candlestick',
    'x': df['date_time'],
    'yaxis': 'y2',
    'name':period,
    'low': df['low_price'],
    'high': df['high_price'],
    'open': df['open_price'],
    'close': df['close_price']
}

fig.add_trace(trace1,row=1,col=1)

fig.update_layout(showlegend=False,
                  width=800,
                  height=1400)

fig.show()

df.to_csv(period + '-' + start.replace('/','-') + '-' + end.replace('/','-') + '.csv' ,index=None)
