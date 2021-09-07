"""
Mr.Kataei 8/4/2021
for init server and analysis which have not any machine learning we dont need any big data so
collect data from binance who get us 500 rows of candles we want , in start server we get this
and store in Static and use it in indicators analysis continuously , for now 30min , 1hour ,4hour ,1day timeframes
"""
from binance.client import Client
import pandas as pd


# default timeframes 30min , 1hour ,4hour ,1day
def generate_data(*symbols: str):
    client = Client()
    columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'time2', 'QAV', 'trades',
               'TBAV', 'TQAV', 'Ignore']
    for symbol in symbols:
        data30min = pd.DataFrame(client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_30MINUTE),
                                 columns=columns)
        data1hour = pd.DataFrame(client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR),
                                 columns=columns)
        data4hour = pd.DataFrame(client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_4HOUR),
                                 columns=columns)
        data1day = pd.DataFrame(client.get_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1DAY),
                                columns=columns)

        # private functions
        # in future we will add new timezones for now Tehran
        def convert_timezone():
            data30min['date'] = pd.DatetimeIndex(
                pd.to_datetime(data30min['date'], unit='ms', yearfirst=True)).tz_localize('UTC').tz_convert(
                'Asia/Tehran')
            data1hour['date'] = pd.DatetimeIndex(
                pd.to_datetime(data1hour['date'], unit='ms', yearfirst=True)).tz_localize('UTC').tz_convert(
                'Asia/Tehran')
            data4hour['date'] = pd.DatetimeIndex(
                pd.to_datetime(data4hour['date'], unit='ms', yearfirst=True)).tz_localize('UTC').tz_convert(
                'Asia/Tehran')
            data1day['date'] = pd.DatetimeIndex(
                pd.to_datetime(data1day['date'], unit='ms', yearfirst=True)).tz_localize('UTC').tz_convert(
                'Asia/Tehran')

        # delete close time and Ignore cols
        def delete_columns():
            del data30min['time2']
            del data1hour['time2']
            del data4hour['time2']
            del data1day['time2']
            del data30min['Ignore']
            del data1hour['Ignore']
            del data4hour['Ignore']
            del data1day['Ignore']

        convert_timezone()
        delete_columns()
        data1hour.to_csv(path_or_buf=f'Static/{symbol}-1hour.csv', index=False)
        data30min.to_csv(path_or_buf=f'Static/{symbol}-30min.csv', index=False)
        data4hour.to_csv(path_or_buf=f'Static/{symbol}-4hour.csv', index=False)
        data1day.to_csv(path_or_buf=f'Static/{symbol}-1day.csv', index=False)
