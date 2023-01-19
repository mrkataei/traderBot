"""
    Mr.kataei 1/3/2022
"""
from Libraries.data_collector import *
import pandas_ta as ta
import pandas as pd

exchange = Exchange.bitfinex
symbol = Symbols.BTCUSDT


# data = get_all_candles_binance(exchange=exchange, symbol=symbol, number=4, unit='h', save_csv=False)


def willr(dataframe: pd.DataFrame, length: int = 14):
    try:
        return ta.willr(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], length=length)
    except Exception as e:
        print(f'invalid dataframe: {e}')


def cmo(dataframe: pd.DataFrame, length: int = 14, scalar: int = 100):
    try:
        return ta.cmo(close=dataframe['close'], length=length, scalar=scalar)
    except Exception as e:
        print(f'invalid dataframe: {e}')


def sma(dataframe: pd.DataFrame, length: int = 14):
    try:
        t = ta.sma(close=dataframe['close'], length=length)
        t.name = f'sma_{length}'
        return t.to_frame()
    except Exception as e:
        print(f'invalid dataframe: {e}')


def mfi(dataframe: pd.DataFrame, length: int = 14):
    try:
        t = ta.mfi(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'],
                      volume=dataframe['volume'], length=length)
        t.name = f'mfi_{length}'
        return t.to_frame()
        return
    except Exception as e:
        print(f'invalid dataframe: {e}')


def stochRsi(dataframe: pd.DataFrame, length: int = 14, rsi_length: int = 14, k: int = 3, d: int = 3):
    try:
        return ta.stochrsi(close=dataframe['close'], length=length, rsi_length=rsi_length, k=k, d=d)
    except Exception as e:
        print(f'invalid dataframe: {e}')


def generate_dataset(dataframe: pd.DataFrame):
    """
    **need must functional in future**
    :param dataframe: dataframe ohclv
    :return: indicators with dataframe
    """
    stoch_rsi_indicator = stochRsi(dataframe=dataframe)
    mfi_indicator = mfi(dataframe=dataframe)
    cmo_indicator = cmo(dataframe=dataframe)
    willr_indicator = willr(dataframe=dataframe)

    temp = pd.concat([stoch_rsi_indicator, mfi_indicator, cmo_indicator, willr_indicator], axis=1)
    temp.columns = ["stoch_k", "stoch_d", "mfi", "cmo", "willr"]
    dataframe = pd.concat([dataframe, temp], axis=1)
    return dataframe
