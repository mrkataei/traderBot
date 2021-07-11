from binance.client import Client
import pyttsx3
from tradingview import *
import pandas as pd
import numpy as np



class Agent:
    engine = None
    def __init__(self , rate:int=125 , volume:float=0.1 , sex:str='male'):
        #setting up volume level  between 0 and 1
        #changing index, changes voices sex :  male or female
        #setting up new voice rate
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id) if sex=='male' else self.engine.setProperty('voice', voices[1].id)
        self.engine.say("Hello , I'm Aran ,your trade assistance")
        self.engine.runAndWait()
        self.engine.stop()
    def say_string(self , sentence):
        self.engine.say(sentence)
        self.engine.runAndWait()
        self.engine.stop()
class ClientBinance(Client):
    __client = None
    __agentCon = None
    __data = None
    def __init__(self ,api_key:str , api_secret:str , agent:bool=True , rate:int=180 , volume:float=1 ,sex:str='male'):
        self.__agentCon = Agent(rate=rate, volume=volume, sex=sex) if agent else None
        super(ClientBinance, self).__init__(api_key=api_key , api_secret=api_secret)
        if self.__agentCon :
            self.__agentCon.say_string("client has been connected")
        print("client has been connected")

    # input timeframes {day  , 1hour , 1month  , 1week  , 1min  , 4hour ,  5min  ,  15min}
    def get_data(self, symbol:str , timeframe:str):
        candles = self.get_klines(symbol=symbol , interval=get_time_interval(timeframe))
        self.__data = pd.DataFrame(candles,
                            columns=['date', 'open', 'high', 'low', 'close', 'volume', 'time2', 'QAV', 'trades',
                                     'TBAV', 'TQAV', 'Ignore'])

        #optional
        del self.__data['time2']
        self.__data['date'] = pd.DatetimeIndex(pd.to_datetime(self.__data['date'],unit='ms' , yearfirst=True)).tz_localize('UTC').tz_convert('Asia/Tehran')
        close = self.__data['close']
        detect = []
        for i in range(0, len(self.__data['close']) - 1):
            if close[i] < close[i + 1]:
                detect.append(1)
            else:
                detect.append(0)
        self.__data['detect'] = pd.DataFrame(detect)
        self.__data = self.__data.fillna(value=0)
        self.__data = self.__data.iloc[1:]
        self.__data['detect'] = self.__data['detect'].astype(int)
        return self.__data

