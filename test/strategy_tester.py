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
    except Exception:
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


def trades_table(dataframe):
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


class StrategyTaster:
    def __init__(self, name: str, symbol: str, timeframe: str, dataframe, initial_value: int):
        self.symbol = symbol
        self.name = name
        self.timeframe = timeframe
        self.dataframe = dataframe
        self.starttime = self.dataframe["date"][0]
        self.endtime = self.dataframe["date"].tail(1).item()

        self.initial_value = initial_value
        self.current_value = initial_value
        self.old_price = 0
        self.old_position = "sell"
        self.low_price = sys.float_info.min
        # self.dataframe = self.window()
        self.trades_list = self.taster(dataframe=self.dataframe, function=self.strategy)
        self.result = self.results()

    def reset(self):
        self.current_value = self.initial_value
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

    def strategy(self, row):

        date = row["date"]
        close = row["close"]
        recommendation = row["recommendation"]

        if close <= self.low_price:
            self.low_price = close
        if self.old_position == "sell" and recommendation == "buy":

            self.old_position = "buy"
            self.old_price = close
            self.low_price = close
            return date, "buy", close, "medium", self.current_value / close, self.current_value, "----", "----", "----"
        elif self.old_position == "buy" and recommendation == "sell":
            self.old_position = "sell"
            self.current_value = self.current_value * (close / self.old_price)
            low = self.low_price
            self.low_price = sys.float_info.min
            return date, "sell", close, "medium",\
                   self.current_value / close, self.current_value, close - self.old_price, \
                   round((close / self.old_price) * 100 - 100, 4), ((low - self.old_price) / self.old_price) * 100

    def results(self, result_df=None):
        try:
            starter_amount = self.trades_list["amount-%"][0]
            dataframe = self.trades_list.drop(self.trades_list[self.trades_list["position"] == "buy"].index)
            net_profit = (np.array(dataframe["value-$"].tail(1))[0] - self.initial_value) / self.initial_value
            positive_trades = dataframe[dataframe["profit-%"] >= 0].count()
            total_trades = int(len(dataframe))
            accuracy = positive_trades.date / total_trades
            average_trade_profit = net_profit / total_trades
            profitpercoin = (dataframe["amount-%"].tail(1).item() - starter_amount) / starter_amount
            result = self.name, self.symbol, self.timeframe, self.starttime, self.endtime, round(
                positive_trades.date), round(total_trades), round(accuracy * 100, 2), round(net_profit * 100, 4), round(
                average_trade_profit * 100, 4), round(profitpercoin * 100, 4),\
                     round(dataframe["value-$"].tail(1).item(), 4)
        except Exception:
            result = self.name, self.symbol, self.timeframe, self.starttime, self.endtime, 0, 0, 0, 0, 0, 0, 0

        try:
            return result_df.append(pd.DataFrame(np.asarray(result).reshape(1, 12),
                                                 columns=['strategy', 'symbol', 'timeframe', 'starttime', 'endtime',
                                                          "positive_trades", "total_trades", "accuracy-%",
                                                          "net_profit-%", "average_trade_profit-%",
                                                          'profit_per_coin-%', "final_amount"]))
        except Exception:
            return pd.DataFrame(np.asarray(result).reshape(1, 12),
                                columns=['strategy', 'symbol', 'timeframe', 'starttime', 'endtime',
                                         "positive_trades", "total_trades", "accuracy-%", "net_profit-%",
                                         "average_trade_profit-%", 'profit_per_coin-%', "final_amount"])

    # def change_date_type(self, date: str, time_zone=None):
    #     datetime_object = parser.parse(date)
    #     if time_zone:
    #         timezone = pytz.timezone(time_zone)
    #         datetime_object = timezone.localize(datetime_object)
    #     return datetime_object
    #
    # def window(self, dataframe=None, timezone=None):
    #     if dataframe is None: dataframe = self.dataframe
    #     starttime_object = self.change_date_type(self.starttime, timezone)
    #     index = dataframe.index
    #     condition = dataframe["date"] >= starttime_object
    #     try:
    #         indices = index[condition]
    #         indices = indices[0]
    #     except Exception as E:
    #         indices = 0
    #     if self.endtime is None:
    #         return dataframe[indices::].reset_index(drop=True)
    #     else:
    #         endtime_object = self.change_date_type(self.endtime, timezone)
    #         end_condition = dataframe["date"] >= endtime_object
    #         try:
    #             end_indices = index[end_condition]
    #             end_indices = end_indices[0]
    #             return dataframe[indices:end_indices].reset_index(drop=True)
    #         except Exception as E:
    #             return dataframe[indices::].reset_index(drop=True)

    def show(self):
        # trades = self.taster(self.dataframe , self.strategy)
        trades_table(self.trades_list)
        self.candlestick_plot()
        fig = px.line(self.trades_list[self.trades_list["position"] == "sell"], x="date", y="value-$",
                      title='current value')
        fig.show()
        fig = px.line(self.trades_list[self.trades_list["position"] == "sell"], x="date", y="profit-%",
                      title='profit-%')
        fig.show()
        return self.result
