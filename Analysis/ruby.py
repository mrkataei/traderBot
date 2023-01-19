"""
    Mr.kataei 1/3/2022
"""
import pandas_ta as ta
from Interfaces.strategy import Strategy


class Ruby(Strategy):
    def __init__(self, data, coin_id: int, timeframe_id: int, bot_ins, analysis_id: int = 2):
        Strategy.__init__(self, data=data, coin_id=coin_id, analysis_id=analysis_id,
                          timeframe_id=timeframe_id, bot_ins=bot_ins)
        self.preprocess()

    def preprocess(self):
        self.data['wma_10'] = ta.wma(self.data['close'], length=10)
        self.data['wma_20'] = ta.wma(self.data['close'], length=20)
        self.data['wma_82'] = ta.wma(self.get_source(source='hlc3'), length=82)
        self.data[['stoch_rsi_k', 'stoch_rsi_d']] = ta.stochrsi(close=self.data['close'],
                                                                k=1, d=2, rsi_length=6, length=6)
        self.data = self.data.round(2)
        self.data['crossover'] = ta.cross(self.data['wma_20'], self.data['wma_10'], above=True)
        self.data['crossunder'] = ta.cross(self.data['wma_20'], self.data['wma_10'], above=False)
        self.data.dropna()
        self.data.reset_index(drop=True)

    def logic(self, row):
        if row['crossover'] and row['stoch_rsi_d'] > row['stoch_rsi_k'] and row['close'] <= row['wma_82']:
            self._set_recommendation(position='buy', risk='low', index=row.name)
        elif row['crossunder'] and row['stoch_rsi_d'] <= row['stoch_rsi_k'] and row['close'] > row['wma_82']:
            self._set_recommendation(position='sell', risk='low', index=row.name)
