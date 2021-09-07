import asyncio
from binance import AsyncClient, BinanceSocketManager
from Inc import db, functions


class Stream:
    def __init__(self, symbol: str):
        self.symbol = symbol
        __connection = db.con_db()
        self.coin_id = functions.get_coin_id(__connection, symbol)
        self.client = None
        self.socket = None

    # there is 4 functions for 4 timeframes after all used in main async
    async def stream_30min_candle(self):
        raise Exception("NotImplementedException")

    async def stream_1hour_candle(self):
        raise Exception("NotImplementedException")

    async def stream_4hour_candle(self):
        raise Exception("NotImplementedException")

    async def stream_1day_candle(self):
        raise Exception("NotImplementedException")

    def set_cost(self, cost: float):
        raise Exception("NotImplementedException")

    def set_gain(self, gain: float):
        raise Exception("NotImplementedException")

    async def stream(self):
        # init statics for clean date
        # this method work with n parameters and return stored CSVs in Static with 4 timeframes
        self.client = await AsyncClient.create()
        self.socket = BinanceSocketManager(self.client)
        await asyncio.gather(self.stream_30min_candle(),
                             self.stream_1hour_candle(),
                             self.stream_4hour_candle(),
                             self.stream_1day_candle())

    def run(self):
        asyncio.run(self.stream())
