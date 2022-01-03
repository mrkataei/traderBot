import pandas_ta as ta
from Interfaces.strategy import Strategy


class Ruby(Strategy):
    def __init__(self, data, coin_id: int, timeframe_id: int, bot_ins, analysis_id: int = 2):
        Strategy.__init__(self, data=data, coin_id=coin_id, analysis_id=analysis_id,
                          timeframe_id=timeframe_id, bot_ins=bot_ins)
        self.preprocess()

    def preprocess(self):
        self.data['ema_9'] = ta.ema(self.data['close'], length=9)
        self.data['ema_38'] = ta.ema(self.data['close'], length=38)
        self.data['crossover'] = ta.cross(self.data['ema_38'], self.data['ema_9'], above=True)
        self.data['crossunder'] = ta.cross(self.data['ema_38'], self.data['ema_9'], above=False)
        self.data.dropna()
        self.data.reset_index(drop=True)

    def logic(self, row):
        if row['crossover']:
            self._set_recommendation(position='buy', risk='low', index=row.name)
        elif row['crossunder']:
            self._set_recommendation(position='sell', risk='low', index=row.name)
