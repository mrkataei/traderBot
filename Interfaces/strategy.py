import pandas as pd
import pandas_ta as ta
import numpy as np
from Inc import db, functions
from Telegram.Client.message import broadcast_messages


class Strategy:
    def __init__(self):
        print("sa")

    def signal(self, *args):
        raise Exception("NotImplementedException")

    def cross_over(self, x, y):
        return True if x[0] < y < x[1] else False

    def cross_under(self, x, y):
        return True if x[0] > y > x[1] else False

    def broadcast_and_insert_database(self):
        functions.set_recommendation(analysis_id=1, coin_id=coin_id, timeframe_id=timeframe_id, position=position,
                                     target_price=target_price, current_price=close, cost_price=cost, risk=result[1])
        broadcast_messages(coin_id=coin_id, analysis_id=1, timeframe_id=timeframe_id, position=position,
                           target_price=target_price, current_price=close, risk=result[1])
