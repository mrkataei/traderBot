import pandas as pd
import pandas_ta as ta
import numpy as np
from Inc import db, functions
from Telegram.Client.message import broadcast_messages


class Tools():

    def __init__(self, analysis_id: int, timeframe_id: int ,coin_id: int):
        self.analysis_id = analysis_id
        self.timeframe_id = timeframe_id
        self.coin_id = coin_id

    def cross_over(self, x, y):
        return True if x[0] < y < x[1] else False

    def cross_under(self, x, y):
        return True if x[0] > y > x[1] else False

    def target_price(self, close: float, gain: float, result: tuple):
        return close * gain + close if result[0] else -close * gain + close

    def get_last_data(self, connection, start_position: bool = None):
        query = functions.get_recommendations(connection, coin_id=self.coin_id, analysis_id=self.analysis_id,
                                              timeframe=self.timeframe_id)
        try:
            old_position = query[0][2]
            old_price = query[0][4]
            # when no rows in database
        except Exception as e:
            old_position = 'buy' if start_position else "sell"
            old_price = 0
            print(e)

        return old_position, old_price

    def signal_process(self, connection, close: float, gain: float, result: tuple, cost:float):
        target_price = self.target_price(close, gain, result)
        position = 'buy' if result[0] else 'sell'
        functions.set_recommendation(db_connection=connection, analysis_id=self.analysis_id,
                                     coin_id=self.coin_id, timeframe_id=self.timeframe_id, position=position,
                                     target_price=target_price, current_price=close,
                                     cost_price=cost, risk=result[1])
        broadcast_messages(connection=connection, analysis_id=self.analysis_id,
                           coin_id=self.coin_id, current_price=close,
                           target_price=target_price, risk=result[1], position=position,
                           timeframe_id=self.timeframe_id)
