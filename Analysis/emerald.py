"""
Mr.Kataei 11/12/2021
"""
import pandas as pd
from Libraries.pattern import *
from Inc.functions import get_recommendations, set_recommendation
from Telegram.Client.message import broadcast_messages
from Libraries.pattern import Patterns


class Emerald(Patterns):
    def __init__(self, data: pd.DataFrame, gain: float, cost: float, coin_id: int, timeframe_id: int, bot_ins):
        Patterns.__init__(self, dataframe=data)
        self.gain = gain
        self.cost = cost
        self.coin_id = coin_id
        self.timeframe_id = timeframe_id
        self.bot = bot_ins

    def get_old_position(self):
        try:
            query = get_recommendations(analysis_id=1, timeframe_id=self.timeframe_id, coin_id=self.coin_id)
            old_position = query[0][2]
            # when no rows in database
        except Exception as e:
            old_position = 'sell'
            # print(e)
        return old_position

    def broadcast(self, position: str, current_price: float, target_price: float):
        broadcast_messages(coin_id=self.coin_id, analysis_id=1, timeframe_id=self.timeframe_id, position=position,
                           target_price=target_price, current_price=current_price, risk='low', bot_ins=self.bot)

    def insert_database(self, position: str, current_price: float, target_price: float):
        set_recommendation(analysis_id=1, coin_id=self.coin_id, timeframe_id=self.timeframe_id, position=position,
                           target_price=target_price, current_price=current_price, cost_price=self.cost, risk='low')

    def signal(self):
        last_row_pattern_detector = self.get_recommendations().tail(1)
        position = last_row_pattern_detector['recommendation'].values[0]
        old_position = self.get_old_position()
        if old_position != position:
            close = float(last_row_pattern_detector['close'].values[0])
            if position == 'buy':
                target_price = close * self.gain + close
                self.broadcast(position=position, current_price=close, target_price=target_price)
                self.insert_database(position=position, current_price=close, target_price=target_price)
            elif position == 'sell':
                target_price = -close * self.gain + close
                self.broadcast(position=position, current_price=close, target_price=target_price)
                self.insert_database(position=position, current_price=close, target_price=target_price)

