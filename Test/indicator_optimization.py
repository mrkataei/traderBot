import numpy as np
import itertools
import pandas as pd
import pandas_ta as ta
import time
from multiprocessing import Process, Value, Array
from functools import partial

start_time = time.time()
from multiprocessing import Pool
from Libraries.macd import macd_indicator
from Test.strategy_tester import StrategyTaster, change_date_type


# test = [['fast', 5, 7],
#         ['slow', 13, 16],
#         ['signal', 26, 30],
#         ['source', 'low', 'high', 'close', 'open', 'hlc2', 'hlc3', 'ohlc4'],
#         ['MA', 'ema', 'sma', 'wma']
#         ]

# print(np.shape(test))


def set_rec(row):
    x = row['buy']
    y = row['sell']
    return 'buy' if x == 1 else 'sell' if y == 1 else None


def set_rec_stoch(row, overbuy, oversell):
    if row > overbuy:
        return "buy"
    elif row < oversell:
        return 'sell'


def get_source(data: pd.DataFrame, source: str = 'close'):
    return {
        'hl2': data.ta.hl2(),
        'hlc3': data.ta.hlc3(),
        'ohlc4': data.ta.ohlc4(),
        'close': data['close'],
        'high': data['high'],
        'low': data['low'],
        'open': data['open']
    }.get(source, data['close'])


# fast, slow, signal, source, MA type
# (10, 24),(20,52),(6,16),(low, high, close, open, hl2, hlc3, ohlo4), (ema, sma, wma)

# %%


# print(np.shape(elements)[0])

# data = pd.read_csv(r"C:\Users\Asus\Downloads\ETHUSDT4h-2021.csv")


def process_macd_setting(obj, data):
    macd = macd_indicator(close=get_source(data=data, source=obj[3]), fast=obj[0],
                          slow=obj[1],
                          signal=obj[2],
                          matype=obj[4])
    macd.columns = ["macd", "histogeram", "signal"]
    # print(macd)
    data['buy'] = ta.cross(macd['macd'], macd['signal'])
    # print(df['recommendation'])
    data['sell'] = ta.cross(macd['macd'], macd['signal'], above=False)
    data["recommendation"] = data.apply(lambda row: set_rec(row), axis=1)
    # print(dataframe)
    try:
        test = StrategyTaster(name=f'test{obj}', symbol="ETHUSDT", timeframe="4hr", dataframe=data, intial_value=100)
        # data.drop(columns=["buy" , "sell" , "recommendation"])
        return test.results()
    except:
        print(f"test{obj}")


def process_stochrsi_setting(obj, data):
    stoch = ta.stochrsi(k=obj[0], d=obj[1], length=obj[2], rsi_length=obj[3], close=get_source(data, obj[4]))
    stoch.columns = ["stochrsi_k", "stochrsi_d"]

    data["recommendation"] = stoch['stochrsi_k'].apply(lambda row: set_rec_stoch(row, overbuy=obj[5], oversell=obj[6]))
    try:
        test = StrategyTaster(name=f'test{obj}', symbol="ETHUSDT", timeframe="4hr", dataframe=data, intial_value=100)
        print(1)
        # data.drop(columns=["buy" , "sell" , "recommendation"])
        return test.results()
    except:
        print(2)
        print(f"test{obj}")


def get_elements(test, setting_size: int):
    adad = []
    for i in range(len(test)):
        if isinstance(test[i][1], int):
            adad.append(np.arange(test[i][1], test[i][2] + 1, 1).tolist())
        elif isinstance(test[i][1], str):
            adad.append((test[i])[1:])

    # print(adad)
    # %%
    if setting_size == 5:
        elements = []
        for element in itertools.product(adad[0], adad[1], adad[2], adad[3], adad[4]):
            elements.append(list(element))
        return elements
    if setting_size == 7:
        elements = []
        for element in itertools.product(adad[0], adad[1], adad[2], adad[3], adad[4], adad[5], adad[6]):
            elements.append(list(element))
        return elements


if __name__ == "__main__":
    # counter = 0
    pd.set_option('display.max_columns', None)
    df = pd.read_csv(r"C:\Users\Asus\Downloads\ETHUSDT4h-2021.csv")
    fuck = pd.DataFrame(columns=['strategy', 'symbol', 'timefarme', 'starttime', 'endtime',
                                 "positive_trades", "total_trades", "acurracy-%",
                                 "net_profit-%", "average_trade_profit-%",
                                 'profit_per_coin-%'])
    df["date"] = df['date'].apply(lambda x: change_date_type(x))
    macd_ranges = [['fast', 5, 12],
                   ['slow', 11, 20],
                   ['signal', 22, 48],
                   ['source', 'low', 'high', 'close', 'open', 'hlc2', 'hlc3', 'ohlc4'],
                   ['MA', 'ema', 'sma', 'wma']
                   ]

    stochrsi_ranges = [['k', 3, 5],
                       ['d', 3, 5],
                       ['length', 50, 57],
                       ['rsi_length', 50, 57],
                       ['source', 'low', 'high', 'close', 'open', 'hlc2', 'hlc3', 'ohlc4'],
                       ['overbuy', 70, 100],
                       ['oversell', 0, 30]
                       ]

    pool = Pool()

    # elements = get_elements(macd_ranges, setting_size=5)[:1000]
    elements = get_elements(stochrsi_ranges, setting_size=7)
    # print(elements)
    pss = partial(process_stochrsi_setting, data=df.copy(deep=True))
    pms = partial(process_macd_setting, data=df.copy(deep=True))
    f = pool.map(pss, elements[50000:50005])
    fuck = fuck.append(f)
    # gpu_test_macd[1, 1](elements, da=df, result_df=fuck)
    # gpu_test[4, 5](x)
    print(fuck)
    print(fuck.shape)
    # fuck.to_csv("multiprocess_ETHUSDT4h-2021.csv")
    print("--- %s seconds ---" % (time.time() - start_time))

# print(macd_elements(stochrsi_ranges, setting_size=7))

# stochrsi_ranges = [['k', 3, 5],
#                    ['d', 3, 5],
#                    ['length', 50, 57],
#                    ['rsi_length', 50, 57],
#                    ['source', 'low', 'high', 'close', 'open', 'hlc2', 'hlc3', 'ohlc4'],
#                    ['overbuy', 70, 100],
#                    ['oversell', 0, 30]
#                    ]
# x = get_elements(stochrsi_ranges, setting_size=7)
# print(x[0:5])
# print(np.array(x).shape)
