import string

import pandas as pd
import pandas_ta as ta
import numpy as np
from Inc import db, functions
from Telegram.Client.message import broadcast_messages


def cross_over(x, y):
    return True if x[0] < y < x[1] else False


def cross_under(x, y):
    return True if x[0] > y > x[1] else False


def gold_signal(data: pd.DataFrame, gain: float, cost: float, coin_id: int, timeframe_id: int, setting: dict):
    connection = db.con_db()
    window_slow = setting['indicators_settings']['MACD']['window_slow']
    window_sign = setting['indicators_settings']['MACD']['window_sign']
    window_fast = setting['indicators_settings']['MACD']['window_fast']

    rsi_column = setting['indicators_settings']['RSI']['rsi_column']
    rsi_period = setting['indicators_settings']['RSI']['rsi_period']

    window_stoch = setting['indicators_settings']['stoch']['window_stoch']
    smooth_window_stoch = setting['indicators_settings']['stoch']['smooth_window_stoch']
    stoch_length = setting['indicators_settings']['stoch']['stoch_length']

    stoch_rsi_length = setting['indicators_settings']['stochrsi']['stoch_rsi_length']
    window_stochrsi = setting['indicators_settings']['stochrsi']['window_stochrsi']
    smooth_window_stochrsi = setting['indicators_settings']['stochrsi']['smooth_window_stochrsi']

    stoch_k_oversell = setting['analysis_setting']['stoch_k_oversell']
    stoch_rsi_k_overbuy = setting['analysis_setting']['stoch_rsi_k_overbuy']
    rsi_oversell = setting['analysis_setting']['rsi_oversell']
    stoch_k_overbuy = setting['analysis_setting']['stoch_k_overbuy']
    stoch_rsi_k_ovesell = setting['analysis_setting']['stoch_rsi_k_ovesell']
    rsi_overbuy = setting['analysis_setting']['rsi_overbuy']
    # macd dataframe
    macd_df = pd.DataFrame(data.ta.macd(window_slow=window_slow, window_fast=window_fast, window_sign=window_sign))
    close = np.array(data.tail(1)["close"])[0]
    macd_df.columns = ["macd", "histogram", "signal"]
    last_macd = np.array(macd_df.tail(2))
    # RSI series
    rsi_sr = ta.rsi(data[rsi_column], length=rsi_period)
    last_rsi = np.array(rsi_sr.tail(1))

    # STOCHASTIC data
    stoch_df = data.ta.stoch(close="close", high='high', low='low', window=window_stoch,
                             smooth_window=smooth_window_stoch)
    last_stoch = np.array(stoch_df.tail(1))

    # STOCHASTIC RSI dataframe
    stoch_rsi_df = data.ta.stochrsi(length=stoch_length, rsi_length=stoch_rsi_length, window=window_stochrsi,
                                    smooth_window=smooth_window_stochrsi)
    last_stoch_rsi = np.array(stoch_rsi_df.tail(1))
    try:
        query = functions.get_recommendations(connection, coin_id=coin_id, analysis_id=3, timeframe=timeframe_id)
        old_position = query[0][2]
        old_price = query[0][4]
        # when no rows in database
    except Exception as e:
        old_position = 'sell'
        old_price = 0
        print(e)

    buy_counter = 0
    print("buy_counter:", buy_counter, "waiting for process...")
    if old_position == "sell":
        if last_stoch[0, 0] < stoch_k_oversell and last_stoch_rsi[0, 0] < stoch_rsi_k_ovesell:
            buy_counter += 2
        if last_rsi[0] < rsi_oversell:
            buy_counter += 1
        if cross_over(last_stoch_rsi[:, 0], last_stoch_rsi[0, 1]):
            buy_counter += 1
        if last_macd[0, 0] < last_macd[1, 0] < 0:
            buy_counter += 1
        print("buy_counter:", buy_counter)
    if buy_counter == 0:
        print("buy_counter:", buy_counter, "process done")
    if buy_counter > 3:
        result = True, "medium"
        target_price = close * gain + close if result[0] else -close * gain + close
        position = 'buy' if result[0] else 'sell'
        functions.set_recommendation(db_connection=connection, analysis_id=3,
                                     coin_id=coin_id, timeframe_id=timeframe_id, position=position,
                                     target_price=target_price, current_price=close,
                                     cost_price=cost, risk=result[1])
        broadcast_messages(connection=connection, analysis_id=2,
                           coin_id=coin_id, current_price=close,
                           target_price=target_price, risk=result[1], position=position,
                           timeframe_id=timeframe_id)

    sell_counter = 0
    print("sell_counter:", sell_counter, "waiting for process...")
    if old_position == "buy" and old_price < close:
        if last_stoch[0, 0] > stoch_k_overbuy and last_stoch_rsi[0, 0] > stoch_rsi_k_overbuy:
            sell_counter += 2
        if last_rsi[0] < rsi_overbuy:
            sell_counter += 1
        if cross_under(last_stoch_rsi[:, 0], last_stoch_rsi[0, 1]):
            sell_counter += 1
        if 0 < last_macd[1, 0] < last_macd[0, 0]:
            sell_counter += 1
        print("sell_counter:", sell_counter)
    if sell_counter == 0:
        print("sell_counter:", sell_counter, "process done")
    if sell_counter > 3:
        result = False, "medium"
        target_price = close * gain + close if result[0] else -close * gain + close
        position = 'buy' if result[0] else 'sell'
        functions.set_recommendation(db_connection=connection, analysis_id=3,
                                     coin_id=coin_id, timeframe_id=timeframe_id, position=position,
                                     target_price=target_price, current_price=close,
                                     cost_price=cost, risk=result[1])
        broadcast_messages(connection=connection, analysis_id=2,
                           coin_id=coin_id, current_price=close,
                           target_price=target_price, risk=result[1], position=position,
                           timeframe_id=timeframe_id)
