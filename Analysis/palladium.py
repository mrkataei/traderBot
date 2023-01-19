"""
    Mr.Amin 1/31/2022
    This is strategy occ
    -------------------------------
    debug -> first check : Mr.kataei 31/1/2022  .
            edit attr and functions and parameters
            sec check : Mr.kataei 1/2/2022
            occ function parameters dont need use attr of class
    ---------------------------
    debug -> remove 1hour candles : Mr.Amin 5/2/2022
"""
import pandas_ta as ta
from Interfaces.strategy import Strategy
import pandas as pd
from Libraries.data_collector import get_candle_binance as candle


class Palladium(Strategy):
    def __init__(self, data, coin_id: int, timeframe_id: int, bot_ins, setting: dict, analysis_id: int = 4):
        Strategy.__init__(self, data=data, coin_id=coin_id, analysis_id=analysis_id,
                          timeframe_id=timeframe_id, bot_ins=bot_ins)
        self.setting = setting
        self.analysis_setting = self.setting['analysis_setting']
        self.length = self.analysis_setting['len']
        self.offSig = self.analysis_setting['offSig']
        self.offsetALMA = self.analysis_setting['offsetALMA']
        self.useRes = self.analysis_setting['useRes']
        self.basisType = self.analysis_setting['basisType']
        self.strares = self.analysis_setting['strares']
        # dont use self.numberTimeFrame, self.unitTimeFrame
        self.numberTimeFrame = self.analysis_setting['numberTimeFrame']
        self.unitTimeFrame = self.analysis_setting['unitTimeFrame']
        self.preprocess()

    def preprocess(self):

        def occ(source: pd.Series, volume: pd.Series = None):
            """
            :param volume: for additional condition we need volume too
            :param source: series of close or open , ...
            :return
            """
            result = None

            if self.basisType == "SMA":
                # v1 - Simple Moving Average
                result = ta.sma(source, self.length)
            elif self.basisType == "EMA":
                # v2 - Exponential Moving Average
                result = ta.ema(source, self.length)

            elif self.basisType == "DEMA":
                # v3 - Double Exponential
                result = ta.dema(source, self.length)

            elif self.basisType == "TEMA":
                # v4 - Triple Exponential
                result = ta.ema(source, self.length)
                result = 3 * (result - ta.ema(result, self.length)) + \
                         ta.ema(ta.ema(result, self.length), self.length)

            elif self.basisType == "WMA":
                # v5 - Weighted
                result = ta.wma(source, self.length)

            elif self.basisType == "VWMA":
                # v6 - Volume Weighted
                # volume must be second variable
                result = ta.vwma(source, volume, self.length)

            elif self.basisType == "HullMA":
                # v8 - Hull
                result = ta.hma(source, self.length)

            elif self.basisType == "ALMA":
                # v10 - Arnaud Legoux
                result = ta.alma(source, self.length, self.offsetALMA, self.offSig)

            elif self.basisType == "TMA":
                # v11 - Triangular (extreme smooth)
                result = ta.sma(source, self.length)
                result = ta.sma(result, self.length)

            return result

        if self.useRes:
            # dont use self var out of init ,
            temp = candle(symbol='ETHUSDT', number=self.numberTimeFrame * self.strares, unit=self.unitTimeFrame,
                          limit=1000)[1]  # need to handle timeframe id - coin id
            indexLastUpperTimeframe = self.data.index[self.data['date'] == temp.date.iloc[-1]].tolist()[-1]
            self.data.drop(list(range(indexLastUpperTimeframe + 1, len(self.data))), axis=0, inplace=True)
            temp['closeSeriesAlt'] = occ(source=temp['close'], volume=temp['volume'])
            temp['openSeriesAlt'] = occ(source=temp['open'], volume=temp['volume'])

            self.data = pd.merge(self.data, temp.loc[:, ["date", "closeSeriesAlt", "openSeriesAlt"]], how="left",
                                 on="date")
            self.data.ffill(inplace=True)
            self.data.bfill(inplace=True)
        else:
            self.data['closeSeriesAlt'] = occ(source=self.data['close'], volume=self.data['volume'])
            self.data['openSeriesAlt'] = occ(source=self.data['open'], volume=self.data['volume'])

        self.data['crossover'] = ta.cross(self.data['closeSeriesAlt'], self.data['openSeriesAlt'], above=True)
        self.data['crossunder'] = ta.cross(self.data['closeSeriesAlt'], self.data['openSeriesAlt'], above=False)

    def logic(self, row):
        # implement your strategy here , you need all rows you need appended to one row in preprocess
        if row['crossover']:
            self._set_recommendation(position='buy', risk='low', index=row.name)
        elif row['crossunder']:
            self._set_recommendation(position='sell', risk='low', index=row.name)