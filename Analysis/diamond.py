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
import numpy as np
from Libraries.tools import Tools, get_source, cross_over, cross_under
from Libraries.macd import macd

ta.cross()
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


def signal(data: pd.DataFrame, gain: float, cost: float, coin_id: int, timeframe_id: int, setting: dict, bot_ins):
    diamond_tools = Tools(analysis_id=3, timeframe_id=timeframe_id, coin_id=coin_id)

    if coin_id in valid_coins_and_times['coins'] \
            and timeframe_id in valid_coins_and_times['coins'][coin_id]['timeframes']:
        # macd
        slow = setting['indicators_setting']['MACD']['slow']
        sign = setting['indicators_setting']['MACD']['signal']
        fast = setting['indicators_setting']['MACD']['fast']
        macd_source = setting['indicators_setting']['MACD']['source']
        macd_source = get_source(data=data, source=macd_source)

        # rsi
        rsi_source = setting['indicators_setting']['RSI']['source']
        rsi_length = setting['indicators_setting']['RSI']['length']
        rsi_source = get_source(data=data, source=rsi_source)

        # stoch
        stoch_k = setting['indicators_setting']['stoch']['k']
        stoch_d = setting['indicators_setting']['stoch']['d']
        stoch_smooth = setting['indicators_setting']['stoch']['smooth']

        # stoch_rsi
        stoch_rsi_rsi_length = setting['indicators_setting']['stochrsi']['rsi_length']
        stoch_rsi_length = setting['indicators_setting']['stochrsi']['length']
        stoch_rsi_k = setting['indicators_setting']['stochrsi']['k']
        stoch_rsi_d = setting['indicators_setting']['stochrsi']['d']
        stoch_rsi_source = setting['indicators_setting']['stochrsi']['source']
        stoch_rsi_source = get_source(data=data, source=stoch_rsi_source)

        # signal parameters
        stoch_k_oversell = setting['analysis_setting']['stoch_k_oversell']
        stoch_k_overbuy = setting['analysis_setting']['stoch_k_overbuy']
        stoch_rsi_k_overbuy = setting['analysis_setting']['stoch_rsi_k_overbuy']
        stoch_rsi_k_oversell = setting['analysis_setting']['stoch_rsi_k_oversell']
        rsi_oversell = setting['analysis_setting']['rsi_oversell']
        rsi_overbuy = setting['analysis_setting']['rsi_overbuy']

        # macd dataframe
        macd_df = macd(close=macd_source, slow=slow, fast=fast, matype="sma", signal=sign)
        close = float(np.array(data.tail(1)["close"])[0])
        # get last 2 positions of  macd df
        last_macd = np.array(macd_df.tail(2))

        # RSI series
        rsi_sr = ta.rsi(close=rsi_source, length=rsi_length)
        # get last  positions of  rsi sr
        last_rsi = np.array(rsi_sr.tail(1))

        # STOCHASTIC data
        stoch_df = data.ta.stoch(k=stoch_k, d=stoch_d, smooth_k=stoch_smooth)
        # get last  positions of  stoch df
        last_stoch = np.array(stoch_df.tail(1))

        # STOCHASTIC RSI dataframe
        stoch_rsi_df = ta.stochrsi(close=stoch_rsi_source, length=stoch_rsi_length,
                                   rsi_length=stoch_rsi_rsi_length, k=stoch_rsi_k, d=stoch_rsi_d)
        # get last 2 positions of  stochrsi df
        last_stoch_rsi = np.array(stoch_rsi_df.tail(2))

        # check last signal of analysis on db
        last_data = diamond_tools.get_last_data(start_position=False)
        old_position = last_data[0]
        old_price = last_data[1]

        buy_counter = 0
        if old_position == "sell":
            # check stoch_k < stoch_k_oversell and stoch_rsi_k < stoch_rsi_k_oversell
            if last_stoch[0, 0] < stoch_k_oversell and last_stoch_rsi[1, 0] < stoch_rsi_k_oversell:
                buy_counter += 2
            # check rsi < rsi_oversell
            if last_rsi[0] < rsi_oversell:
                buy_counter += 1
            # check crossOver
            if cross_over(last_stoch_rsi[:, 0], last_stoch_rsi[1, 1]):
                buy_counter += 1
            # check macd < 0 and macd > macd[1]
            if last_macd[0, 0] < last_macd[1, 0] < 0:
                buy_counter += 1
        # buy signal operation
        if buy_counter > 3:
            # calculate risk
            if buy_counter == 4:
                result = True, "medium"
            else:
                result = True, "high"
            # add signal to database
            diamond_tools.signal_process(close=close, gain=gain, result=result, cost=cost, bot_ins=bot_ins)

        sell_counter = 0
        if old_position == "buy" and old_price < close:
            # check stoch_k > stoch_k_oversell and stoch_rsi_k > stoch_rsi_k_oversell
            if last_stoch[0, 0] > stoch_k_overbuy and last_stoch_rsi[1, 0] > stoch_rsi_k_overbuy:
                sell_counter += 2
            # check rsi < rsi_overbuy
            if last_rsi[0] < rsi_overbuy:
                sell_counter += 1
            # check crossunder
            if cross_under(last_stoch_rsi[:, 0], last_stoch_rsi[1, 1]):
                sell_counter += 1
            # macd > 0 and macd < macd[1]
            if 0 < last_macd[1, 0] < last_macd[0, 0]:
                sell_counter += 1

        # sell signal operation
        if sell_counter > 3:
            if sell_counter == 4:
                result = False, "medium"
            else:
                result = False, "high"
            diamond_tools.signal_process(close=close, gain=gain, result=result, cost=cost, bot_ins=bot_ins)
