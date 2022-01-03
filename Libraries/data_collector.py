"""
Mr.Kataei 8/4/2021
get_candle_api use in stream to get candles for analysis and strategies this method have limit for n last candles
you need for analysis.data collect form Bitfinex API where url can change for any API you want.
there is 3 type of dictionary for bitfinex symbols or CSvs we need to save
_get_all_candles is private method to use in generate_big_data where collect all data that can get from bitfinex

"""
import time
import pandas as pd
import requests
import enum


class Exchange(enum.Enum):
    binance = 'binance'
    bitfinex = 'bitfinex'


class Symbols(enum.Enum):
    BTCUSDT = 'bitcoin'
    ETHUSDT = 'ethereum'
    ADAUSDT = 'cardano'
    DOGEUSDT = 'doge'
    BCHUSDT = 'bitcoinCash'
    ETCUSDT = 'ethereumClassic'


symbols = {'BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOGEUSDT', 'BCHUSDT', 'ETCUSDT'}

symbols_bitfinix = {'BTCUSDT': 'tBTCUSD', 'ETHUSDT': 'tETHUSD', 'ADAUSDT': 'tADAUSD', 'DOGEUSDT': 'tDOGE:USD',
                    'BCHUSDT': 'tBCHN:USD', 'ETCUSDT': 'tETCUSD'}


def get_url_params_column(exchange: Exchange, timeframe: str, symbol: str, start_time: int = 115133520000):
    # 115133520000 is Wednesday, 21 December 2005 02:52:00
    if exchange.name == Exchange.binance.name:
        params = {'interval': timeframe, 'symbol': symbol, 'limit': 1000, 'startTime': start_time}
        url = 'https://api1.binance.com/api/v3/klines'
        columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'Qav', 'trade-number', 'TBbav',
                   'TBbqv', 'ignore']
    elif exchange.name == Exchange.bitfinex.name:
        symbol = symbols_bitfinix[symbol]
        params = {'limit': 10000, 'sort': 1, 'start': start_time}
        url = f'https://api-pub.bitfinex.com/v2/candles/trade:{timeframe}:{symbol}/hist'
        columns = ['date', 'open', 'close', 'high', 'low', 'volume']
    else:
        return
    return params, url, columns


def get_all_candles_binance(exchange: Exchange, symbol: Symbols, number: int = 4, unit: str = 'h',
                            is_tehran: bool = True, save_csv: bool = True):
    unit = unit
    number = number
    convert_time_to_ms = 0
    timeframe = str(number) + unit
    symbol = symbol.name
    params, url, columns = get_url_params_column(exchange=exchange, timeframe=timeframe, symbol=symbol)
    if params is None:
        return
    if unit == 'h':
        convert_time_to_ms = 3600 * 1000
    elif unit == 'm':
        convert_time_to_ms = 60 * 1000
    elif unit == 'd':
        convert_time_to_ms = 3600 * 1000 * 24

    end_time = int(round(time.time() * 1000))

    try:
        r = requests.get(url=url, params=params)
        data = r.json()
        data = pd.DataFrame(data=data, columns=columns).astype(float)
        data = data[data.columns[:]]
        start_time = int(data.tail(1)['date'].values[0])
        while start_time < end_time - number * convert_time_to_ms:
            params, url, columns = get_url_params_column(exchange=exchange, timeframe=timeframe, symbol=symbol,
                                                         start_time=start_time)
            r = requests.get(url=url, params=params)
            next_data = r.json()
            next_data = pd.DataFrame(data=next_data, columns=columns).astype(float)
            next_data = next_data[data.columns[:]]
            data = pd.concat([data, next_data], axis=0)
            data = data.reset_index(drop=True)
            start_time = int(data.tail(1)['date'].values[0])
        if is_tehran:
            data.date = pd.DatetimeIndex(pd.to_datetime(data['date'], unit='ms', yearfirst=True)).tz_localize(
                'UTC').tz_convert('Asia/Tehran')
        data = data.drop_duplicates(subset=['date'])
        if save_csv:
            data.to_csv(f'{symbol}-{timeframe}-{exchange.name}.csv', index=False)
        return data
    except Exception as e:
        print(f'something wrong on get data from {exchange.name}:\n', e)


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


def get_candle_binance(symbol: str, timeframe: str, limit: int):
    params = {'interval': timeframe, 'symbol': symbol, 'limit': limit}
    url = 'https://api1.binance.com/api/v3/klines'
    try:
        r = requests.get(url=url, params=params)
        data = r.json()
        data = pd.DataFrame(data=data, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                                'Qav', 'trade-number', 'TBbav', 'TBbqv', 'ignore']).astype(float)
        data = data[data.columns[0:6]]
        data.date = pd.DatetimeIndex(pd.to_datetime(data['date'], unit='ms', yearfirst=True)).tz_localize(
            'UTC').tz_convert(
            'Asia/Tehran')
        return True, data
    except Exception as e:
        result = 'something wrong getting data from binance:\n' + str(e)
        return False, result


# usage
# ex = Exchange.binance
# sym = Symbols.BTCUSDT
# get_all_candles_binance(exchange=ex, symbol=sym, number=15, unit='m')
