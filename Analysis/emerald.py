"""
Mr.Kataei 11/12/2021
"""
import pandas as pd
from Inc.functions import get_last_recommendations, set_recommendation, record_dictionary
from Telegram.Client.message import broadcast_messages
from Analysis.pattern import Patterns


class Emerald(Patterns):
    def __init__(self, data: pd.DataFrame, coin_id: int, timeframe_id: int, bot_ins):
        Patterns.__init__(self, dataframe=data)
        self.coin_id = coin_id
        self.timeframe_id = timeframe_id
        self.bot = bot_ins

    def get_old_position(self):
        record = get_last_recommendations(analysis_id=1, timeframe_id=self.timeframe_id,
                                          coin_id=self.coin_id)[0]
        if record:
            old_position = record_dictionary(record=record, table='recommendations')['position']
        else:
            old_position = 'sell'
        return old_position

    def broadcast(self, position: str, current_price: float):
        broadcast_messages(coin_id=self.coin_id, analysis_id=1, timeframe_id=self.timeframe_id, position=position,
                           current_price=current_price, risk='low', bot_ins=self.bot)

    def insert_database(self, position: str, current_price: float):
        set_recommendation(analysis_id=1, coin_id=self.coin_id, timeframe_id=self.timeframe_id, position=position,
                           risk='low', price=current_price)

    def signal(self):
        last_row_pattern_detector = self.get_recommendations().tail(1)
        position = last_row_pattern_detector['recommendation'].values[0]
        old_position = self.get_old_position()
        if old_position != position:
            close = float(last_row_pattern_detector['close'].values[0])
            if position == 'buy':
                self.broadcast(position=position, current_price=close)
                self.insert_database(position=position, current_price=close)
            elif position == 'sell':
                self.broadcast(position=position, current_price=close)
                self.insert_database(position=position, current_price=close)
