import pandas as pd


class Strategy:
    def __init__(self, data: pd.DataFrame):
        self.dataframe = data

    def signal(self):
        raise Exception("NotImplementedException")

    def preprocess(self):
        raise Exception("NotImplementedException")

    def trade(self):
        raise Exception("NotImplementedException")

    def broadcast(self):
        raise Exception("NotImplementedException")

    def get_source(self, source: str = 'close'):
        return {
            'hl2': self.dataframe.ta.hl2(),
            'hlc3': self.dataframe.ta.hlc3(),
            'ohlc4': self.dataframe.ta.ohlc4(),
            'close': self.dataframe['close'],
            'high': self.dataframe['high'],
            'low': self.dataframe['low'],
            'open': self.dataframe['open']
        }.get(source, self.dataframe['close'])
