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
import telebot
from Analysis.emerald import signal as emerald
from Analysis.diamond import signal as diamond
from Analysis.ruby import signal as ruby
from Interfaces.stream import Stream, append

# master bot already run on vps dont use this @algowatchbot -> address
API_KEY = '1987308624:AAEow3hvRGt4w6ZFmz3bYaQz1J8p-OzRer0'
# @testkourosh2bot -> address // use this bot for test your code
# API_KEY = '1978536410:AAE_RMk3-4r_cLnt_nRcEnZHaSp-vIk9oVo'
_bot_ins = telebot.TeleBot(API_KEY)


class StreamIStrategies(Stream):
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
                    setting_emerald = self.get_setting_analysis(analysis_id=1, timeframe_id=1)
                    self.data_30min = append(data=self.data_30min.tail(100), symbol=self.symbol,
                                             timeframe="30min", candle=c_30m_data)
                    emerald(data=self.data_30min, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                            timeframe_id=1, setting=setting_emerald, bot_ins=_bot_ins)
                    setting_diamond = self.get_setting_analysis(analysis_id=3, timeframe_id=1)
                    diamond(data=self.data_30min, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                            timeframe_id=1, setting=setting_diamond, bot_ins=_bot_ins)
                    await asyncio.sleep(1790)

    async def stream_1hour_candle(self):
        candle_1hour = self.socket.kline_socket(symbol=self.symbol, interval='1h')
        async with candle_1hour:
            while True:
                c_1h_data = await candle_1hour.recv()
                if c_1h_data['k']['x']:
                    setting_emerald = self.get_setting_analysis(analysis_id=1, timeframe_id=2)
                    self.data_1hour = append(data=self.data_1hour.tail(100), symbol=self.symbol,
                                             timeframe="1hour", candle=c_1h_data)
                    emerald(data=self.data_1hour, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                            timeframe_id=2, setting=setting_emerald, bot_ins=_bot_ins)
                    await asyncio.sleep(3590)

    async def stream_4hour_candle(self):
        candle_4hour = self.socket.kline_socket(symbol=self.symbol, interval='4h')
        async with candle_4hour:
            while True:
                c_4h_data = await candle_4hour.recv()
                if c_4h_data['k']['x']:
                    setting_emerald = self.get_setting_analysis(analysis_id=1, timeframe_id=3)
                    self.data_4hour = append(data=self.data_4hour.tail(100), symbol=self.symbol,
                                             timeframe="4hour", candle=c_4h_data)
                    emerald(data=self.data_4hour, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                            timeframe_id=3, setting=setting_emerald, bot_ins=_bot_ins)
                    setting_ruby = self.get_setting_analysis(analysis_id=2, timeframe_id=3)
                    ruby(data=self.data_30min, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                         timeframe_id=3, settings=setting_ruby, bot_ins=_bot_ins)
                    setting_diamond = self.get_setting_analysis(analysis_id=3, timeframe_id=3)
                    diamond(data=self.data_30min, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                            timeframe_id=3, setting=setting_diamond, bot_ins=_bot_ins)
                    await asyncio.sleep(14390)

    async def stream_1day_candle(self):
        candle_1day = self.socket.kline_socket(symbol=self.symbol, interval='1d')
        async with candle_1day:
            while True:
                c_1d_data = await candle_1day.recv()
                if c_1d_data['k']['x']:
                    setting_emerald = self.get_setting_analysis(analysis_id=1, timeframe_id=4)
                    self.data_1day = append(data=self.data_1day.tail(100), symbol=self.symbol,
                                            timeframe="1day", candle=c_1d_data)
                    emerald(data=self.data_1day, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                            timeframe_id=4, setting=setting_emerald, bot_ins=_bot_ins)
                    await asyncio.sleep(86390)

    def set_cost(self, cost: float):
        self.cost = cost

    def set_gain(self, gain: float):
        self.gain = gain


class StrategiesThreads:
    def __init__(self, *symbols: str):
        self.symbols = symbols
        self.threads = []
        for symbol in symbols:
            self.threads.append(threading.Thread(target=StreamIStrategies(symbol=symbol).run))

    def start_threads(self):
        for thread in self.threads:
            thread.daemon = True
            thread.start()

    def join_threads(self):
        for thread in self.threads:
            thread.join()
