"""
Arman hajimirza
this function created for back testing the signals ...
"""

import sys

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pytz
from dateutil import parser
from plotly.subplots import make_subplots

'''
checked and its work!
this function return dataframe of indicators and every details 
that  diamond signal needs to generate signal
parameters: dataframe , signal settings
output: dataframe 
'''

# def create_df(data, setting: dict):
#     global stoch_k_oversell
#     global stoch_k_overbuy
#     global stoch_rsi_k_overbuy
#     global stoch_rsi_k_oversell
#     global rsi_oversell
#     global rsi_overbuy
#     slow = setting['indicators_setting']['MACD']['slow']
#     sign = setting['indicators_setting']['MACD']['signal']
#     fast = setting['indicators_setting']['MACD']['fast']
#     macd_source = setting['indicators_setting']['MACD']['source']
#     macd_source = get_source(data=data, source=macd_source)
#
#     # rsi
#     rsi_source = setting['indicators_setting']['RSI']['source']
#     rsi_length = setting['indicators_setting']['RSI']['length']
#     rsi_source = get_source(data=data, source=rsi_source)
#
#     # stoch
#     stoch_k = setting['indicators_setting']['stoch']['k']
#     stoch_d = setting['indicators_setting']['stoch']['d']
#     stoch_smooth = setting['indicators_setting']['stoch']['smooth']
#
#     # stoch_rsi
#     stoch_rsi_rsi_length = setting['indicators_setting']['stochrsi']['rsi_length']
#     stoch_rsi_length = setting['indicators_setting']['stochrsi']['length']
#     stoch_rsi_k = setting['indicators_setting']['stochrsi']['k']
#     stoch_rsi_d = setting['indicators_setting']['stochrsi']['d']
#     stoch_rsi_source = setting['indicators_setting']['stochrsi']['source']
#     stoch_rsi_source = get_source(data=data, source=stoch_rsi_source)
#
#     # signal parameters
#     stoch_k_oversell = setting['analysis_setting']['stoch_k_oversell']
#     stoch_k_overbuy = setting['analysis_setting']['stoch_k_overbuy']
#     stoch_rsi_k_overbuy = setting['analysis_setting']['stoch_rsi_k_overbuy']
#     stoch_rsi_k_oversell = setting['analysis_setting']['stoch_rsi_k_oversell']
#     rsi_oversell = setting['analysis_setting']['rsi_oversell']
#     rsi_overbuy = setting['analysis_setting']['rsi_overbuy']
#
#     macd_df = macd.macd_indicator(close=macd_source, slow=slow, fast=fast, matype="sma", signal=sign)
#     rsi_sr = ta.rsi(close=rsi_source, length=rsi_length)
#     stoch_df = data.ta.stoch(k=stoch_k, d=stoch_d, smooth_k=stoch_smooth)
#     stoch_rsi_df = ta.stochrsi(close=stoch_rsi_source, length=stoch_rsi_length, rsi_length=stoch_rsi_rsi_length,
#                                k=stoch_rsi_k, d=stoch_rsi_d)
#     new_df = pd.concat([macd_df, rsi_sr, stoch_df, stoch_rsi_df], axis=1)
#     new_df.columns = ["macd", "histogeram", "signal", "rsi", "stoch_k", "stoch_d", "stochrsi_k", "stochrsi_d"]
#     new_df = pd.concat([data["date"], data["close"], new_df], axis=1)
#     new_df["macd1"] = new_df['macd'].shift(periods=1)
#     new_df = new_df.dropna()
#     new_df = new_df.reset_index(drop=True)
#     new_df["crossover"] = ta.cross(series_a=new_df["stochrsi_k"], series_b=new_df["stochrsi_d"])
#     new_df["crossunder"] = ta.cross(series_a=new_df["stochrsi_k"], series_b=new_df["stochrsi_d"], above=False)
#     return new_df
#
#
# """
# checked
# set globals and intial value for backtesting
# """
#
#
# def restart(intialvalue):
#     global old_price
#     global old_position
#     global intial_value
#     global low_price
#     old_price = 0
#     old_position = "sell"
#     low_price = sys.float_info.min
#     intial_value = intialvalue
#
#
# """
# checked
# get time and timezone and changed the to standard format
# can be used for reformat the date of any dataframes
# """
#
#
# def change_date_type(date: str, time_zone=None):
#     datetime_object = parser.parse(date)
#     if time_zone:
#         timezone = pytz.timezone(time_zone)
#         datetime_object = timezone.localize(datetime_object)
#     return datetime_object
#
#
# """
#
#  create the window of data frame checked and its works correctly
#
# """
#
#
# def window(dataframe, starttime: str, endtime=None, timezone=None):
#     starttime_object = change_date_type(starttime, timezone)
#     index = dataframe.index
#     # starttime_object = datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S%z')
#     condition = dataframe["date"] >= starttime_object
#     try:
#         indices = index[condition]
#         indices = indices[0]
#     except Exception as E:
#         indices = 0
#     if endtime is None:
#         return dataframe[indices::].reset_index(drop=True)
#     else:
#         # endtime_object = datetime.strptime( endtime, '%Y-%m-%d %H:%M:%S%z')
#         endtime_object = change_date_type(endtime, timezone)
#         end_condition = dataframe["date"] >= endtime_object
#         try:
#             end_indices = index[end_condition]
#             end_indices = end_indices[0]
#             print(end_indices)
#
#             return dataframe[indices:end_indices].reset_index(drop=True)
#         except Exception as E:
#             print(E)
#             return dataframe[indices::].reset_index(drop=True)
#

"""
checked and works correctly
this function is a diomond signal
that check conditions of each candle  

"""


# def diamond(date, close, macd, rsi, stoch_k, stoch_d, stochrsi_k, stochrsi_d, macd1, crossover, crossunder):
#     global old_price
#     global old_position
#     global intial_value
#     global low_price
#     buy_counter = 0
#     sell_counter = 0
#
#     if close <= low_price:
#         low_price = close
#     if old_position == "sell":
#         # check stoch_k < stoch_k_oversell and stoch_rsi_k < stoch_rsi_k_oversell
#         if stoch_k < stoch_k_oversell and stochrsi_k < stoch_rsi_k_oversell:
#             buy_counter += 2
#         # check rsi < rsi_oversell
#         if rsi < rsi_oversell:
#             buy_counter += 1
#         # check crossOver
#         if crossover == 1:
#             buy_counter += 1
#         # check macd < 0 and macd > macd[1]
#         if macd1 < macd < 0:
#             buy_counter += 1
#         # buy signal operation
#         if buy_counter > 3:
#             # calculate risk
#             old_position = "buy"
#             old_price = close
#             low_price = close
#             if buy_counter == 4:
#                 buy_counter = 0
#                 return date, "buy", close, "medium", intial_value / close, intial_value, "----", "----", "----"
#             else:
#                 buy_counter = 0
#                 return date, "buy", close, "high", intial_value / close, intial_value, "----", "----", "----"
#         # add signal to database
#     elif old_position == "buy" and old_price < close:
#         # check stoch_k > stoch_k_oversell and stoch_rsi_k > stoch_rsi_k_oversell
#         if stoch_k > stoch_k_overbuy and stochrsi_k > stoch_rsi_k_overbuy:
#             sell_counter += 2
#         # check rsi < rsi_overbuy
#         if rsi < rsi_overbuy:
#             sell_counter += 1
#         # check crossunder
#         if crossunder == 1:
#             sell_counter += 1
#         # macd > 0 and macd < macd[1]
#         if 0 < macd < macd1:
#             sell_counter += 1
#         if sell_counter > 3:
#             old_position = "sell"
#             intial_value = intial_value * (close / old_price)
#             low = low_price
#             low_price = sys.float_info.min
#             if sell_counter == 4:
#                 sell_counter = 0
#                 return date, "sell", close, "medium", intial_value / close, intial_value, close - old_price, round(
#                     (close / old_price) * 100 - 100, 4), ((low - old_price) / old_price) * 100
#             else:
#                 sell_counter = 0
#                 return date, "sell", close, "high", intial_value / close, intial_value, close - old_price, round(
#                     (close / old_price) * 100 - 100, 4), ((low - old_price) / old_price) * 100
#
#
# """
# checked and work correctly
# this function iterate on dataframe and process
# signal of each row to generate dataframe of signals
#
# """
#
#
# def strategy(dataframe, intialvalue):
#     restart(intialvalue)
#     output_df = dataframe.apply(
#         lambda row: diamond(date=row["date"], close=row["close"], macd=row["macd"], rsi=row["rsi"],
#                             stoch_k=row["stoch_k"],
#                             stoch_d=row["stoch_d"], stochrsi_k=row["stochrsi_k"],
#                             stochrsi_d=row["stochrsi_d"],
#                             macd1=row["macd1"], crossover=row["crossover"],
#                             crossunder=row["crossunder"]), axis=1)
#     output_df = output_df.dropna()
#     return pd.DataFrame(output_df.to_list(),
#                         columns=['date', 'position', 'close-$', "risk", "amount-%", "value-$", "profit-$", "profit-%",
#                                  "low price-%"])
#
#
# """
# checked and work correctly
# show performance of signal on dataframe
# """
#
#
# def results(dataframe, intial_value: int):
#     dataframe = dataframe.drop(dataframe[dataframe["position"] == "buy"].index)
#     net_profit = np.array(dataframe["value-$"].tail(1))[0] / intial_value
#     positive_trades = dataframe[dataframe["profit-%"] >= 0].count()
#     total_trades = int(len(dataframe))
#     acurracy = positive_trades.date / total_trades
#     average_trade_profit = net_profit / total_trades
#     result = round(positive_trades.date), round(total_trades), round(acurracy * 100, 2), round(net_profit * 100,
#                                                                                                4), round(
#         average_trade_profit * 100, 4)
#     return pd.DataFrame(np.asarray(result).reshape(1, 5),
#                         columns=["positive_trades", "total_trades", "acurracy-%", "net_profit-%",
#                                  "average_trade_profit-%"])
#

class StrategyTaster:
    def __init__(self, name: str, symbol: str, timeframe: str, dataframe, endtime: str,
                 intial_value: int, starttime: str = '2000 1 1'):
        self.symbol = symbol
        self.name = name
        self.timeframe = timeframe
        self.dataframe = dataframe
        self.starttime = starttime
        self.endtime = endtime

        self.intial_value = intial_value
        self.current_value = intial_value
        self.old_price = 0
        self.old_position = "sell"
        self.low_price = sys.float_info.min
        self.dataframe = self.window()
        self.trades_list = self.taster(dataframe=self.dataframe, function=self.strategy)
        self.result = self.results()

    def reset(self):
        self.current_value = self.intial_value
        self.old_price = 0
        self.old_position = "sell"
        self.low_price = sys.float_info.min

    def taster(self, dataframe, function):
        self.reset()
        output_df = dataframe.apply(lambda row: function(row), axis=1)
        output_df = output_df.dropna()
        return pd.DataFrame(output_df.to_list(),
                            columns=['date', 'position', 'close-$', "risk", "amount-%", "value-$", "profit-$",
                                     "profit-%", "low price-%"])

    def preprocess(self):
        raise Exception("not ready yet")

    def candlestick_plot(self):

        candlestick = go.Candlestick(x=self.dataframe['date'],
                                     open=self.dataframe['open'],
                                     high=self.dataframe['high'],
                                     low=self.dataframe['low'],
                                     close=self.dataframe['close'])

        rec_df = self.trades_list

        recommendations = go.Scatter(
            x=rec_df['date'],
            y=rec_df['close-$'] + 50,
            mode="markers",
            text=rec_df["position"] + "<br>" + rec_df["risk"] + "<br>" + rec_df['close-$'].astype(str),

            # marker=dict(symbol="6")
            marker=dict(symbol='triangle-down', size=12, color=(
                (rec_df["position"] == "buy")
            ).astype('int'),
                        colorscale=[[0, 'red'], [1, 'blue']])
        )

        fig = make_subplots(specs=[[{"secondary_y": False}]])
        fig.add_trace(candlestick)
        fig.add_trace(recommendations, secondary_y=False)
        fig.update_layout(plot_bgcolor='rgb(44,52,60)')
        fig.update_yaxes(tickprefix="$")
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
        fig.show()

    def trades_table(self, dataframe):
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(dataframe.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[dataframe["date"], dataframe["position"], dataframe["close-$"], dataframe["risk"],
                               dataframe["amount-%"], dataframe["value-$"], dataframe["profit-$"],
                               dataframe["profit-%"], dataframe['low price-%']],

                       fill=dict(color=['rgb(245, 245, 245)',  # unique color for the first column
                                        ['rgba(0,250, 0, 0.8)' if type(
                                            profit) is float and profit >= 0 else 'red' if type(
                                            profit) is float and profit < 0 else "Lavender" for profit in
                                         dataframe["profit-%"]]]),
                       align='left'))
        ])

        fig.show()

    def strategy(self, row):

        date = row["date"]
        close = row["close"]
        recomendation = row["recommendation"]

        if close <= self.low_price:
            self.low_price = close
        if self.old_position == "sell" and recomendation == "buy":

            self.old_position = "buy"
            self.old_price = close
            self.low_price = close
            return date, "buy", close, "medium", self.current_value / close, self.current_value, "----", "----", "----"
        elif self.old_position == "buy" and recomendation == "sell":
            self.old_position = "sell"
            self.current_value = self.current_value * (close / self.old_price)
            low = self.low_price
            self.low_price = sys.float_info.min
            return date, "sell", close, "medium", self.current_value / close, self.current_value, close - self.old_price, \
                   round((close / self.old_price) * 100 - 100, 4), ((low - self.old_price) / self.old_price) * 100

    def results(self, result_df=None):

        starter_amount = self.trades_list["amount-%"][0]
        dataframe = self.trades_list.drop(self.trades_list[self.trades_list["position"] == "buy"].index)
        net_profit = np.array(dataframe["value-$"].tail(1))[0] / self.intial_value
        positive_trades = dataframe[dataframe["profit-%"] >= 0].count()
        total_trades = int(len(dataframe))
        acurracy = positive_trades.date / total_trades
        average_trade_profit = net_profit / total_trades
        profitpercoin = (dataframe["amount-%"].tail(1).item() - starter_amount) / starter_amount
        result = self.name, self.symbol, self.timeframe, self.starttime, self.endtime, round(
            positive_trades.date), round(total_trades), round(acurracy * 100, 2), round(net_profit * 100, 4), round(
            average_trade_profit * 100, 4), round(profitpercoin * 100, 4)

        try:
            return result_df.append(pd.DataFrame(np.asarray(result).reshape(1, 11),
                                                 columns=['strategy', 'symbol', 'timefarme', 'starttime', 'endtime',
                                                          "positive_trades", "total_trades", "acurracy-%",
                                                          "net_profit-%", "average_trade_profit-%",
                                                          'profit_per_coin-%']))
        except:
            return pd.DataFrame(np.asarray(result).reshape(1, 11),
                                columns=['strategy', 'symbol', 'timefarme', 'starttime', 'endtime',
                                         "positive_trades", "total_trades", "acurracy-%", "net_profit-%",
                                         "average_trade_profit-%", 'profit_per_coin-%'])

    def change_date_type(self, date: str, time_zone=None):
        datetime_object = parser.parse(date)
        if time_zone:
            timezone = pytz.timezone(time_zone)
            datetime_object = timezone.localize(datetime_object)
        return datetime_object

    def window(self, dataframe=None, timezone=None):
        if dataframe is None: dataframe = self.dataframe
        starttime_object = self.change_date_type(self.starttime, timezone)
        index = dataframe.index
        condition = dataframe["date"] >= starttime_object
        try:
            indices = index[condition]
            indices = indices[0]
        except Exception as E:
            indices = 0
        if self.endtime is None:
            return dataframe[indices::].reset_index(drop=True)
        else:
            endtime_object = self.change_date_type(self.endtime, timezone)
            end_condition = dataframe["date"] >= endtime_object
            try:
                end_indices = index[end_condition]
                end_indices = end_indices[0]
                return dataframe[indices:end_indices].reset_index(drop=True)
            except Exception as E:
                return dataframe[indices::].reset_index(drop=True)

    def show(self):
        # trades = self.taster(self.dataframe , self.strategy)
        self.trades_table(self.trades_list)
        self.candlestick_plot()
        fig = px.line(self.trades_list[self.trades_list["position"] == "sell"], x="date", y="value-$",
                      title='current value')
        fig.show()
        fig = px.line(self.trades_list[self.trades_list["position"] == "sell"], x="date", y="profit-%",
                      title='profit-%')
        fig.show()
        return self.result
