'''
Arman hajimirza
this function created for back testing the signals ...
'''
import datetime
from datetime import datetime
import pandas as pd
import pandas_ta as ta
import numpy as np
from Libraries.tools import get_source
from Libraries import macd
import sys
from dateutil import parser
import pytz

'''
checked and its work!
this function return dataframe of indicators and every details 
that  diamond signal needs to generate signal
parameters: dataframe , signal settings
output: dataframe 
'''


def diamond_preprocess(data, setting: dict):
    global stoch_k_oversell
    global stoch_k_overbuy
    global stoch_rsi_k_overbuy
    global stoch_rsi_k_oversell
    global rsi_oversell
    global rsi_overbuy
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

    macd_df = macd.macd(close=macd_source, slow=slow, fast=fast, matype="sma", signal=sign)
    rsi_sr = ta.rsi(close=rsi_source, length=rsi_length)
    stoch_df = data.ta.stoch(k=stoch_k, d=stoch_d, smooth_k=stoch_smooth)
    stoch_rsi_df = ta.stochrsi(close=stoch_rsi_source, length=stoch_rsi_length, rsi_length=stoch_rsi_rsi_length,
                               k=stoch_rsi_k, d=stoch_rsi_d)
    new_df = pd.concat([macd_df, rsi_sr, stoch_df, stoch_rsi_df], axis=1)
    new_df.columns = ["macd", "histogeram", "signal", "rsi", "stoch_k", "stoch_d", "stochrsi_k", "stochrsi_d"]
    new_df = pd.concat([df["date"], df["close"], new_df], axis=1)
    new_df["macd1"] = new_df['macd'].shift(periods=1)
    new_df = new_df.dropna()
    new_df = new_df.reset_index(drop=True)
    new_df["crossover"] = ta.cross(series_a=new_df["stochrsi_k"], series_b=new_df["stochrsi_d"])
    new_df["crossunder"] = ta.cross(series_a=new_df["stochrsi_k"], series_b=new_df["stochrsi_d"], above=False)
    return new_df


"""
checked
set globals and intial value for backtesting
"""


def reset(intialvalue):
    global old_price
    global old_position
    global intial_value
    global low_price
    old_price = 0
    old_position = "sell"
    low_price = sys.float_info.min
    intial_value = intialvalue


"""
checked
get time and timezone and changed the to standard format
can be used for reformat the date of any dataframes
"""


def change_date_type(date: str, time_zone=None):
    datetime_object = parser.parse(date)
    if time_zone:
        timezone = pytz.timezone(time_zone)
        datetime_object = timezone.localize(datetime_object)
    return datetime_object


"""

 create the window of data frame checked and its works correctly
 
"""


def window(dataframe, starttime: str, endtime=None, timezone=None):
    starttime_object = change_date_type(starttime, timezone)
    index = dataframe.index
    # starttime_object = datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S%z')
    condition = dataframe["date"] >= starttime_object
    try:
        indices = index[condition]
        indices = indices[0]
    except Exception as E:
        indices = 0
    if endtime is None:
        return dataframe[indices::].reset_index(drop=True)
    else:
        # endtime_object = datetime.strptime( endtime, '%Y-%m-%d %H:%M:%S%z')
        endtime_object = change_date_type(endtime, timezone)
        end_condition = dataframe["date"] >= endtime_object
        try:
            end_indices = index[end_condition]
            end_indices = end_indices[0]
            print(end_indices)

            return dataframe[indices:end_indices].reset_index(drop=True)
        except Exception as E:
            print(E)
            return dataframe[indices::].reset_index(drop=True)


"""
checked and works correctly
this function is a diomond signal
that check conditions of each candle  

"""


def diamond(row):
    global old_price
    global old_position
    global intial_value
    global low_price

    date = row['date']
    close = row["close"]
    macd = row['macd']
    rsi = row['rsi']
    stoch_k = row["stoch_k"]
    stochrsi_k = row["stochrsi_k"]
    macd1 = row["macd1"]
    crossover = row['crossover']
    crossunder = row['crossunder']
    buy_counter = 0
    sell_counter = 0

    if close <= low_price:
        low_price = close
    if old_position == "sell":
        # check stoch_k < stoch_k_oversell and stoch_rsi_k < stoch_rsi_k_oversell
        if stoch_k < stoch_k_oversell and stochrsi_k < stoch_rsi_k_oversell:
            buy_counter += 2
        # check rsi < rsi_oversell
        if rsi < rsi_oversell:
            buy_counter += 1
        # check crossOver
        if crossover == 1:
            buy_counter += 1
        # check macd < 0 and macd > macd[1]
        if macd1 < macd < 0:
            buy_counter += 1
        # buy signal operation
        if buy_counter > 3:
            # calculate risk
            old_position = "buy"
            old_price = close
            low_price = close
            if buy_counter == 4:
                buy_counter = 0
                return date, "buy", close, "medium", intial_value / close, intial_value, "----", "----", "----"
            else:
                buy_counter = 0
                return date, "buy", close, "high", intial_value / close, intial_value, "----", "----", "----"
        # add signal to database
    elif old_position == "buy" and old_price < close:
        # check stoch_k > stoch_k_oversell and stoch_rsi_k > stoch_rsi_k_oversell
        if stoch_k > stoch_k_overbuy and stochrsi_k > stoch_rsi_k_overbuy:
            sell_counter += 2
        # check rsi < rsi_overbuy
        if rsi < rsi_overbuy:
            sell_counter += 1
        # check crossunder
        if crossunder == 1:
            sell_counter += 1
        # macd > 0 and macd < macd[1]
        if 0 < macd < macd1:
            sell_counter += 1
        if sell_counter > 3:
            old_position = "sell"
            intial_value = intial_value * (close / old_price)
            low = low_price
            low_price = sys.float_info.min
            if sell_counter == 4:
                sell_counter = 0
                return date, "sell", close, "medium", intial_value / close, intial_value, close - old_price, round(
                    (close / old_price) * 100 - 100, 4), ((low - old_price) / old_price) * 100
            else:
                sell_counter = 0
                return date, "sell", close, "high", intial_value / close, intial_value, close - old_price, round(
                    (close / old_price) * 100 - 100, 4), ((low - old_price) / old_price) * 100


"""
checked and work correctly
this function iterate on dataframe and process 
signal of each row to generate dataframe of signals
function parameter is a signal function such as diamond and pattern or ruby

"""


def strategy(dataframe, function, instialvalue):
    reset(instialvalue)
    output_df = dataframe.apply(lambda row: function(row), axis=1)
    output_df = output_df.dropna()
    return pd.DataFrame(output_df.to_list(),
                        columns=['date', 'position', 'close-$', "risk", "amount-%", "value-$", "profit-$", "profit-%",
                                 "low price-%"])


'''
checked and its work!
this function return dataframe of indicators and every details 
that  patterns signal needs to generate signal
parameters: dataframe 
output: dataframe 
'''


def patterns_preprocess(dataframe):
    dataframe = dataframe.replace(1, True)
    # buy
    dataframe["buy"] = dataframe[
        ['ladder_bottom', 'doji_star_bullish', 'matching_low', 'in_neck_line_bullish', 'harami_cross_bullish', 'hammer',
         'belt_hold_bullish', 'on_neck_line_bullish', 'homing_pigeon', 'tri_star_bullish', 'engulfing_bullish',
         'harami_bullish',
         'three_outside_up', 'morning_doji_star', 'three_inside_up', 'piercing_line', 'upside_gap_three_methods',
         'abandoned_baby_bullish',
         'inverted_hammer', 'upside_tasuki_gap', 'stick_sandwich', 'meeting_line_bullish', 'downside_gap_three_methods',
         'three_white_soldiers', 'morning_star', 'breakaway_bullish']].any(axis='columns')
    # sell
    dataframe["sell"] = dataframe[
        ['falling_three_methods', 'matching_high', 'hanging_man', "belt_hold_bearish", 'harami_cross_bearish',
         'doji_star_bearish', 'in_neck_line_bearish', 'on_neck_line_bearish', 'shooting_star',
         'engulfing_bearish', 'tri_star_bearish', 'loentical_three_cross', 'evening_doji_star',
         'abandoned_baby_bearish',
         'three_outside_down', 'harami_bearish', 'three_inside_down', 'deliberation', 'dark_cloud_cover',
         'advance_block',
         'meeting_line_bearish', 'evening_star', 'downside_tasuki_gap', 'three_black_crows']].any(axis='columns')

    return dataframe[["date", 'close', 'open', 'low', 'high', 'volume', 'buy', 'sell']]


'''
checked and works correctly
this function is a patterns signal
that check conditions of each candle 
 
'''


def patterns(row):
    date = row["date"]
    close = row["close"]
    buy = row["buy"]
    sell = row["sell"]
    global old_price
    global old_position
    global intial_value
    global low_price
    if close <= low_price:
        low_price = close
    if old_position == "sell" and buy:

        old_position = "buy"
        old_price = close
        low_price = close
        return date, "buy", close, "medium", intial_value / close, intial_value, "----", "----", "----"
    elif old_position == "buy" and sell:

        old_position = "sell"
        intial_value = intial_value * (close / old_price)
        low = low_price
        low_price = sys.float_info.min
        return date, "sell", close, "medium", intial_value / close, intial_value, close - old_price, round(
            (close / old_price) * 100 - 100, 4), ((low - old_price) / old_price) * 100


"""
checked and work correctly
show performance of signal on dataframe
"""


def results(dataframe, intial_value: int):
    dataframe = dataframe.drop(dataframe[dataframe["position"] == "buy"].index)
    net_profit = np.array(dataframe["value-$"].tail(1))[0] / intial_value
    positive_trades = dataframe[dataframe["profit-%"] >= 0].count()
    total_trades = int(len(dataframe))
    acurracy = positive_trades.date / total_trades
    average_trade_profit = net_profit / total_trades
    result = round(positive_trades.date), round(total_trades), round(acurracy * 100, 2), round(net_profit * 100,
                                                                                               4), round(
        average_trade_profit * 100, 4)
    return pd.DataFrame(np.asarray(result).reshape(1, 5),
                        columns=["positive_trades", "total_trades", "acurracy-%", "net_profit-%",
                                 "average_trade_profit-%"])

# df = pd.read_csv(r"D:\PycharmProjects\Static\Binance_ETHUSDT_minute.csv")
#
# df = df.iloc[::-1]
# df= df.reset_index(drop=True) df.columns = ['unix','date' ,'symbol', 'open' , 'high' , 'low' ,
# 'close' , 'volume','Adj close' , 'count']
# print(df)

# settings = {'analysis_setting': {'stoch_k_oversell': 29,
# 'stoch_k_overbuy': 86, 'stoch_rsi_k_oversell': 16, 'stoch_rsi_k_overbuy': 86, 'rsi_oversell': 39, 'rsi_overbuy':
# 64}, 'indicators_setting': {'RSI': {'length': 4, 'source': 'close'}, 'stoch': {'k': 22, 'd': 3, 'smooth': 3},
# 'stochrsi': {'k': 3, 'd': 3, 'rsi_length': 22, 'length': 11, 'source': 'ohlc4'}, 'MACD': {'slow': 26, 'signal': 20,
# 'fast': 10, 'source': 'low', 'matype': 'ema'}}}

# new_df = diamond_preprocess(df , setting = settings )
# print(new_df)
# fuck = strategy(new_df , diamond , 100)
# print(fuck)
