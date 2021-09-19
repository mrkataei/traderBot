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


def signal(data: pd.DataFrame, gain: float, cost: float, coin_id: int, timeframe_id: int, window_slow: int,
           window_fast: int, window_sign: int, delay: int, safeline: int ,histline: float):
    connection = db.con_db()
    # create macd dataframe macd has 3 column original macd , histogram  and signal
    macd_df = pd.DataFrame(data.ta.macd(window_slow=window_slow, window_fast=window_fast, window_sign=window_sign))
    macd_df.columns = ["macd", "histogram", "signal"]
    # add price of coin to the macd_df
    macd_df["close"] = data.close

    safe_line = safeline / 100.0

    last_macd = np.array(macd_df.tail(2))
    close = float(last_macd[1, 3])
    try:
        query = functions.get_recommendations(connection, coin_id=coin_id, analysis_id=2, timeframe=timeframe_id)
        old_position = query[0][2]
        old_risk = query[0][7]
        old_price = query[0][4]
        # when no rows in database
    except Exception as e:
        old_position = 'sell'
        old_risk = 'low'
        old_price = 0
        print(e)

    if cross_over(last_macd[:, 1], histline) and \
            last_macd[1, 0] < - safe_line and old_position == "sell":
        result = True, "medium"
        target_price = close * gain + close if result[0] else -close * gain + close
        position = 'buy' if result[0] else 'sell'
        functions.set_recommendation(db_connection=connection, analysis_id=2,
                                     coin_id=coin_id, timeframe_id=timeframe_id, position=position,
                                     target_price=target_price, current_price=close,
                                     cost_price=cost, risk=result[1])
        broadcast_messages(connection=connection, analysis_id=2,
                           coin_id=coin_id, current_price=close,
                           target_price=target_price, risk=result[1], position=position,
                           timeframe_id=timeframe_id)
    elif float(last_macd[1, 1]) < np.array(macd_df.tail(delay)["histogram"])[0] and \
            old_price < close and old_position == "buy":
        result = False, "medium"
        target_price = close * gain + close if result[0] else -close * gain + close
        position = 'buy' if result[0] else 'sell'
        functions.set_recommendation(db_connection=connection, analysis_id=2,
                                     coin_id=coin_id, timeframe_id=timeframe_id, position=position,
                                     target_price=target_price, current_price=close,
                                     cost_price=cost, risk=result[1])
        broadcast_messages(connection=connection, analysis_id=2,
                           coin_id=coin_id, current_price=close,
                           target_price=target_price, risk=result[1], position=position,
                           timeframe_id=timeframe_id)

