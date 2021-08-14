from binance.client import Client
import pandas as pd

#default timeframes 30min , 1hour ,4hour ,1day
def generate_data(symbol:str):
    client = Client()
    columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'time2', 'QAV', 'trades',
               'TBAV', 'TQAV', 'Ignore']
    candles1day = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY)
    data1day = pd.DataFrame(candles1day,columns=columns)
    candles1hour = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR)
    data1hour = pd.DataFrame(candles1hour,columns=columns)
    candles4hour = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_4HOUR)
    data4hour = pd.DataFrame(candles4hour,columns=columns)
    candles30min = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_30MINUTE)
    data30min = pd.DataFrame(candles30min,columns=columns)
    def convert_timezone():
        data30min['date'] = pd.DatetimeIndex(pd.to_datetime(data30min['date'], unit='ms', yearfirst=True)).tz_localize('UTC').tz_convert('Asia/Tehran')
        data1hour['date'] = pd.DatetimeIndex(pd.to_datetime(data1hour['date'], unit='ms', yearfirst=True)).tz_localize('UTC').tz_convert('Asia/Tehran')
        data4hour['date'] = pd.DatetimeIndex(pd.to_datetime(data4hour['date'], unit='ms', yearfirst=True)).tz_localize('UTC').tz_convert('Asia/Tehran')
        data1day['date'] = pd.DatetimeIndex(pd.to_datetime(data1day['date'], unit='ms', yearfirst=True)).tz_localize('UTC').tz_convert('Asia/Tehran')
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
    data1hour.to_csv(path_or_buf=f'../Static/{symbol}-1hour.csv' ,index=False)
    data30min.to_csv(path_or_buf=f'../Static/{symbol}-30min.csv',index=False)
    data4hour.to_csv(path_or_buf=f'../Static/{symbol}-4hour.csv',index=False)
    data1day.to_csv(path_or_buf=f'../Static/{symbol}-1day.csv',index=False)
