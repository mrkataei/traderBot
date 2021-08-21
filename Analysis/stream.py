"""
Mr.Kataei 8/15/2021
async functions for get data stream from binance socket for 30m , 1h , 4h , 1day timeframes and multiple symbols
.first you must init statics you have because when new data append date work truth , after that check your analysis
with csvs stored
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
from binance import AsyncClient ,BinanceSocketManager ,Client
import pandas as pd
from Libraries import data_collector
from Inc import db
from Analysis import ichimoku

connection = db.con_db()


def init_statics():
    #this method work with n parameters and return stored csvs in Static with 4 timeframes
    data_collector.generate_data("BTCUSDT" , "ETHUSDT")

#for append new row in our csvs , candle details from binance in bellow
def append(data:pd.DataFrame , symbol:str, timeframe:str , candle):
    """
        candle details
            {
                "e": "kline",					# event type
                "E": 1499404907056,				# event time
                "s": "ETHBTC",					# symbol
                "k": {
                    "t": 1499404860000, 		# start time of this bar
                    "T": 1499404919999, 		# end time of this bar
                    "s": "ETHBTC",				# symbol
                    "i": "1m",					# interval
                    "f": 77462,					# first trade id
                    "L": 77465,					# last trade id
                    "o": "0.10278577",			# open
                    "c": "0.10278645",			# close
                    "h": "0.10278712",			# high
                    "l": "0.10278518",			# low
                    "v": "17.47929838",			# volume
                    "n": 4,						# number of trades
                    "x": false,					# whether this bar is final
                    "q": "1.79662878",			# quote volume
                    "V": "2.34879839",			# volume of active buy
                    "Q": "0.24142166",			# quote volume of active buy
                    "B": "13279784.01349473"	# can be ignored
                }
            }
    """
    time = pd.to_datetime(candle['k']['T'], unit='ms', yearfirst=True).tz_localize('UTC').tz_convert('Asia/Tehran')
    data = data.append({'date': time,
                        'open': candle['k']['o'],
                        'high': candle['k']['h'], 'low': candle['k']['l'],
                        'close': candle['k']['c'], 'volume': candle['k']['v'],
                        'QAV': candle['k']['q'], 'trades': candle['k']['n'],
                        'TBAV': candle['k']['V'], 'TQAV': candle['k']['Q']}, ignore_index=True)
    data.to_csv(path_or_buf=f'Static/{symbol}-{timeframe}.csv' ,index=False)
    return data
#for now we have 2 coins and 2 parameters in future need loop for all coins
#there is 4 functions for 4 timeframes after all used in main async
async def stream_30min_candle(*symbols:str ,socket:BinanceSocketManager):
    # count = 0
    data0_30min = pd.read_csv(f'Static/{symbols[0]}-30min.csv')
    data1_30min = pd.read_csv(f'Static/{symbols[1]}-30min.csv')
    candle0_30min = socket.kline_socket(symbol=symbols[0], interval=Client.KLINE_INTERVAL_30MINUTE)
    candle1_30min = socket.kline_socket(symbol=symbols[1], interval=Client.KLINE_INTERVAL_30MINUTE)
    async with candle0_30min ,candle1_30min:
        while True:
            c_30m_data0 = await candle0_30min.recv()
            c_30m_data1 = await candle1_30min.recv()
            if c_30m_data0['k']['x']:
                data0_30min = append(data0_30min ,symbols[0] ,"30min" ,c_30m_data0 )
                ichimoku.signal(data=data0_30min ,gain=0.003 ,cost=1,coin_id=1 ,timeframe_id=1)
                # count +=1
            if c_30m_data1['k']['x']:
                data1_30min = append(data1_30min ,symbols[1] ,"30min" ,c_30m_data1 )
                ichimoku.signal(data=data1_30min ,gain=0.003 ,cost=1,coin_id=2 ,timeframe_id=1)
                # count += 1

            # 30min sleep for new data
            # if count == 2:
            #     count = 0
            #     await asyncio.sleep(1798)

async def stream_1hour_candle(*symbols:str ,socket:BinanceSocketManager):
    # count = 0
    data0_1hour = pd.read_csv(f'Static/{symbols[0]}-1hour.csv')
    data1_1hour = pd.read_csv(f'Static/{symbols[1]}-1hour.csv')
    candle0_1hour = socket.kline_socket(symbol=symbols[0], interval=Client.KLINE_INTERVAL_1HOUR)
    candle1_1hour = socket.kline_socket(symbol=symbols[1], interval=Client.KLINE_INTERVAL_1HOUR)
    async with candle0_1hour ,candle1_1hour:
        while True:
            c_1h_data0 = await candle0_1hour.recv()
            c_1h_data1 = await candle1_1hour.recv()
            if c_1h_data0['k']['x']:
                data0_1hour = append(data0_1hour , symbols[0] ,"1hour",c_1h_data0)
                ichimoku.signal(data=data0_1hour, gain=0.003, cost=1, coin_id=1, timeframe_id=2)
                # count += 1

            if c_1h_data1['k']['x']:
                data1_1hour = append(data1_1hour , symbols[1] ,"1hour",c_1h_data1)
                ichimoku.signal(data=data1_1hour, gain=0.003, cost=1, coin_id=2, timeframe_id=2)
                # count += 1

            # 1hour sleep for new data
            # if count == 2:
            #     count = 0
            #     await asyncio.sleep(3598)

async def stream_4hour_candle(*symbols:str ,socket:BinanceSocketManager):
    # count = 0
    data0_4hour = pd.read_csv(f'Static/{symbols[0]}-4hour.csv')
    data1_4hour = pd.read_csv(f'Static/{symbols[1]}-4hour.csv')
    candle0_4hour = socket.kline_socket(symbol=symbols[0], interval=Client.KLINE_INTERVAL_4HOUR)
    candle1_4hour = socket.kline_socket(symbol=symbols[1], interval=Client.KLINE_INTERVAL_4HOUR)
    async with candle0_4hour ,candle1_4hour:
        while True:
            c_4h_data0 = await candle0_4hour.recv()
            c_4h_data1 = await candle1_4hour.recv()
            if c_4h_data0['k']['x']:
                data0_4hour = append(data0_4hour, symbols[0],"4hour", c_4h_data0)
                ichimoku.signal(data=data0_4hour, gain=0.003, cost=1, coin_id=1, timeframe_id=3)
                # count += 1

            if c_4h_data1['k']['x']:
                data1_4hour = append(data1_4hour, symbols[1],"15min", c_4h_data1)
                ichimoku.signal(data=data1_4hour, gain=0.003, cost=1, coin_id=2, timeframe_id=3)
                # count += 1

            #sleep 4hours for new data
            # if count == 2:
            #     count = 0
            #     await asyncio.sleep(14398)

async def stream_1day_candle(*symbols:str ,socket:BinanceSocketManager):
    # count = 0
    data0_1day = pd.read_csv(f'Static/{symbols[0]}-1day.csv')
    data1_1day = pd.read_csv(f'Static/{symbols[1]}-1day.csv')
    candle0_1day = socket.kline_socket(symbol=symbols[0], interval=Client.KLINE_INTERVAL_1DAY)
    candle1_1day = socket.kline_socket(symbol=symbols[1], interval=Client.KLINE_INTERVAL_1DAY)
    async with candle0_1day ,candle1_1day:
        while True:
            c_1d_data0 = await candle0_1day.recv()
            c_1d_data1 = await candle1_1day.recv()
            if c_1d_data0['k']['x']:
                data0_1day = append(data0_1day, symbols[0],"1day", c_1d_data0)
                ichimoku.signal(data=data0_1day, gain=0.003, cost=1, coin_id=1, timeframe_id=4)
                # count +=1
            if c_1d_data1['k']['x']:
                data1_1day = append(data1_1day, symbols[1],"1day", c_1d_data1)
                ichimoku.signal(data=data1_1day, gain=0.003, cost=1, coin_id=2, timeframe_id=4)
                # count +=1
            # sleep 24hour for new data
            # if count == 2:
            #     count = 0
            #     await asyncio.sleep(86398)

async def stream():
    #init statics for clean date
    init_statics()
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    await asyncio.gather(stream_30min_candle("BTCUSDT" , "ETHUSDT" ,socket=bm) ,
                         stream_1hour_candle("BTCUSDT" , "ETHUSDT" ,socket=bm) ,
                         stream_4hour_candle("BTCUSDT" , "ETHUSDT" ,socket=bm) ,
                         stream_1day_candle("BTCUSDT" , "ETHUSDT" ,socket=bm))

#use this in main
def run():
    asyncio.run(stream())