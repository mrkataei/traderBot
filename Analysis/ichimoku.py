import asyncio
from binance import AsyncClient, BinanceSocketManager
import pandas as pd
import pandas_ta as ta
from time import sleep
from Libraries import data_collector

def init_statics():
    data_collector.generate_data("BTCUSDT")
    data_collector.generate_data("ETHUSDT")

async def stream_30min_candles(symbol:str):
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    data = pd.read_csv('../Static/BTCUSDT-1min.csv')
    ts = bm.kline_socket(symbol=symbol, interval=client.KLINE_INTERVAL_1MINUTE)

    async with ts as tscm:
        while True:
            res = await tscm.recv()
            if res['k']['x']:
                time = pd.to_datetime(res['k']['t'], unit='ms', yearfirst=True).tz_localize('UTC').tz_convert('Asia/Tehran')
                data = data.append({'date': time,
                                    'open': res['k']['o'],
                                    'high': res['k']['h'], 'low': res['k']['l'],
                                    'close': res['k']['c'], 'volume': res['k']['v'],
                                    'QAV': res['k']['q'], 'trades': res['k']['n'],
                                    'TBAV': res['k']['V'], 'TQAV': res['k']['Q']}, ignore_index=True)
                data.to_csv(path_or_buf='../Static/BTCUSDT-1min.csv' ,index=False)
                print(data)
                sleep(59)


    await client.close_connection()
# #
# if __name__ == "__main__":
#
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(stream_30min_candles("BTCUSDT"))