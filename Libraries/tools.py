import pandas as pd
import pandas_ta as ta
from Inc import functions
from Telegram.Client.message import broadcast_messages


def get_source(data: pd.DataFrame, source: str = 'close'):
    return {
        'hl2': data.ta.hl2(),
        'hlc3': data.ta.hlc3(),
        'ohlc4': data.ta.ohlc4(),
        'close': data['close'],
        'high': data['high'],
        'low': data['low'],
        'open': data['open']
    }.get(source, data['close'])


def cross_over(x, y):
    return True if x[0] < y < x[1] else False


def target_price(close: float, gain: float, result: tuple):
    return close * gain + close if result[0] else -close * gain + close


def cross_under(x, y):
    return True if x[0] > y > x[1] else False


class Tools:

    def __init__(self, analysis_id: int, timeframe_id: int, coin_id: int):
        self.analysis_id = analysis_id
        self.timeframe_id = timeframe_id
        self.coin_id = coin_id

    def get_last_data(self, start_position: bool = None):
        query = functions.get_recommendations(analysis_id=self.analysis_id, timeframe_id=self.timeframe_id,
                                              coin_id=self.coin_id)
        try:
            old_position = query[0][2]
            old_price = query[0][4]
            # when no rows in database
        except Exception as e:
            old_position = 'buy' if start_position else "sell"
            old_price = 0
            print(e)

        return old_position, old_price

    def signal_process(self, close: float, gain: float, result: tuple, cost: float):
        position = 'buy' if result[0] else 'sell'
        tp = target_price(close=close, gain=gain, result=result)
        functions.set_recommendation(analysis_id=self.analysis_id, coin_id=self.coin_id, timeframe_id=self.timeframe_id,
                                     position=position, target_price=tp, current_price=close, cost_price=cost,
                                     risk=result[1])
        broadcast_messages(analysis_id=self.analysis_id, coin_id=self.coin_id, current_price=close,
                           target_price=tp, risk=result[1], position=position, timeframe_id=self.timeframe_id)
