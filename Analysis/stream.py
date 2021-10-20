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
import threading
from time import sleep
import telebot
from Analysis.emerald import signal as emerald
from Analysis.diamond import signal as diamond
from Analysis.ruby import signal as ruby
from Interfaces.stream import Stream
from Libraries.data_collector import get_candle_api as candles

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

    def stream_30min_candle(self):
        while True:
            data = candles(symbol=self.symbol, timeframe='30m', limit=100)
            setting_emerald = self.get_setting_analysis(analysis_id=1, timeframe_id=1)
            emerald(data=data, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                    timeframe_id=1, setting=setting_emerald, bot_ins=_bot_ins, symbol=self.symbol, timeframe='30m')
            setting_diamond = self.get_setting_analysis(analysis_id=3, timeframe_id=1)
            diamond(data=data, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                    timeframe_id=1, setting=setting_diamond, bot_ins=_bot_ins, symbol=self.symbol, timeframe='30m')
            sleep(20)

    def stream_1hour_candle(self):
        data = candles(symbol=self.symbol, timeframe='1h', limit=100)
        setting_emerald = self.get_setting_analysis(analysis_id=1, timeframe_id=2)
        emerald(data=data, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                timeframe_id=2, setting=setting_emerald, bot_ins=_bot_ins, symbol=self.symbol, timeframe='1hour')
        sleep(41)

    def stream_4hour_candle(self):
        data = candles(symbol=self.symbol, timeframe='4h', limit=100)
        setting_emerald = self.get_setting_analysis(analysis_id=1, timeframe_id=3)
        emerald(data=data, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                timeframe_id=3, setting=setting_emerald, bot_ins=_bot_ins, symbol=self.symbol, timeframe='4hour')
        setting_ruby = self.get_setting_analysis(analysis_id=2, timeframe_id=3)
        ruby(data=data, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
             timeframe_id=3, settings=setting_ruby, bot_ins=_bot_ins, symbol=self.symbol, timeframe='4hour')
        setting_diamond = self.get_setting_analysis(analysis_id=3, timeframe_id=3)
        diamond(data=data, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                timeframe_id=3, setting=setting_diamond, bot_ins=_bot_ins, symbol=self.symbol, timeframe='4hour')
        sleep(163)

    def stream_1day_candle(self):
        data = candles(symbol=self.symbol, timeframe='1D', limit=100)
        setting_emerald = self.get_setting_analysis(analysis_id=1, timeframe_id=4)
        emerald(data=data, gain=self.gain, cost=self.cost, coin_id=self.coin_id,
                timeframe_id=4, setting=setting_emerald, bot_ins=_bot_ins, symbol=self.symbol, timeframe='1Day')
        sleep(211)

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
