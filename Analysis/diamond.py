"""
Arman hajimirza

database configure :

        valid for all coins
        timeframe_id -> 1=30min , 2=1hour ,3=4hour ,4=1day
         coin_id:  valid_timeframes:
                1:      timeframes: {3}
                2:      timeframes: {3}
                3:      timeframes: {3}
                4:      timeframes: {1}
                5:      timeframes: {3}
                6:      timeframes: {3}
        analysis_id -> 3=diamond

use this query for get user who have this signal with this coin and time:
        users = functions.get_user_recommendation(connection, coin_id=1,analysis_id=1, timeframe_id=1)
and get chat_id for notify them with this query :
        chat_id = functions.get_user_chat_id(connection , user[0])
all of this in Telegram/message just use broadcast method

"""

import pandas as pd
import pandas_ta as ta
# import numpy as np
# from Libraries.tools import get_source
# from Telegram.Client.message import broadcast_messages
# from Trade import spot
from Libraries.macd import macd_indicator
# import datetime
# from Inc.functions import get_recommendations, set_recommendation
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

symbols_bitfinix = {'BTCUSDT': 'tBTCUSD', 'ETHUSDT': 'tETHUSD', 'ADAUSDT': 'tADAUSD', 'DOGEUSDT': 'tDOGE:USD',
                    'BCHUSDT': 'tBCHN:USD', 'ETCUSDT': 'tETCUSD'}
valid_coins_and_times = {
    'coins':
        {
            1: {'timeframes': {3}},
            2: {'timeframes': {3}},
            3: {'timeframes': {3}},
            4: {'timeframes': {1}},
            5: {'timeframes': {3}},
            6: {'timeframes': {3}}
        }
}


class Diamond:

    def __init__(self, data: pd.DataFrame, gain: float, cost: float, coin_id: int, timeframe_id: int, bot_ins,
                 setting: dict):
        self.data = data
        self.gain = gain
        self.cost = cost
        self.coin_id = coin_id
        self.timeframe_id = timeframe_id
        self.bot = bot_ins
        self.setting = setting
        self.macd_setting = setting['indicators_setting']['MACD']
        self.rsi_setting = setting['indicators_setting']['RSI']
        self.stoch_setting = setting['indicators_setting']['stoch']
        self.stochrsi_setting = setting['indicators_setting']['stochrsi']

        statics_setting = setting['analysis_setting']
        self.stoch_k_oversell = statics_setting['stoch_k_oversell']
        self.stoch_k_overbuy = statics_setting['stoch_k_overbuy']
        self.stoch_rsi_k_overbuy = statics_setting['stoch_rsi_k_overbuy']
        self.stoch_rsi_k_oversell = statics_setting['stoch_rsi_k_oversell']
        self.rsi_oversell = statics_setting['rsi_oversell']
        self.rsi_overbuy = statics_setting['rsi_overbuy']

        self.preprocess()

    def preprocess(self):
        slow = self.macd_setting['slow']
        sign = self.macd_setting['signal']
        fast = self.macd_setting['fast']
        macd_source = self.macd_setting['source']
        macd_source = get_source(data=self.data, source=macd_source)

        # rsi
        rsi_source = self.rsi_setting['source']
        rsi_length = self.rsi_setting['length']
        rsi_source = get_source(data=self.data, source=rsi_source)

        # stoch
        stoch_k = self.stoch_setting['k']
        stoch_d = self.stoch_setting['d']
        stoch_smooth = self.stoch_setting['smooth']

        # stoch_rsi
        stoch_rsi_rsi_length = self.stochrsi_setting['rsi_length']
        stoch_rsi_length = self.stochrsi_setting['length']
        stoch_rsi_k = self.stochrsi_setting['k']
        stoch_rsi_d = self.stochrsi_setting['d']
        stoch_rsi_source = self.stochrsi_setting['source']
        stoch_rsi_source = get_source(data=self.data, source=stoch_rsi_source)

        # signal parameters

        macd_df = macd_indicator(close=macd_source, slow=slow, fast=fast, matype="sma", signal=sign)
        rsi_sr = ta.rsi(close=rsi_source, length=rsi_length)
        stoch_df = self.data.ta.stoch(k=stoch_k, d=stoch_d, smooth_k=stoch_smooth)
        stoch_rsi_df = ta.stochrsi(close=stoch_rsi_source, length=stoch_rsi_length, rsi_length=stoch_rsi_rsi_length,
                                   k=stoch_rsi_k, d=stoch_rsi_d)
        temp = pd.concat([macd_df, rsi_sr, stoch_df, stoch_rsi_df], axis=1)
        temp.columns = ["macd", "histogeram", "signal", "rsi", "stoch_k", "stoch_d", "stochrsi_k", "stochrsi_d"]

        temp = pd.concat([self.data, temp], axis=1)

        temp["macd1"] = temp['macd'].shift(periods=1)

        temp = temp.dropna()

        temp = temp.reset_index(drop=True)
        temp["crossover"] = ta.cross(series_a=temp["stochrsi_k"], series_b=temp["stochrsi_d"])
        temp["crossunder"] = ta.cross(series_a=temp["stochrsi_k"], series_b=temp["stochrsi_d"], above=False)

        self.data = temp

    #
    # def get_old_position(self):
    #     query = get_recommendations(analysis_id=3, timeframe_id=self.timeframe_id, coin_id=self.coin_id)
    #     if query:
    #         old_position = query[0][2]
    #     else:
    #         old_position = 'sell'
    #     return old_position
    #
    # def get_old_price(self):
    #     query = get_recommendations(analysis_id=3, timeframe_id=self.timeframe_id, coin_id=self.coin_id)
    #     if query:
    #         old_price = query[0][4]
    #     else:
    #         old_price = 0
    #     return old_price

    # def broadcast(self, position: str, current_price: float, target_price: float, risk: str):
    #     broadcast_messages(coin_id=self.coin_id, analysis_id=3, timeframe_id=self.timeframe_id, position=position,
    #                        target_price=target_price, current_price=current_price, risk='risk', bot_ins=self.bot)
    #
    # def insert_database(self, position: str, current_price: float, target_price: float, risk: str):
    #     set_recommendation(analysis_id=3, coin_id=self.coin_id, timeframe_id=self.timeframe_id, position=position,
    #                        target_price=target_price, current_price=current_price, cost_price=self.cost, risk=risk)

    def _set_recommendation(self, position: str, risk: str, index):
        self.data.loc[index, 'recommendation'] = position
        self.data.loc[index, 'risk'] = risk

    def get_recommendations(self):
        self.signal_detector()
        return self.data[['date', 'open', 'high', 'close', 'low', 'risk', 'recommendation']].copy()

    def diamond(self, row):

        macd = row["macd"]
        rsi = row["rsi"]
        stoch_k = row["stoch_k"]
        stochrsi_k = row["stochrsi_k"]
        macd1 = row["macd1"]
        crossover = row["crossover"]
        crossunder = row["crossunder"]

        buy_counter = 0
        sell_counter = 0

        # check stoch_k < stoch_k_oversell and stoch_rsi_k < stoch_rsi_k_oversell
        if stoch_k < self.stoch_k_oversell and stochrsi_k < self.stoch_rsi_k_oversell:
            buy_counter += 2
        # check rsi < rsi_oversell
        if rsi < self.rsi_oversell:
            buy_counter += 1
        # check crossOver
        if crossover == 1:
            buy_counter += 1
        # check macd < 0 and macd > macd[1]
        if macd1 < macd < 0:
            buy_counter += 1
        # buy signal operation
        if buy_counter > 3:
            if buy_counter == 4:
                self._set_recommendation(position="buy", risk="high", index=row.name)
            else:
                self._set_recommendation(position="buy", risk='mediom', index=row.name)
            # add signal to database
        # check stoch_k > stoch_k_oversell and stoch_rsi_k > stoch_rsi_k_oversell
        if stoch_k > self.stoch_k_overbuy and stochrsi_k > self.stoch_rsi_k_overbuy:
            sell_counter += 2
        # check rsi < rsi_overbuy
        if rsi < self.rsi_overbuy:
            sell_counter += 1
        # check crossunder
        if crossunder == 1:
            sell_counter += 1
        # macd > 0 and macd < macd[1]
        if 0 < macd < macd1:
            sell_counter += 1
        if sell_counter > 3:
            if sell_counter == 4:
                self._set_recommendation(position="sell", risk='high', index=row.name)
            else:
                self._set_recommendation(position="sell", risk='mediom', index=row.name)

    def signal_detector(self):
        self.data.apply(lambda row: self.diamond(row), axis=1)

    # def signal(self):
    #     last_row_diamond_detector = self.get_recommendations().tail(1)
    #     position = last_row_diamond_detector['recommendation'].values[0]
    #     old_position = self.get_old_position()
    #     old_price = self.get_old_price()
    #     if old_position != position:
    #         close = float(last_row_diamond_detector['close'].values[0])
    #         if position == 'buy':
    #             target_price = close * self.gain + close
    #             self.broadcast(position=position, current_price=close, target_price=target_price,
    #                            risk=last_row_diamond_detector['risk'].values[0])
    #             self.insert_database(position=position, current_price=close, target_price=target_price,
    #                                  risk=last_row_diamond_detector['risk'].values[0])
    #         elif position == 'sell' and old_price < close:
    #             target_price = -close * self.gain + close
    #             self.broadcast(position=position, current_price=close, target_price=target_price,
    #                            risk=last_row_diamond_detector['risk'].values[0])
    #             self.insert_database(position=position, current_price=close, target_price=target_price,
    #                                  risk=last_row_diamond_detector['risk'].values[0])


# df = pd.read_csv(r"C:\Users\Asus\Downloads\bitcoin-pattern-reco-1min.csv")
# df = df[['date', 'open', 'high', 'close', 'low', "volume"]]
# df = df.tail(10000)
# print(df)
# settings = {'analysis_setting': {'stoch_k_oversell': 29, 'stoch_k_overbuy': 86, 'stoch_rsi_k_oversell': 16,
#                                  'stoch_rsi_k_overbuy': 86, 'rsi_oversell': 39, 'rsi_overbuy': 64},
#             'indicators_setting': {'RSI': {'length': 4, 'source': 'close'}, 'stoch': {'k': 22, 'd': 3, 'smooth': 3},
#                                    'stochrsi': {'k': 3, 'd': 3, 'rsi_length': 22, 'length': 11, 'source': 'ohlc4'},
#                                    'MACD': {'slow': 26, 'signal': 20, 'fast': 10, 'source': 'low', 'matype': 'ema'}}}
# # df = df.iloc[::-1]
# # # df = df.drop(columns=["tradecount"])
# # df = df.reset_index(drop=True)
# # print(df)
# pd.set_option('display.max_columns', None)
# a = Diamond(data=df, coin_id=1, timeframe_id=1, gain=1, bot_ins=1, setting=settings, cost=1)
# # print(a.data)
# # print(a.preprocess_data)
# # a.preprocess()
#
# a.signal_detector()
#
# df = a.get_recommendations()

# print(df)
