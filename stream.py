import asyncio
from binance import AsyncClient, BinanceSocketManager
from datetime import datetime
from Analysis.Analysis import *
import pandas as pd
from Account.demoAccount import Account
from ML.ML import BasicNeuralNetwork

def get_time_interval(time_frame):
    return {
        '1min': AsyncClient.KLINE_INTERVAL_1MINUTE,
        '3min': AsyncClient.KLINE_INTERVAL_3MINUTE,
        '5min': AsyncClient.KLINE_INTERVAL_5MINUTE,
        '15min': AsyncClient.KLINE_INTERVAL_15MINUTE,
        '30min': AsyncClient.KLINE_INTERVAL_30MINUTE,
        '1hour': AsyncClient.KLINE_INTERVAL_1HOUR,
        '2hour': AsyncClient.KLINE_INTERVAL_2HOUR,
        '4hour': AsyncClient.KLINE_INTERVAL_4HOUR,
        '6hour': AsyncClient.KLINE_INTERVAL_6HOUR,
        '8hour': AsyncClient.KLINE_INTERVAL_8HOUR,
        '12hour': AsyncClient.KLINE_INTERVAL_12HOUR,
        '1day': AsyncClient.KLINE_INTERVAL_1DAY,
        '3day': AsyncClient.KLINE_INTERVAL_3DAY,
        '1week': AsyncClient.KLINE_INTERVAL_1WEEK,
        '1month': AsyncClient.KLINE_INTERVAL_1MONTH,
    }.get(time_frame, AsyncClient.KLINE_INTERVAL_1MINUTE)
def handle_message(msg):
    if msg['e'] == 'error':
        print(msg['m'])
    else:
        bitcoins_exchanged = float(msg['p']) * float(msg['q'])
        timestamp = msg['T'] / 1000
        timestamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        if msg['m']:
            event_side = 'SELL'
        else:
            event_side = 'BUY '
        print("{} - {} - {} - Price: {} - Qty: {} BTC Qty: {}$".format(timestamp,
                                                                       event_side,
                                                                       msg['s'],
                                                                       msg['p'],
                                                                       msg['q'],bitcoins_exchanged))


class AsWebSocketClient:
    __symbol = None
    __data_live = None
    __time_frame= None
    __network=None
    __data_analysis = pd.DataFrame(columns=[ 'date' ,'recommend' ])
    __candle_counter = 0
    __noidea_time = None
    def __init__(self, client:Account, nn:BasicNeuralNetwork, symbol:str, time_frame:str= '1min', time:str= '00:00'):
        self.__symbol=symbol
        self.__time_frame =time_frame
        self.__network=nn
        self.__noidea_time = time
        self.__data_live = client.get_data(symbol=symbol , timeframe=time_frame)
        self.__client = client
        self.__data_live.drop(self.__data_live.tail(1).index , inplace=True) #remove duplicated row first
        self.__noidea_time = [int(word) for word in self.__noidea_time.split(':') if word.isdigit()]
    async def __real_time(self):
        client = await AsyncClient.create()
        bm = BinanceSocketManager(client)
        ts = bm.kline_socket(symbol=self.__symbol , interval=get_time_interval(self.__time_frame )) if self.__time_frame  == '1min' else bm.trade_socket(str(self.__symbol))
        async with ts as tscm:

            while True:
                res = await tscm.recv()
                if self.__time_frame  == '1min' and res['k']['x'] :
                    last_close_price = float(self.__data_live.tail(1).close) #save last price before new data append for compare new price and insert detect

                    time = pd.to_datetime(res['k']['t'] ,unit='ms' ,yearfirst=True).tz_localize('UTC').tz_convert('Asia/Tehran')
                    self.__data_live = self.__data_live.append({'date':time ,
                                                                'open':res['k']['o'] ,
                                                                'high':res['k']['h'] , 'low':res['k']['l'] ,
                                                                'close':res['k']['c'] ,'volume':res['k']['v'],
                                                                'QAV':res['k']['q'] ,'trades':res['k']['n'],
                                                                'TBAV':res['k']['V'] ,'TQAV':res['k']['Q'],
                                                                'Ignore':res['k']['B'] } , ignore_index=True)
                    self.__data_live.iloc[-2, self.__data_live.columns.get_loc('detect')] = int(1) if last_close_price <= float(res['k']['c']) else int(0)
                    ichi = get_indicators_col(self.__data_live).fillna(value=-1)
                    recom = ichimoku_recommend(price_data=self.__data_live , ichimoku=ichi)
                    train_input= recom.tail(1).astype(int)
                    del train_input['date']
                    print("Ml says: ")
                    re =self.__network.think(np.array(train_input))[0][0]
                    print(re)
                    self.__data_analysis = self.__data_analysis.append({'date':time,'recommend':re} ,ignore_index=True)
                    print(self.__data_analysis)
                    print(self.__data_live)
                    to_csv(data=self.__data_live , name='Static/data.csv')
                    to_csv(data=ichi , name='Static/ichimoku.csv')
                    to_csv(data=recom , name='Static/recommendation_ichimoku.csv')
                    to_csv(data=self.__data_analysis , name='Static/ml_recommendation.csv')

                    #update weights after n candles (for test)
                    # self.__candle_counter = self.__candle_counter + 1
                    # if self.__candle_counter == 5 :
                    #     # add new weights with new input and shift 1 others
                    #     new_time = self.__get_new_time(5)
                    #     #drop Nan value in tail
                    #     data_live_temp = self.__data_live[:-1]
                    #     recom_temp = recom[:-1]
                    #     training_inputs = recom_without_noidea(recom_temp, new_time)
                    #     training_outputs = get_detect(data=data_live_temp  ,start_time=new_time)
                    #     self.__network.train(training_inputs, training_outputs, 10000)
                    #     self.__candle_counter = 0
                elif self.__time_frame != '1min':
                    # handle_message(res)
                    print(res)
    #for update weights we need knows new time
    def __get_new_time(self , minute:int):
        # hour = int (minute / 60 )
        # minute = minute % 60
        # self.__noidea_time[0] = self.__noidea_time[0] + hour
        self.__noidea_time[1] = self.__noidea_time[1] + minute
        if self.__noidea_time[1] > 55 :
            self.__noidea_time[1] = 0
            self.__noidea_time[0] = self.__noidea_time[0] + 1

        if self.__noidea_time[1] < 10 :
            new_time = '{hour}:0{minute}'.format(hour=self.__noidea_time[0], minute=self.__noidea_time[1])
        if self.__noidea_time[0] < 10 :
            new_time = '0{hour}:{minute}'.format(hour=self.__noidea_time[0], minute=self.__noidea_time[1])
        if self.__noidea_time[0] >=10 and self.__noidea_time[1] >= 10 :
            new_time = '{hour}:{minute}'.format(hour=self.__noidea_time[0], minute=self.__noidea_time[1])
        else:
            new_time = '0{hour}:0{minute}'.format(hour=self.__noidea_time[0], minute=self.__noidea_time[1])
        return new_time


                    # await client.close_connection()

    def live_realtime_price(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__real_time())

