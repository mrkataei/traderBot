import asyncio
from binance import AsyncClient, BinanceSocketManager
from datetime import datetime
from Analysis import *
import pandas as pd


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
    def __init__(self , symbol:str , data:pd.DataFrame):
        self.__symbol=symbol
        self.__data_live = data
    async def real_time(self , time_frame:str):
        client = await AsyncClient.create()
        bm = BinanceSocketManager(client)
        ts = bm.kline_socket(symbol=self.__symbol , interval=get_time_interval(time_frame)) if time_frame == '1min' else bm.trade_socket(str(self.__symbol))

        async with ts as tscm:
            while True:
                res = await tscm.recv()
                if time_frame == '1min' and res['k']['x'] :
                    self.__data_live = self.__data_live.append({'date':pd.to_datetime(res['k']['t'] ,unit='ms') ,
                                                                'open':res['k']['o'] ,
                                                                'high':res['k']['h'] , 'low':res['k']['l'] ,
                                                                'close':res['k']['c'] ,'volume':res['k']['v'],
                                                                'QAV':res['k']['q'] ,'trades':res['k']['n'],
                                                                'TBAV':res['k']['V'] ,'TQAV':res['k']['Q'],
                                                                'Ignore':res['k']['B']} , ignore_index=True)
                    self.__data_live = cast_to_float(self.__data_live)
                    ichi = get_indicators_col(self.__data_live).fillna(value=0)
                    recom = ichimoku_recommend(price_data=self.__data_live , ichimoku=ichi)

                    print(self.__data_live)
                    to_csv(data=self.__data_live , name='live.csv')
                    to_csv(data=ichi , name='ichimuko.csv')
                    to_csv(data=recom , name='recomIchi.csv')
                elif time_frame != '1min':
                    handle_message(res)


        # await client.close_connection()

    def live_realtime_price(self , time_frame:str='1min'):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.real_time(time_frame=time_frame))

