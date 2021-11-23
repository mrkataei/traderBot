"""
    Mr.Kataei 11/12/2021
"""
import threading
from Inc.functions import get_coin_id
from Conf.analysis_settings import get_analysis_setting


class Stream:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.coin_id = get_coin_id(symbol)

    # there is 4 functions for 4 timeframes after all used in main async
    def stream_1min_candle(self):
        raise Exception("NotImplementedException")

    def stream_30min_candle(self):
        raise Exception("NotImplementedException")

    def stream_1hour_candle(self):
        raise Exception("NotImplementedException")

    def stream_4hour_candle(self):
        raise Exception("NotImplementedException")

    def stream_1day_candle(self):
        raise Exception("NotImplementedException")

    def stream(self):
        stream_1m_candle = threading.Thread(target=self.stream_1min_candle)
        stream_30min_candle = threading.Thread(target=self.stream_30min_candle)
        stream_1hour_candle = threading.Thread(target=self.stream_1hour_candle)
        stream_4hour_candle = threading.Thread(target=self.stream_4hour_candle)
        stream_1day_candle = threading.Thread(target=self.stream_1day_candle)
        stream_1m_candle.start()
        stream_30min_candle.start()
        stream_1hour_candle.start()
        stream_4hour_candle.start()
        stream_1day_candle.start()

    def get_setting_analysis(self, analysis_id: int, timeframe_id: int):
        settings = get_analysis_setting(coin_id=self.coin_id, timeframe_id=timeframe_id,
                                        analysis_id=analysis_id)
        return settings

    def run(self):
        self.stream()
