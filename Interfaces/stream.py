import asyncio
from binance import AsyncClient, BinanceSocketManager
from Inc import db, functions
import pandas as pd


# for append new row in our CSVs , candle details from binance in bellow
def append(data: pd.DataFrame, symbol: str, timeframe: str, candle):
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
                        'open': float(candle['k']['o']),
                        'high': float(candle['k']['h']), 'low': float(candle['k']['l']),
                        'close': float(candle['k']['c']), 'volume': float(candle['k']['v']),
                        'QAV': float(candle['k']['q']), 'trades': float(candle['k']['n']),
                        'TBAV': float(candle['k']['V']), 'TQAV': float(candle['k']['Q'])}, ignore_index=True)
    data.to_csv(path_or_buf=f'Static/{symbol}-{timeframe}.csv', index=False)
    return data


class Stream:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.connection = db.con_db()
        self.coin_id = functions.get_coin_id(self.connection, symbol)
        self.client = None
        self.socket = None
        self.data_30min = pd.read_csv(f'Static/{self.symbol}-30min.csv')
        self.data_1hour = pd.read_csv(f'Static/{self.symbol}-1hour.csv')
        self.data_4hour = pd.read_csv(f'Static/{self.symbol}-4hour.csv')
        self.data_1day = pd.read_csv(f'Static/{self.symbol}-1day.csv')

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

    def get_setting_analysis(self, analysis_id: int, timeframe_id: int):
        settings = functions.get_analysis_setting(db_connection=self.connection, coin_id=self.coin_id,
                                                  timeframe_id=timeframe_id, analysis_id=analysis_id)
        return settings

    def run(self):
        asyncio.run(self.stream())
