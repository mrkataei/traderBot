import pandas as pd
import pandas_ta as ta

from Inc.functions import set_recommendation, get_last_recommendations, record_dictionary
from Libraries.tools import get_source
from Libraries.macd import macd_indicator

from Telegram.Client.message import broadcast_messages


class Ruby:
    """
    A class that generate and broadcast ruby signal
    ...
    Attributes
    ----------
    data: dataframe
        A dataframe made of candles with  specific coin and timeframe
        at least must have 100 rows
        dataframe columns: date , close , open , high , volume

    coin_id : int
        the id of coin that dataframe made of
    timeframe_id :
        the id of coin that dataframe made of
    bot:

    setting: dict
        A setting include signal(analysis) settings and indicators settings
        that Ruby needs to generate signal
        setting format:
        {'analysis_setting': {'delay': int, 'safe_line': int, 'hist_line': int},
        'indicators_setting': {'MACD': {'slow': int, 'signal': int, 'fast': int, 'source': str , 'matype': 'str'}}}
    Methods
    -------
    preprocess();
        generate the dataframe that Ruby needs to process signal
    get_old_position()
        this method gets last position (buy or sell) from database
    get_old_price():
        this method gets last price (close) from database
    broadcast(position: str, current_price: float, target_price: float, risk: str):
        broadcast the signal to users
    insert_database(position: str, current_price: float, target_price: float, risk: str):
        insert singal to database
    _set_recommendation(self, position: str, index):
        set position and condition in specific index of dataframe
    ruby(row):
        check conditions of signal for one row
    signal_detector():
        apply ruby function  to dataframe
    get_recommendations():
        process signal on dataframe
    signal():
        check last row recommendations to generate new signal
    """

    def __init__(self, data: pd.DataFrame, coin_id: int, timeframe_id: int, bot_ins, setting: dict):
        """
        parameters
        ----------
        data: dataframe
            A dataframe made of candles with  specific coin and timeframe
            at least must have 100 rows
            dataframe columns: date , close , open , high , volume

        coin_id : int
            the id of coin that dataframe made of
        timeframe_id :
            the id of coin that dataframe made of
        bot_ins:

        setting: dict
            A setting include signal(analysis) settings and indicators settings
            that Ruby needs to generate signal
            setting format:
            {'analysis_setting': {'delay': int, 'safe_line': int, 'hist_line': int},
            'indicators_setting': {'MACD': {'slow': int, 'signal': int, 'fast': int, 'source': str , 'matype': 'str'}}}


        """
        self.data = data
        self.coin_id = coin_id
        self.timeframe_id = timeframe_id
        self.bot = bot_ins
        self.setting = setting
        self.macd_setting = setting['indicators_setting']['MACD']
        statics_setting = setting['analysis_setting']
        self.delay = statics_setting['delay']
        self.safe_line = statics_setting['safe_line']
        self.hist_line = statics_setting['hist_line']
        self.preprocess()

    def preprocess(self):
        """
        generate the dataframe that Ruby needs to process signal
        get macd settings and generate macd dataframe

        check and add crossover column to dataframe
        concat these to main dataframe
        """
        # macd settings
        slow = self.macd_setting['slow']
        sign = self.macd_setting['signal']
        fast = self.macd_setting['fast']
        matype = self.macd_setting['matype']
        macd_source = self.macd_setting['source']
        macd_source = get_source(data=self.data, source=macd_source)
        # generate macd dataframe
        macd_df = macd_indicator(close=macd_source, slow=slow, fast=fast, signal=sign, matype=matype)
        macd_df.columns = ["macd", "histogram", "signal"]
        # concat candles dateframe with macd dataframe
        temp = pd.concat([self.data, macd_df], axis=1)
        # add macd[delay] to dataframe
        temp[f'macd{self.delay}'] = temp['macd'].shift(periods=self.delay)
        temp = temp.dropna()
        # add crossover of histogram and hist_line  column to datafram
        temp["crossover"] = ta.cross(series_a=temp["histogram"], series_b=pd.Series(self.hist_line, index=temp.index))
        self.data = temp

    def get_old_position(self):
        """
        get last position(buy or sell) of analysis id 2
        old position by default is 'sell'
        :return: old_position
        """
        query = get_last_recommendations(analysis_id=2, timeframe_id=self.timeframe_id, coin_id=self.coin_id)
        if query:
            old_position = record_dictionary(query[0], "recommendations")["position"]
        else:
            old_position = 'sell'
        return old_position

    def get_old_price(self):
        """
        get last price(close) of analysis id 2
        old position by default is 'sell'
        :return: last_price
        """
        query = get_last_recommendations(analysis_id=2, timeframe_id=self.timeframe_id, coin_id=self.coin_id)
        if query:
            old_price = record_dictionary(query[0], "recommendations")["price"]
        else:
            old_price = 0
        return old_price

    def broadcast(self, position: str, current_price: float, risk: str):
        """
        broadcast signal to users
        :param position: recommendation of signal
        :param current_price: close of selected candle
        :param risk: risk of signal

        """
        broadcast_messages(coin_id=self.coin_id, analysis_id=2, timeframe_id=self.timeframe_id, position=position,
                           current_price=current_price, risk=risk, bot_ins=self.bot)

    def insert_database(self, position: str, current_price: float, risk: str):
        """
        insert signal to database
        :param position: recommendation of signal
        :param current_price: close of selected candle
        :param risk: risk of signal
        """
        set_recommendation(analysis_id=2, coin_id=self.coin_id, timeframe_id=self.timeframe_id, position=position,
                           price=current_price, risk=risk)

    def _set_recommendation(self, position: str, index):
        # set recommendation and risk in dataframe
        self.data.loc[index, 'recommendation'] = position
        self.data.loc[index, 'risk'] = "medium"

    def get_recommendations(self):
        """
        apply signal to dataframe
        and add risk and recommendation column to dataframe
        :return: dataframe
        """
        self.signal_detector()
        return self.data[['date', 'open', 'high', 'close', 'low', 'risk', 'recommendation']].copy()

    def ruby(self, row):
        """
        check a row of dataframe to check ruby conditions and insert position to recommendation column and risk to
        risk column
        :param row: a row of dataframe
        """
        crossover = row['crossover']
        histogram = row['histogram']
        macd = row["macd"]
        delay_hist = row[f'macd{self.delay}']

        if crossover == 1 and macd < - self.safe_line:
            self._set_recommendation(position='buy', index=row.name)
        elif histogram < delay_hist:
            self._set_recommendation(position='sell', index=row.name)

    def signal_detector(self):
        self.data.apply(lambda row: self.ruby(row), axis=1)

    def signal(self):
        """
        check last row of processed dataframe to generate signal
        """
        last_row_ruby_detector = self.get_recommendations().tail(1)
        position = last_row_ruby_detector['recommendation'].values[0]
        old_position = self.get_old_position()
        old_price = self.get_old_price()
        if old_position != position:
            close = float(last_row_ruby_detector['close'].values[0])
            if position == 'buy':
                self.broadcast(position=position, current_price=close, risk=last_row_ruby_detector['risk'].values[0])
                self.insert_database(position=position, current_price=close,
                                     risk=last_row_ruby_detector['risk'].values[0])

            elif position == 'sell' and old_price < close:
                self.broadcast(position=position, current_price=close, risk=last_row_ruby_detector['risk'].values[0])
                self.insert_database(position=position, current_price=close,
                                     risk=last_row_ruby_detector['risk'].values[0])

# test case:
# df = pd.read_csv(r"C:\Users\Asus\Downloads\bitcoin-pattern-reco-1min.csv")
# df = df[['date', 'open', 'high', 'close', 'low', "volume"]]
# df = df.tail(10000)
# print(df)
# settings = {'analysis_setting': {'delay': 13, 'safe_line': -8603, 'hist_line': 0},
# 'indicators_setting': {'MACD': {'slow': 17, 'signal': 9, 'fast': 4, 'source': 'close', 'matype': 'sma'}}}
# # df = df.iloc[::-1]
# # # df = df.drop(columns=["tradecount"])
# # df = df.reset_index(drop=True)
# # print(df)
# pd.set_option('display.max_columns', None)
# a = Ruby(data=df, coin_id=5, timeframe_id=4, gain=1, bot_ins=1, setting=settings, cost=1)
# print(a.get_old_position())
# print(a.get_old_price())
