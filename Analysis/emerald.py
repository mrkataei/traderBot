"""
Arman hajimirza & Mr.Kataei

database configure :
        coin_id -> 1=BTCUSDT , 2=ETHUSDT
        timeframe_id -> 1=30min , 2=1hour ,3=4hour ,4=1day
        analysis_id -> 1=ichimoku
use this query for get user who have this signal with this coin and time:
        users = functions.get_user_recommendation(connection, coin_id=1,analysis_id=1, timeframe_id=1)
and get chat_id for notify them with this query :
        chat_id = functions.get_user_chat_id(connection , user[0])
all of this in Telegram/message just use broadcast method
for insert new signal :
        functions.set_recommendation(connection, 1, 1, 1, "sell", 2500, 2300, 2, "high")
        broadcast_message(*args)
"""
import pandas as pd
import pandas_ta as ta
import numpy as np
from Inc.functions import get_recommendations, set_recommendation
from Telegram.Client.message import broadcast_messages
import datetime


def _get_ichimoku(data: pd.DataFrame, tenkan, kijun, senkou):
    ichimoku = pd.DataFrame(data.ta.ichimoku(tenkan=tenkan, kijun=kijun, senkou=senkou)[0])
    ichimoku.columns = ['spanA', 'spanB', 'tenkensen', 'kijunsen', 'chiku']

    # continuous rows from clouds
    def get_future_spans():
        ichimoku_future = pd.DataFrame(data.ta.ichimoku(tenkan=tenkan, kijun=kijun, senkou=senkou)[1])
        ichimoku_future.columns = ['spanA', 'spanB']
        return ichimoku_future

    return ichimoku, get_future_spans()


def signal(data: pd.DataFrame, gain: float, cost: float, coin_id: int, timeframe_id: int, setting: dict, bot_ins,
           symbol: str, timeframe: str):
    tenkan = setting['indicators_setting']['ichimoku']['tenkan']
    kijun = setting['indicators_setting']['ichimoku']['kijun']
    senkou = setting['indicators_setting']['ichimoku']['senkou']
    ichimoku_all = _get_ichimoku(data=data, tenkan=tenkan, kijun=kijun, senkou=senkou)
    ichimoku = ichimoku_all[0]
    future = ichimoku_all[1]
    ichimoku['close'] = data.close
    # future cloud and market trend
    future['signal'] = np.where(future['spanA'] > future['spanB'], 'buy', 'sell')
    # one last row in ichimoku
    last_ichimoku = np.array(ichimoku.tail(1))[0].astype(float)
    close = float(last_ichimoku[5])
    print(str(datetime.datetime.now()), "emerald checking ..." + symbol, timeframe)
    try:
        query = get_recommendations(analysis_id=1, timeframe_id=timeframe_id, coin_id=coin_id)
        old_position = query[0][2]
        old_risk = query[0][7]
        # when no rows in database
    except Exception as e:
        old_position = 'buy'
        old_risk = 'low'
        # print(e)

    def check():
        # return Tuple ( buy->True , sell->False ) and risk (0(low)-10(high))
        if future.iloc[-1, 2] == 'buy':  # 3 col signal last row
            if last_ichimoku[0] > last_ichimoku[1]:
                if close > last_ichimoku[2]:
                    if close > last_ichimoku[3]:
                        if close > last_ichimoku[0]:
                            return True, 'low'
                        else:
                            return True, 'medium'
                    else:
                        return True, 'medium'
                else:
                    return True, 'high'
            else:
                return True, 'very high'
        else:
            if close > last_ichimoku[0]:
                if close > last_ichimoku[3]:
                    if close > last_ichimoku[2]:
                        if last_ichimoku[0] < last_ichimoku[1]:
                            return False, 'low'
                        else:
                            return False, 'medium'
                    else:
                        return False, 'medium'
                else:
                    return False, 'high'
            else:
                return False, 'very high'

    result = check()
    target_price = close * gain + close if result[0] else -close * gain + close
    position = 'buy' if result[0] else 'sell'
    if old_position != position or old_risk != result[1]:
        set_recommendation(analysis_id=1, coin_id=coin_id, timeframe_id=timeframe_id, position=position,
                           target_price=target_price, current_price=close, cost_price=cost, risk=result[1])
        broadcast_messages(coin_id=coin_id, analysis_id=1, timeframe_id=timeframe_id, position=position,
                           target_price=target_price, current_price=close, risk=result[1], bot_ins=bot_ins)
# for transaction in future
# users = functions.get_user_recommendation(connection, coin_id=coin_id, analysis_id=1, timeframe_id=timeframe_id)
# for user in users:
#     functions.pay_transaction(db_connection=connection ,cost_price=cost ,username=user ,detail="")
