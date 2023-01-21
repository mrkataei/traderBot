"""
Mr.Kataei 8/15/2021
updated at 9/16/2021
this StreamIStrategies class is inheritance  from stream and implement those functions and some
 additional function work with StrategiesThreads that run on thread for each coin that every coin have many thread size
 of timeframe already supported
for broadcast signals we need API telebot that on bot for our signals
/*for test code change the API First*/
database configure :
        coin_id -> 1=BTCUSDT , 2=ETHUSDT , 3=
        timeframe_id -> 1=30min , 2=1hour ,3=4hour ,4=1day, 1=1min
        analysis_id -> 1=emerald , 2=ruby , 3= diamond
"""
import threading
from time import sleep, time
from datetime import datetime
from time import process_time
import telebot
# from Analysis.emerald import Emerald
from Analysis.palladium import Palladium
from Analysis.diamond import Diamond
from Analysis.ruby import Ruby
from Interfaces.stream import Stream
from Libraries.data_collector import get_candle_binance as candles
from Libraries.check_validation_users import check_validate_stream

# master bot already run on vps dont use this @aitrdbot -> address
API_KEY = '2123917023:AAFPy9xoaJLt0BxqQJgC3J3F9km8F7ozdn8'
# @testkourosh2bot -> address // use this bot for test your code
# API_KEY = '1978536410:AAE_RMk3-4r_cLnt_nRcEnZHaSp-vIk9oVo'

_bot_ins = telebot.TeleBot(API_KEY)


class StreamIStrategies(Stream):
    def __init__(self, symbol: str):
        Stream.__init__(self, symbol=symbol)

    def stream_1min_candle(self):
        while True:
            # delay = 59
            # if 1 <= round(time()) % 60 <= 3:
            #     print('1min', datetime.fromtimestamp(time()))
            #     data = candles(symbol=self.symbol, number=1, unit='m', limit=10)
            #     if data[0]:
            #         emerald = Emerald(data=data[1], coin_id=self.coin_id, timeframe_id=5, bot_ins=_bot_ins)
            #         emerald.signal()
            #     delay = process_time()
            # sleep(abs(60 - delay))
            sleep(60)

    def stream_15min_candle(self):
        while True:
            delay = 899
            if 1 <= round(time()) % 900 <= 3:
                print('15min', datetime.fromtimestamp(time()))
                data = candles(symbol=self.symbol, number=15, unit='m', limit=400)
                if data[0]:
                    ruby = Ruby(data=data[1], coin_id=self.coin_id, timeframe_id=6, bot_ins=_bot_ins)
                    ruby.signal()
                delay = process_time()
            sleep(abs(900 - delay))

    def stream_30min_candle(self):
        while True:
            # 30 min strategies implement here
            sleep(1800)

    def stream_1hour_candle(self):
        while True:
            # 60 min strategies implement here
            delay = 3599
            if 1 <= round(time()) % 3600 <= 3:
                print('1hour', datetime.fromtimestamp(time()))
                data = candles(symbol=self.symbol, number=1, unit='h', limit=1000)
                if data[0]:
                    setting_palladium = self.get_setting_analysis(analysis_id=4, timeframe_id=2)
                    if setting_palladium:
                        palladium = Palladium(data=data[1], coin_id=self.coin_id, timeframe_id=2,
                                              setting=setting_palladium, bot_ins=_bot_ins)
                        palladium.signal()
                delay = process_time()
            sleep(abs(3600 - delay))

    def stream_4hour_candle(self):
        while True:
            delay = 14399
            if 1 <= round(time()) % 14400 <= 3:
                print('4hour', datetime.fromtimestamp(time()))
                data = candles(symbol=self.symbol, number=4, unit='h', limit=1000)
                if data[0]:
                    setting_diamond = self.get_setting_analysis(analysis_id=3, timeframe_id=3)
                    if setting_diamond:
                        diamond = Diamond(data=data[1], coin_id=self.coin_id, timeframe_id=3,
                                          setting=setting_diamond, bot_ins=_bot_ins)
                        diamond.signal()
                delay = process_time()
            sleep(abs(14400 - delay))

    def stream_1day_candle(self):
        while True:
            # 1 Day strategies implement here
            sleep(86400)


class StrategiesThreads:
    def __init__(self, *symbols: str):
        self.symbols = symbols
        self.threads = []
        for symbol in symbols:
            self.threads.append(threading.Thread(target=StreamIStrategies(symbol=symbol).run))

    def start_threads(self):
        threading.Thread(target=check_validate_stream).start()
        for thread in self.threads:
            thread.daemon = True
            thread.start()

    def join_threads(self):
        for thread in self.threads:
            thread.join()
