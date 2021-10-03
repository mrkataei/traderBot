""""
Mr.Kataei 8/7/2021
get symbol detail with timeframes this detail doesn't need API-KEY from binance
detail : percent of candle ( close - open)*100/open
"""
from binance.client import Client
import pandas as pd
from Libraries.definitions import *

_client = Client()


def get_interval_client(timeframe: str):
    return {
        '1min': _client.KLINE_INTERVAL_1MINUTE,
        '3min': _client.KLINE_INTERVAL_3MINUTE,
        '5min': _client.KLINE_INTERVAL_5MINUTE,
        '15min': _client.KLINE_INTERVAL_15MINUTE,
        '30min': _client.KLINE_INTERVAL_30MINUTE,
        '1hour': _client.KLINE_INTERVAL_1HOUR,
        '2hour': _client.KLINE_INTERVAL_2HOUR,
        '4hour': _client.KLINE_INTERVAL_4HOUR,
        '6hour': _client.KLINE_INTERVAL_6HOUR,
        '8hour': _client.KLINE_INTERVAL_8HOUR,
        '12hour': _client.KLINE_INTERVAL_12HOUR,
        '1day': _client.KLINE_INTERVAL_1DAY,
        '3day': _client.KLINE_INTERVAL_3DAY,
        'weekly': _client.KLINE_INTERVAL_1WEEK,
        'monthly': _client.KLINE_INTERVAL_1MONTH,

    }.get(timeframe, _client.KLINE_INTERVAL_1MINUTE)


def get_candle_details(symbol: str, timeframe: str):
    symbol = symbol.upper()
    timeframe = get_interval_client(timeframe)
    data = pd.DataFrame(_client.get_klines(symbol=symbol, interval=timeframe, limit=1)).values
    return data


def get_percent_candle(symbol: str, timeframe: str):
    data = get_candle_details(symbol, timeframe)
    percent = (float(data[0, 4]) - float(data[0, 1])) * 100 / float(data[0, 1])
    percent = round(percent, 3)
    return percent


def candle_details_to_string(symbol: str, timeframe: str):
    data = get_candle_details(symbol, timeframe)
    # calculate time in first row and first col to Tehran time
    time = pd.to_datetime(data[0, 0], unit='ms', yearfirst=True).tz_localize('UTC').tz_convert('Asia/Tehran')
    percent = (float(data[0, 4]) - float(data[0, 1])) * 100 / float(data[0, 1])
    percent = round(percent, 3)
    open_p = round(float(data[0, 1]), 4)
    high_p = round(float(data[0, 2]), 4)
    low_p = round(float(data[0, 3]), 4)
    close_p = round(float(data[0, 4]), 4)
    volume_p = round(float(data[0, 5]), 4)
    if percent > 0:
        emoji = "🤑" + symbol + "\n🟢"
    else:
        emoji = "😰" + symbol + "\n🔴"
    text = emoji + str(percent) + "%\n" + "⏱" + trans('C_timeframe') + " " + timeframe + "\n" \
           + trans('C_open_time') + str(time) + "\n" + trans('C_open') + str(open_p) + "$\n" \
           + trans('C_high') + str(high_p) + "$\n" + trans('C_low') + str(low_p) + "$\n" \
           + trans('C_close') + str(close_p) + "$\n" + trans('C_volume') + str(volume_p) + "\n" \
           + trans('C_number_trades') + str(data[0, 8])
    return text
