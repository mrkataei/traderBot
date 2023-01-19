"""
Mr.Kataei
"""
import pandas_ta as ta
from Libraries.macd import macd_indicator
from Interfaces.strategy import Strategy


class Diamond(Strategy):
    def __init__(self, data, coin_id: int, timeframe_id: int, bot_ins, setting: dict, is_back_test: bool = False,
                 analysis_id: int = 3):
        Strategy.__init__(self, data=data, coin_id=coin_id, analysis_id=analysis_id,
                          timeframe_id=timeframe_id, bot_ins=bot_ins)
        self.macd_setting = setting['indicators_setting']['MACD']
        self.rsi_setting = setting['indicators_setting']['RSI']
        self.stoch_setting = setting['indicators_setting']['stoch']
        self.stochrsi_setting = setting['indicators_setting']['stochrsi']

        statics_setting = setting['analysis_setting']
        self.stoch_k_oversell = statics_setting['stoch_k_oversell']
        self.stoch_k_overbuy = statics_setting['stoch_k_overbuy']
        self.stoch_rsi_k_overbuy = statics_setting['stoch_rsi_k_overbuy']
        self.stoch_rsi_k_oversell = statics_setting['stoch_rsi_k_oversell']
        self.rsi_oversell = statics_setting['rsi_oversell']
        self.rsi_overbuy = statics_setting['rsi_overbuy']
        self.open_trades = False if self.last_position == 'sell' or is_back_test else True
        self.position_avg_price = 0
        self.preprocess()

    def preprocess(self):
        # macd
        macd_source = self.get_source(source=self.macd_setting['source'])
        self.data[['macd', 'histogram', 'signal']] = macd_indicator(close=macd_source, slow=self.macd_setting['slow'],
                                                                    fast=self.macd_setting['fast'],
                                                                    matype="sma", signal=self.macd_setting['signal'])

        # rsi
        rsi_source = self.get_source(source=self.rsi_setting['source'])
        self.data['rsi'] = ta.rsi(close=rsi_source, length=self.rsi_setting['length'])

        # stoch
        self.data[['stoch_k', 'stoch_d']] = self.data.ta.stoch(k=self.stoch_setting['k'], d=self.stoch_setting['d'],
                                                               smooth_k=self.stoch_setting['smooth'])

        # stoch_rsi
        stoch_rsi_source = self.get_source(source=self.stochrsi_setting['source'])
        self.data[['stochrsi_k', 'stochrsi_d']] = ta.stochrsi(close=stoch_rsi_source,
                                                              length=self.stochrsi_setting['length'],
                                                              rsi_length=self.stochrsi_setting['rsi_length'],
                                                              k=self.stochrsi_setting['k'],
                                                              d=self.stochrsi_setting['d'])
        # shifted macd
        self.data["macd_1"] = self.data['macd'].shift(periods=1)
        # shifted stochrsi_k , stochrsi_d
        self.data["stochrsi_k_1"] = self.data["stochrsi_k"].shift(periods=1)
        self.data["stochrsi_d_1"] = self.data["stochrsi_d"].shift(periods=1)

        self.data = self.data.round(2)
        self.data = self.data.iloc[373:]  # stoch rsi delay
        self.data = self.data.reset_index()

    def logic(self, row):
        crossover = False
        crossunder = False
        buy_counter = 0
        sell_counter = 0
        if row["stochrsi_k_1"] > row["stochrsi_d_1"] and row["stochrsi_k"] <= row["stochrsi_d"]:
            crossunder = True
        if row["stochrsi_k_1"] < row["stochrsi_d_1"] and row["stochrsi_k"] >= row["stochrsi_d"]:
            crossover = True
        # check stoch_k < stoch_k_oversell and stoch_rsi_k < stoch_rsi_k_oversell
        if row["stoch_k"] < self.stoch_k_oversell and row["stochrsi_k"] < self.stoch_rsi_k_oversell:
            buy_counter += 2
        # check rsi < rsi_oversell
        if row["rsi"] < self.rsi_oversell:
            buy_counter += 1
        # check crossOver
        if crossover:
            buy_counter += 1
        # check macd < 0 and macd > macd[1]
        if row["macd_1"] < row["macd"] < 0:
            buy_counter += 1
        # buy signal operation
        if buy_counter > 3 and not self.open_trades:
            self.open_trades = True
            self._set_recommendation(position="buy", risk="high", index=row.name)
            self.position_avg_price = row['open']

        # check stoch_k > stoch_k_oversell and stoch_rsi_k > stoch_rsi_k_oversell
        if row["stoch_k"] > self.stoch_k_overbuy and row["stochrsi_k"] > self.stoch_rsi_k_overbuy:
            sell_counter += 2
        # check rsi < rsi_overbuy
        if row["rsi"] > self.rsi_overbuy:
            sell_counter += 1
        # check crossunder
        if crossunder:
            sell_counter += 1
        # macd > 0 and macd < macd[1]
        if 0 < row["macd"] < row["macd_1"]:
            sell_counter += 1
        if sell_counter > 3 and self.open_trades and self.position_avg_price < row['open']:
            # self.position_avg_price = 0
            self._set_recommendation(position="sell", risk='high', index=row.name)
            self.open_trades = False

    def signal(self):
        """
        check last row of processed dataframe to generate signal
        """
        last_row_diamond_detector = self.get_recommendations().tail(1)
        position = last_row_diamond_detector['recommendation'].values[0]
        if self.last_position != position and position is not None:
            close = float(last_row_diamond_detector['close'].values[0])
            self.broadcast(position=position, current_price=close, risk=last_row_diamond_detector['risk'].values[0])
            self.insert_database(position=position, current_price=close,
                                 risk=last_row_diamond_detector['risk'].values[0])
            if position == 'buy':
                self.order(position=position)
            elif position == 'sell' and self.last_price < close:
                self.order(position=position)
