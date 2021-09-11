"""
Mr.Kataei 8/15/2021
async functions for get data stream from binance socket for 30m , 1h , 4h , 1day timeframes and multiple symbols
.first you must init statics you have because when new data append date work truth , after that check your analysis
with CSVs stored
database configure :
        coin_id -> 1=BTCUSDT , 2=ETHUSDT
        timeframe_id -> 1=30min , 2=1hour ,3=4hour ,4=1day
        analysis_id -> 1=ichimoku
use this query for get user who have this signal with this coin and time:
        users = functions.get_user_recommendation(connection, coin_id=1,analysis_id=1, timeframe_id=1)
and get chat_id for notify them with this query :
        chat_id = functions.get_user_chat_id(connection , user[0])
all of this in Telegram/message just use broadcast method
for insert new signal :
        functions.set_recommendation(connection, 1, 1, 1, "sell", 2500, 2300, 2, "high")
        broadcast_message(*args)
"""
import asyncio
import threading
from Analysis import ichimoku
from Interfaces.stream import Stream, append


class StreamIchimoku(Stream):
    def __init__(self, symbol: str, cost: float = 1, gain: float = 0.003):
        Stream.__init__(self, symbol=symbol)
        self.cost = cost
        self.gain = gain

    async def stream_30min_candle(self):
        candle_30min = self.socket.kline_socket(symbol=self.symbol, interval='30m')
        async with candle_30min:
            while True:
                c_30m_data = await candle_30min.recv()
                if c_30m_data['k']['x']:
                    self.data_30min = append(data=self.data_30min.tail(100), symbol=self.symbol,
                                             timeframe="30min", candle=c_30m_data)
                    ichimoku.signal(data=self.data_30min, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                                    timeframe_id=1)
                    await asyncio.sleep(1790)

    async def stream_1hour_candle(self):
        candle_1hour = self.socket.kline_socket(symbol=self.symbol, interval='1h')
        async with candle_1hour:
            while True:
                c_1h_data = await candle_1hour.recv()
                if c_1h_data['k']['x']:
                    self.data_1hour = append(data=self.data_1hour.tail(100), symbol=self.symbol,
                                             timeframe="1hour", candle=c_1h_data)
                    ichimoku.signal(data=self.data_1hour, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                                    timeframe_id=2)
                    await asyncio.sleep(3590)

    async def stream_4hour_candle(self):
        candle_4hour = self.socket.kline_socket(symbol=self.symbol, interval='4h')
        async with candle_4hour:
            while True:
                c_4h_data = await candle_4hour.recv()
                if c_4h_data['k']['x']:
                    self.data_4hour = append(data=self.data_4hour.tail(100), symbol=self.symbol,
                                             timeframe="4hour", candle=c_4h_data)
                    ichimoku.signal(data=self.data_4hour, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                                    timeframe_id=3)
                    await asyncio.sleep(14390)

    async def stream_1day_candle(self):
        candle_1day = self.socket.kline_socket(symbol=self.symbol, interval='1d')
        async with candle_1day:
            while True:
                c_1d_data = await candle_1day.recv()
                if c_1d_data['k']['x']:
                    self.data_1day = append(data=self.data_1day.tail(100), symbol=self.symbol,
                                            timeframe="1day", candle=c_1d_data)
                    ichimoku.signal(data=self.data_1day, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                                    timeframe_id=4)
                    await asyncio.sleep(86390)

    def set_cost(self, cost: float):
        self.cost = cost

    def set_gain(self, gain: float):
        self.gain = gain


def run_ichimoku_threads(*symbols: str):
    for symbol in symbols:
        ichimoku_symbol = StreamIchimoku(symbol=symbol)
        btcusdt_thread = threading.Thread(target=ichimoku_symbol.run)
        btcusdt_thread.daemon = True
        btcusdt_thread.start()
