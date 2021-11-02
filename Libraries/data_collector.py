"""
Mr.Kataei 8/4/2021
get_candle_api use in stream to get candles for analysis and strategies this method have limit for n last candles
you need for analysis.data collect form Bitfinex API where url can change for any API you want.
there is 3 type of dictionary for bitfinex symbols or CSvs we need to save
_get_all_candles is private method to use in generate_big_data where collect all data that can get from bitfinex

"""
import datetime
import time
import pandas as pd
import requests

symbols = {'BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOGEUSDT', 'BCHUSDT', 'ETCUSDT'}

symbols_bitfinix = {'BTCUSDT': 'tBTCUSD', 'ETHUSDT': 'tETHUSD', 'ADAUSDT': 'tADAUSD', 'DOGEUSDT': 'tDOGE:USD',
                    'BCHUSDT': 'tBCHN:USD', 'ETCUSDT': 'tETCUSD'}

symbols_csv = {'tBTCUSD': 'Bitcoin', 'tETHUSD': 'Ethereum', 'tADAUSD': 'Cardano', 'tDOGE:USD': 'Doge-Coin',
               'tBCHN:USD': 'Bitcoin-Cash', 'tETCUSD': 'Ethereum-Classic'}

timeframe_csv = {'30m': '30-Minute', '1h': '1-Hour', '4h': '4-Hour', '1D': '1-Day'}


def get_candle_binance(symbol: str, timeframe: str, limit: int):
    params = {'interval': timeframe, 'symbol': symbol, 'limit': limit}
    url = 'https://api1.binance.com/api/v3/klines'
    try:
        r = requests.get(url=url, params=params)
        data = r.json()
        data = pd.DataFrame(data=data, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                                'Qav', 'trade-number', 'TBbav', 'TBbqv', 'ignore']).astype(float)
        data = data[data.columns[0:6]]
        data.date = pd.DatetimeIndex(pd.to_datetime(data['date'], unit='ms', yearfirst=True)).tz_localize('UTC').tz_convert(
            'Asia/Tehran')
        return data
    except Exception as e:
        print('something wrong on get data from binance:\n', e)


def get_candle_bitfinex(symbol: str, timeframe: str, limit: int):
    symbol = symbols_bitfinix[symbol]
    params = {'limit': limit, 'sort': -1}
    url = f'https://api-pub.bitfinex.com/v2/candles/trade:{timeframe}:{symbol}/hist'
    try:
        r = requests.get(url=url, params=params)
        data = r.json()
        data = pd.DataFrame(data=data, columns=['date', 'open', 'close', 'high', 'low', 'volume'])
        data.date = pd.DatetimeIndex(pd.to_datetime(data['date'], unit='ms', yearfirst=True)
                                     ).tz_localize('UTC').tz_convert('Asia/Tehran')
        data = data.iloc[::-1]
        data = data.reset_index(drop=True)
        return data
    except Exception as e:
        print('something wrong on get data from bitfinex:\n', e)


def _get_all_candles(symbol: str, timeframe: str):
    symbol = symbols_bitfinix[symbol]
    params = {'limit': 10000, 'sort': 1}
    url = f'https://api-pub.bitfinex.com/v2/candles/trade:{timeframe}:{symbol}/hist'
    r = requests.get(url=url, params=params)
    data = r.json()
    data = pd.DataFrame(data=data, columns=['date', 'open', 'close', 'high', 'low', 'volume'])
    start_time = int(data.tail(1)['date'].values[0])
    end_time = int(round(time.time() * 1000))
    while start_time < end_time:
        params = {'limit': 10000, 'sort': 1, 'start': start_time}
        r = requests.get(url=url, params=params)
        next_data = r.json()
        next_data = pd.DataFrame(data=next_data, columns=['date', 'open', 'close', 'high', 'low', 'volume'])
        data = pd.concat([data, next_data], axis=0)
        data = data.reset_index(drop=True)
        start_time = int(data.tail(1)['date'].values[0])
    data.date = pd.DatetimeIndex(pd.to_datetime(data['date'], unit='ms', yearfirst=True)
                                 ).tz_localize('UTC').tz_convert('Asia/Tehran')
    data = data.drop_duplicates(subset=['date'])
    data.to_csv(path_or_buf=f'Static/{symbols_csv[symbol]}-{timeframe_csv[timeframe]}.csv', index=False)


def complete_candles_csv(symbol: str, timeframe: str):
    url = f'https://api-pub.bitfinex.com/v2/candles/trade:{timeframe}:{symbol}/hist'
    path = f'Static/{symbols_csv[symbol]}-{timeframe}.csv'
    data = pd.read_csv(path)
    last = data['date'].tail(1)
    start_time = time.mktime(datetime.datetime.strptime(last.item(), "%Y-%m-%d %H:%M:%S%z").timetuple())
    params = {'limit': 10000, 'sort': 1, 'start': start_time}
    r = requests.get(url=url, params=params)
    next_data = r.json()
    next_data = pd.DataFrame(data=next_data, columns=['date', 'open', 'close', 'high', 'low', 'volume']).ty
    data = pd.concat([data, next_data], axis=0)
    data = data.reset_index(drop=True)
    data.date = pd.DatetimeIndex(pd.to_datetime(data['date'], unit='ms', yearfirst=True)
                                 ).tz_localize('UTC').tz_convert('Asia/Tehran')
    data = data.drop_duplicates(subset=['date'])
    data.to_csv(path_or_buf=path, index=False)


def generate_big_data():
    for symbol in symbols:
        _get_all_candles(symbol=symbol, timeframe='30m')
        _get_all_candles(symbol=symbol, timeframe='1h')
        _get_all_candles(symbol=symbol, timeframe='4h')
        _get_all_candles(symbol=symbol, timeframe='1D')
