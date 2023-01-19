"""
Mr.Kataei 8/4/2021
tradingview api signals
"""
from tradingview_ta import TA_Handler

_ta = TA_Handler(screener='crypto', exchange='BINANCE')


def get_time_interval(time):
    return {
        '1day': '1d',
        '1hour': '1h',
        '4hour': '4h',
        '30min': '15m',
    }.get(time, '15m')


def tradingview_recommendations(symbol: str, timeframe: str, *option: str):

    _ta.set_symbol_as(symbol=symbol)
    _ta.set_interval_as(intvl=get_time_interval(timeframe))
    res = []
    for opt in option:
        res.append({'summary': _ta.get_analysis().summary,
                       'MA': _ta.get_analysis().moving_averages,
                       'OSI': _ta.get_analysis().oscillators
                    }.get(opt, _ta.get_analysis().summary))
    return res
