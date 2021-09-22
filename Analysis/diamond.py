import pandas as pd
import pandas_ta as ta
import numpy as np
from Inc import db, functions
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


def cross_under(x, y):
    return True if x[0] > y > x[1] else False


valid_coins_and_times = {
    'coins':
        {
            1: {'timeframes': {3}},
            2: {'timeframes': {3}},
            3: {'timeframes': {3}},
            4: {'timeframes': {1}},
            5: {'timeframes': {3}}
        }
}


def gold_signal(data: pd.DataFrame, gain: float, cost: float, coin_id: int, timeframe_id: int, setting: dict):
    if coin_id in valid_coins_and_times['coins'] \
            and timeframe_id in valid_coins_and_times['coins'][coin_id]['timeframes']:
        connection = db.con_db()
        # macd
        slow = setting['indicators_settings']['MACD']['slow']
        sign = setting['indicators_settings']['MACD']['sign']
        fast = setting['indicators_settings']['MACD']['fast']
        macd_source = setting['indicators_settings']['MACD']['source']

        # rsi
        rsi_source = setting['indicators_settings']['RSI']['source']
        rsi_length = setting['indicators_settings']['RSI']['length']
        rsi_source = get_source(data=data, source=rsi_source)

        # stoch
        stoch_k = setting['indicators_settings']['stoch']['k']
        stoch_d = setting['indicators_settings']['stoch']['d']
        stoch_smooth = setting['indicators_settings']['stoch']['smooth']

        # stoch_rsi
        stoch_rsi_rsi_length = setting['indicators_settings']['stochrsi']['rsi_length']
        stoch_rsi_length = setting['indicators_settings']['stochrsi']['length']
        stoch_rsi_k = setting['indicators_settings']['stochrsi']['k']
        stoch_rsi_d = setting['indicators_settings']['stochrsi']['d']
        stoch_rsi_source = setting['indicators_settings']['stochrsi']['source']
        stoch_rsi_source = get_source(data=data, source=stoch_rsi_source)

        # signal parameters
        stoch_k_oversell = setting['analysis_setting']['stoch_k_oversell']
        stoch_k_overbuy = setting['analysis_setting']['stoch_k_overbuy']
        stoch_rsi_k_overbuy = setting['analysis_setting']['stoch_rsi_k_overbuy']
        stoch_rsi_k_oversell = setting['analysis_setting']['stoch_rsi_k_oversell']
        rsi_oversell = setting['analysis_setting']['rsi_oversell']
        rsi_overbuy = setting['analysis_setting']['rsi_overbuy']

        # macd dataframe
        macd_source = get_source(data=data, source=macd_source)
        macd_df = ta.macd(close=macd_source, slow=slow, fast=fast, signal=sign)
        close = np.array(data.tail(1)["close"])[0]
        last_macd = np.array(macd_df.tail(2))

        # RSI series
        rsi_source = get_source(data=data, source=rsi_source)
        rsi_sr = ta.rsi(close=rsi_source, length=rsi_length)
        last_rsi = np.array(rsi_sr.tail(1))

        # STOCHASTIC data
        stoch_df = ta.stoch(high=data['high'], low=data['low'], close=data['close'],
                            k=stoch_k, d=stoch_d, smooth_k=stoch_smooth)
        last_stoch = np.array(stoch_df.tail(1))

        # STOCHASTIC RSI dataframe
        stoch_rsi_df = ta.stochrsi(close=stoch_rsi_source, length=stoch_rsi_length,
                                   rsi_length=stoch_rsi_rsi_length, k=stoch_rsi_k, d=stoch_rsi_d)
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
            if last_stoch[0, 0] < stoch_k_oversell and last_stoch_rsi[0, 0] < stoch_rsi_k_oversell:
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
