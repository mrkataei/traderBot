"""
Arman hajimirza
"""
import pandas as pd
import pandas_ta as ta
import numpy as np

def get_ichimoku(data:pd.DataFrame , tenkan:int=9 , kijun:int=26 , senkou:int=52):

    ichimoku = pd.DataFrame(data.ta.ichimoku(tenkan=tenkan , kijun=kijun , senkou=senkou)[0])
    ichimoku.columns = ['spanA' ,'spanB' ,'tenkensen' ,'kijunsen' ,'chiku']
    return ichimoku

def signal(data:pd.DataFrame):
    ichimoku = get_ichimoku(data)
    ichimoku['close'] = data.close
    ichimoku['date'] = data.date
    ichimoku = ichimoku.dropna()
    ichimoku = ichimoku.reset_index(drop=True)

    def buy_signals(current):
        status = False
        # first signal
        # close<spanA<spanB
        if (ichimoku.loc[current,'spanA'] < ichimoku.loc[current, 'spanB'] and ichimoku.loc[current, "close"] < ichimoku.loc[current,'spanA']):
            # laggingspan_i < close_i & laggingspan_i-1 < close_i-1
            if (ichimoku.loc[current - 1, 'chiku'] < ichimoku.loc[current - 1, "close"] and ichimoku.loc[current, 'chiku'] < ichimoku.loc[
                current, "close"]):
                # Kijunsen_i > close_i & Kijunsen_i-1 > close_i-1
                if (ichimoku.loc[current - 1, 'kijunsen'] > ichimoku.loc[current - 1, "close"] and ichimoku.loc[current, 'kijunsen'] > ichimoku.loc[
                    current, "close"]):
                    # Tenkensen_i > close_i & Tenkensen_i-1 > close_i-1
                    if (ichimoku.loc[current - 1, 'tenkensen'] > ichimoku.loc[current - 1, "close"] and ichimoku.loc[current, 'tenkensen'] > ichimoku.loc[
                        current, "close"]):
                        # spanA_i - spanA_i-10 > 0
                        if (ichimoku.loc[current,'spanA'] - ichimoku.loc[current - 10,'spanA'] > 0):
                            status = True
                            return status
        # second signal
        # close>spanA>spanB
        elif (ichimoku.loc[current,'spanA'] > ichimoku.loc[current, 'spanB'] and ichimoku.loc[current, "close"] > ichimoku.loc[current,'spanA']):
            # laggingspan_i > close_i & laggingspan_i-1 > close_i-1
            if (ichimoku.loc[current - 1, 'chiku'] < ichimoku.loc[current - 1, "close"] and ichimoku.loc[current, 'chiku'] < ichimoku.loc[
                current - 1, "close"]):
                # Tenkensen_i > close_i & Tenkensen_i-1 > close_i-1
                if (ichimoku.loc[current - 1, 'tenkensen'] > ichimoku.loc[current - 1, "close"] and ichimoku.loc[current, 'tenkensen'] > ichimoku.loc[
                    current, "close"]):
                    # spanA_i>spanA_i-10 , spanB_i>spanB_i-10
                    if (ichimoku.loc[current,'spanA'] - ichimoku.loc[current - 10,'spanA'] > 0 and ichimoku.loc[current, 'spanB'] - ichimoku.loc[
                        current - 10, 'spanB'] > 0):
                        status = True
                        return status

        return status

    def sell_signals(current):
        status = False
        # firstsignal
        # close>spanA>spanB
        if (ichimoku.loc[current,'spanA'] > ichimoku.loc[current, 'spanB'] and ichimoku.loc[current, "close"] > ichimoku.loc[current,'spanA']):
            # Tenkensen_i < close_i & Tenkensen_i-1 < close_i-1
            if (ichimoku.loc[current - 1, 'tenkensen'] < ichimoku.loc[current - 1, "close"] and ichimoku.loc[current, 'tenkensen'] < ichimoku.loc[
                current, "close"]):
                # Kijunsen_i < close_i & Kijunsen_i-1 < close_i-1
                if (ichimoku.loc[current - 1, 'kijunsen'] < ichimoku.loc[current - 1, "close"] and ichimoku.loc[current, 'kijunsen'] < ichimoku.loc[
                    current, "close"]):
                    # laggingspan_i > close_i & laggingspan_i-1 > close_i-1
                    if (ichimoku.loc[current - 1, 'chiku'] > ichimoku.loc[current - 1, "close"] and ichimoku.loc[current, 'chiku'] > ichimoku.loc[
                        current, "close"]):
                        # spanA_i - spanA_i-10 > 0 , spanB_i - spanB_i-10 != 0
                        if (ichimoku.loc[current,'spanA'] - ichimoku.loc[current - 10,'spanA'] > 0 and ichimoku.loc[current, 'spanB'] -
                                ichimoku.loc[current - 10, 'spanB'] != 0):
                            status = True
                            return status
        # secondsignal
        # close<spanA<spanB
        elif (ichimoku.loc[current,'spanA'] < ichimoku.loc[current, 'spanB'] and ichimoku.loc[current, "close"] < ichimoku.loc[current,'spanA']):
            # spanA_i - spanA_i-5  >  spanB_i - spanB_i-5
            if (ichimoku.loc[current,'spanA'] - ichimoku.loc[current - 5,'spanA'] > ichimoku.loc[current, 'spanB'] - ichimoku.loc[
                current - 5, 'spanB']):
                # Tenkensen_i - Tenkensen_i-5 > Kijunsen_i - Kijunsen_i-5
                if (ichimoku.loc[current, 'tenkensen'] - ichimoku.loc[current - 5, 'tenkensen'] > ichimoku.loc[current, 'kijunsen'] - ichimoku.loc[
                    current - 5, 'kijunsen']):
                    # spanA_i - spanA_i-10 < 0 , spanB_i - spanB_i-10 != 0
                    if (ichimoku.loc[current,'spanA'] - ichimoku.loc[current - 10,'spanA'] < 0 and ichimoku.loc[current, 'spanB'] - ichimoku.loc[
                        current - 10, 'spanB'] != 0):
                        # laggingspan_i > close_i & laggingspan_i-1 > close_i-1
                        if (ichimoku.loc[current - 1, 'chiku'] > ichimoku.loc[current - 1, "close"] and ichimoku.loc[current, 'chiku'] >
                                ichimoku.loc[current, "close"] and ichimoku.loc[current + 1, 'chiku'] > ichimoku.loc[current + 1, "close"]):
                            status = True
                            return status
        return status

    def analyse():
        count = 0
        for i in range(10, len(ichimoku) - 1):
            if buy_signals(i):
                count +=1
                ichimoku.loc[i, "status"] = "Buy"
            elif sell_signals(i):
                count += 1
                ichimoku.loc[i, "status"] = "Sell"
        print(count)
    analyse()
    ichimoku.to_csv('test.csv')
    print(ichimoku)

signal(pd.read_csv('../Static/BTCUSDT-30min.csv'))