"""
Mr.Kataei 8/4/2021
get_candle_api use in stream to get candles for analysis and strategies this method have limit for n last candles
you need for analysis.data collect form Bitfinex API where url can change for any API you want.
there is 3 type of dictionary for bitfinex symbols or CSvs we need to save
_get_all_candles is private method to use in generate_big_data where collect all data that can get from bitfinex

"""
import time
import pandas as pd
from requests import RequestException, get
import enum


class Exchange(enum.Enum):
    binance = 'binance'
    bitfinex = 'bitfinex'
    nobitex = 'nobitex'


class Symbols(enum.Enum):
    BTCUSDT = 'bitcoin'
    ETHUSDT = 'ethereum'
    ADAUSDT = 'cardano'
    DOGEUSDT = 'doge'
    BCHUSDT = 'bitcoinCash'
    ETCUSDT = 'ethereumClassic'


symbols = {'BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOGEUSDT', 'BCHUSDT', 'ETCUSDT'}

symbols_bitfinix = {'BTCUSDT': 'tBTCUST', 'ETHUSDT': 'tETHUST', 'ADAUSDT': 'tADAUST', 'DOGEUSDT': 'tDOGE:UST',
                    'BCHUSDT': 'tBCHN:UST', 'ETCUSDT': 'tETCUST'}

nobitex_timeframes = {'1h': '60', '3h': '180', '6h': '360', '12h': '720', '1d': 'D', '2d': '2D', '3d': '3D'}

bitfinex_timeframes = {'1m': '1m', '5m': '5m', '15m': '15m', '30m': '30m', '1h': '1h', '3h': '3h', '6h': '6h',
                       '12h': '12h', '1d': '1D', '1w': '1W', '14d': '14D', '1M': '1M'}

binance_timeframes = {'1m': '1m', '5m': '5m', '15m': '15m', '30m': '30m', '1h': '1h', '2h': '2h', '4h': '4h',
                      '6h': '6h', '8h': '8h', '12h': '12h', '1d': '1d', '3d': '3d', '1w': '1w', '1M': '1M'}


def get_ohclv_dataframe(exchange: Exchange, timeframe: str, symbol: str, start_time: int = 1151335200000):
    # 115133520000 is Wednesday, 21 December 2005 02:52:00
    if exchange.name == Exchange.binance.name:
        try:
            timeframe = binance_timeframes[timeframe]
        except KeyError:
            print('invalid timeframe for binance switching to 4hour timeframe ...')
            timeframe = '4h'
        params = {'interval': timeframe, 'symbol': symbol, 'limit': 1000, 'startTime': start_time}
        url = 'https://api1.binance.com/api/v3/klines'
        columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'Qav', 'trade-number', 'TBbav',
                   'TBbqv', 'ignore']
        try:
            r = get(url=url, params=params)
            data = r.json()
            data = pd.DataFrame(data=data, columns=columns).astype(float)
        except RequestException as e:
            print(e)
            return

    elif exchange.name == Exchange.bitfinex.name:
        try:
            timeframe = bitfinex_timeframes[timeframe]
        except KeyError:
            print('invalid timeframe for bitfinex switching to 4hour timeframe ...')
            timeframe = '4h'
        symbol = symbols_bitfinix[symbol]
        params = {'limit': 10000, 'sort': 1, 'start': start_time}
        print(timeframe, symbol)
        url = f'https://api-pub.bitfinex.com/v2/candles/trade:{timeframe}:{symbol}/hist'
        columns = ['date', 'open', 'close', 'high', 'low', 'volume']
        try:
            r = get(url=url, params=params)
            data = r.json()
            data = pd.DataFrame(data=data, columns=columns).astype(float)
        except RequestException as e:
            print(e)
            return
    elif exchange.name == Exchange.nobitex.name:
        start_time = int(start_time / 1000)  # ms convert to s
        url = 'https://api.nobitex.ir/market/udf/history'
        try:
            resolution = nobitex_timeframes[timeframe]
        except KeyError:
            print('invalid timeframe for nobitex switching to 1hour timeframe ...')
            resolution = 'D'
        params = {'symbol': symbol, 'resolution': resolution, 'from': start_time}
        print(symbol, resolution, start_time)
        try:
            r = get(url=url, params=params)
            data = r.json()
            # print(data'1160120967, 115133520')
            if data['s'] == 'ok':
                data = pd.DataFrame(
                    {'date': data['t'], 'close': data['c'], 'open': data['o'], 'high': data['h'],
                     'low': data['l'], 'volume': data['v']}).astype(float)
                data['date'] = data['date'] * 1000
            else:
                return
        except RequestException as e:
            print(e)
            return
    else:
        return
    return data


def calculate_end_time(number: int = 4, unit: str = 'h'):
    convert_time_to_ms = 0
    if unit == 'h':
        convert_time_to_ms = 3600 * 1000
    elif unit == 'm':
        convert_time_to_ms = 60 * 1000
    elif unit == 'd' or unit == 'D':
        convert_time_to_ms = 3600 * 1000 * 24
    elif unit == 'w':
        convert_time_to_ms = 3600 * 24 * 7 * 1000
    elif unit == 'M':
        convert_time_to_ms = 3600 * 24 * 30 * 1000  # bug infinite loop

    end_time = int(round(time.time() * 1000))
    return end_time - number * convert_time_to_ms


def get_all_candles(exchange: Exchange, symbol: Symbols, number: int = 4, unit: str = 'h',
                    is_tehran: bool = True, save_csv: bool = True):
    """
    :param exchange: its enum from Exchange ( bitfinex , binance ,...)
    :param symbol: its enum from Symbols
    :param number: its int number number of day or hours or minutes
    :param unit: its string for which timeframe,  m for minutes , h for hours , d for day
    :param is_tehran: for casting to tehran time this parameter need to be true
    :param save_csv:  for save data to directory calls this function needs to be true
    :return: dataframe of ohcl
    """
    timeframe = str(number) + unit
    symbol = symbol.name
    data = get_ohclv_dataframe(exchange=exchange, timeframe=timeframe, symbol=symbol)
    if data is None:
        return
    end_time = calculate_end_time(number=number, unit=unit)
    try:
        start_time = int(data.tail(1)['date'].values[0])
        while start_time < end_time:
            next_data = get_ohclv_dataframe(exchange=exchange, timeframe=timeframe, symbol=symbol,
                                            start_time=start_time)
            data = pd.concat([data, next_data], axis=0)
            data = data.reset_index(drop=True)
            start_time = int(data.tail(1)['date'].values[0])
            print(data)
        if is_tehran:
            data.date = pd.DatetimeIndex(pd.to_datetime(data['date'], unit='ms', yearfirst=True)).tz_localize(
                'UTC').tz_convert('Asia/Tehran')
        data = data.drop_duplicates(subset=['date'])
        if exchange.name == 'nobitex':
            data = data.loc[(data['close'] != 0.0)]  # for handle nobitex data empty data
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
        r = get(url=url, params=params)
        data = r.json()
        data = pd.DataFrame(data=data, columns=['date', 'open', 'close', 'high', 'low', 'volume'])
        data.date = pd.DatetimeIndex(pd.to_datetime(data['date'], unit='ms', yearfirst=True)
                                     ).tz_localize('UTC').tz_convert('Asia/Tehran')
        data = data.iloc[::-1]
        data = data.reset_index(drop=True)
        return data
    except Exception as e:
        print('something wrong on get data from bitfinex:\n', e)


def get_candle_binance(symbol: str, limit: int, number: int = 4, unit: str = 'h', open_want: bool = False):
    timeframe = str(number) + unit
    end_time = calculate_end_time(number=number, unit=unit)
    if open_want:
        params = {'interval': timeframe, 'symbol': symbol, 'limit': limit}
    else:
        params = {'interval': timeframe, 'symbol': symbol, 'limit': limit, 'endTime': end_time}
    url = 'https://api1.binance.com/api/v3/klines'
    try:
        r = get(url=url, params=params)
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


def get_candle_nobitex(symbol: Symbols, number: int = 1, unit: str = 'h', start_time: int = 1560120967,
                       end_time: int = 1562230967):
    timeframe = str(number) + unit
    try:
        resolution = nobitex_timeframes[timeframe]
    except KeyError:
        resolution = '60'
    url = 'https://api.nobitex.ir/market/udf/history'
    params = {'symbol': symbol.name, 'resolution': resolution, 'from': start_time, 'to': end_time}
    try:
        r = get(url=url, params=params)
        data = r.json()
        if data['s'] == 'ok':
            data = pd.DataFrame({'date': data['t'], 'close': data['c'], 'open': data['o'], 'high': data['h'],
                                 'low': data['l'], 'volume': data['v']})
            data.date = pd.DatetimeIndex(pd.to_datetime(data['date'], unit='s', yearfirst=True)).tz_localize(
                'UTC').tz_convert(
                'Asia/Tehran')
            data = data.loc[(data['close'] != 0.0)]  # for handle nobitex data empty data
            return True, data
    except Exception as e:
        result = 'something wrong getting data from nobitex:\n' + str(e)
        return False, result
    else:
        result = 'bad results'
        return False, result


if __name__ == '__main__':
    pass
# usage
# ex = Exchange.binance
# sym = Symbols.BTCUSDT
# get_all_candles(exchange=ex, symbol=sym, number=4, unit='h')
