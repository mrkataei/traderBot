import pandas as pd
import pandas_ta as ta
import numpy as np
from Inc import db, functions
from Telegram.Client.message import broadcast_messages


# from Telegram import message


def cross_over(x, y):
    return True if x[0] < y < x[1] else False


def cross_under(x, y):
    return True if x[0] > y > x[1] else False


def signal(data: pd.DataFrame, gain: float, cost: float, coin_id: int, timeframe_id: int, settings: dict):
    delay = settings['analysis_setting']['delay']
    safe_line = settings['analysis_setting']['safe_line']
    hist_line = settings['analysis_setting']['hist_line']
    slow = settings['indicators_setting']['MACD']['slow']
    sign = settings['indicators_setting']['MACD']['signal']
    fast = settings['indicators_setting']['MACD']['fast']
    connection = db.con_db()
    # create macd dataframe macd has 3 column original macd , histogram  and signal
    macd_df = ta.macd(close=data['close'], slow=slow, fast=fast, signal=sign)
    macd_df.columns = ["macd", "histogram", "signal"]
    # add price of coin to the macd_df
    macd_df["close"] = data.close

    safe_line = safe_line / 100.0

    last_macd = np.array(macd_df.tail(2))
    close = float(last_macd[1, 3])
    try:
        query = functions.get_recommendations(analysis_id=2, timeframe=timeframe_id, coin_id=coin_id)
        old_position = query[0][2]
        old_price = query[0][4]
        # when no rows in database
    except Exception as e:
        old_position = 'sell'
        old_price = 0
        print(e)

    if cross_over(last_macd[:, 1], hist_line) and \
            last_macd[1, 0] < - safe_line and old_position == "sell":
        result = True, "medium"
        target_price = close * gain + close if result[0] else -close * gain + close
        position = 'buy' if result[0] else 'sell'
        functions.set_recommendation(analysis_id=2, coin_id=coin_id, timeframe_id=timeframe_id, position=position,
                                     target_price=target_price, current_price=close, cost_price=cost, risk=result[1])
        broadcast_messages(coin_id=coin_id, analysis_id=2, timeframe_id=timeframe_id, position=position,
                           target_price=target_price, current_price=close, risk=result[1])
    elif float(last_macd[1, 1]) < np.array(macd_df.tail(delay)["histogram"])[0] and \
            old_price < close and old_position == "buy":
        result = False, "medium"
        target_price = close * gain + close if result[0] else -close * gain + close
        position = 'buy' if result[0] else 'sell'
        functions.set_recommendation(analysis_id=2, coin_id=coin_id, timeframe_id=timeframe_id, position=position,
                                     target_price=target_price, current_price=close, cost_price=cost, risk=result[1])
        broadcast_messages(coin_id=coin_id, analysis_id=2, timeframe_id=timeframe_id, position=position,
                           target_price=target_price, current_price=close, risk=result[1])

