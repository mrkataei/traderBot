"""
Mr.Kataei 8/4/2021
tradingview api signals
"""
from tradingview_ta import TA_Handler, Interval


def get_time_interval(time):
    return {
        'day': Interval.INTERVAL_1_DAY,
        '1hour': Interval.INTERVAL_1_HOUR,
        '4hour': Interval.INTERVAL_4_HOURS,
        '30min': Interval.INTERVAL_15_MINUTES,
    }.get(time, Interval.INTERVAL_15_MINUTES)


def tradingview_recommendations(symbol: str, timeframe: str, *option: str):
    ta = TA_Handler(symbol=symbol, screener='crypto', exchange='BINANCE',
                    interval=get_time_interval(timeframe))
    res = []
    for opt in option:
        res.append({'summary': ta.get_analysis().summary,
                       'MA': ta.get_analysis().moving_averages,
                       'OSI': ta.get_analysis().oscillators
                    }.get(opt, ta.get_analysis().summary))
    return res

