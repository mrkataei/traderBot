"""
Arman hajimirza & Mr.Kataei
"""
import pandas as pd
import pandas_ta as ta


import numpy as np

def get_ichimoku(data:pd.DataFrame , tenkan:int=9 , kijun:int=26 , senkou:int=52):

    ichimoku = pd.DataFrame(data.ta.ichimoku(tenkan=tenkan , kijun=kijun , senkou=senkou)[0])
    ichimoku.columns = ['spanA' ,'spanB' ,'tenkensen' ,'kijunsen' ,'chiku']
    #continious rows from clouds
    def get_future_spans():
        ichimoku_future = pd.DataFrame(data.ta.ichimoku(tenkan=tenkan , kijun=kijun , senkou=senkou)[1])
        ichimoku_future.columns = ['spanA', 'spanB']
        return ichimoku_future
    return ichimoku ,get_future_spans()

def signal(data:pd.DataFrame):
    ichimoku_all = get_ichimoku(data)
    ichimoku = ichimoku_all[0]
    future = ichimoku_all[1]
    ichimoku['close'] = data.close
    ichimoku['date'] = data.date
    ichimoku['change'] = ichimoku['close'].pct_change()
    future['signal'] = np.where(future['spanA']>=future['spanB'] , 'buy' , 'sell')
    print(future)
    ichimoku.change = ichimoku.change.shift(-1)
    # ichimoku['tenkensen-rec'] = np.where(ichimoku['tenkensen'] == -1, -1,
    #                                  np.where(ichimoku['tenkensen'] < ichimoku['close'], 1, 0)).astype(int)
    # ichimoku['kijunsen-rec'] = np.where(ichimoku['kijunsen'] == -1, -1,
    #                                 np.where(ichimoku['kijunsen'] < ichimoku['close'], 1, 0)).astype(int)
    # ichimoku['spanA-rec'] = np.where(ichimoku['spanA'] == -1, -1,
    #                              np.where(ichimoku['spanA'] < ichimoku['close'], 1, 0)).astype(int)
    # ichimoku['spanB-rec'] = np.where(ichimoku['spanB'] == -1, -1,
    #                              np.where(ichimoku['spanB'] < ichimoku['close'], 1, 0)).astype(int)
    # ichimoku['chiku-rec'] = np.where(ichimoku['chiku'] == -1, -1,
    #                              np.where(ichimoku['chiku'] > ichimoku['close'], 1, 0)).astype(int)
    # ichimoku['kijunAndspanBCross'] = np.where(ichimoku['spanB'] == -1, -1,
    #                                           np.where(ichimoku['kijunsen'] == ichimoku['spanB'], -1,
    #                                                    np.where(ichimoku['kijunsen'] > ichimoku['spanB'], 1, 0))).astype(
    #     int)
    # ichimoku['tenkensenAndkijunsen'] = np.where(ichimoku['kijunsen'] == -1, -1,
    #                                             np.where(ichimoku['tenkensen'] == ichimoku['kijunsen'], 0,
    #                                                      np.where(ichimoku['tenkensen'] > ichimoku['kijunsen'], 1,
    #                                                               0))).astype(int)
    # ichimoku['priceAndABspan'] = np.where(ichimoku['spanB'] == -1, -1, np.where(ichimoku['spanA'] == 0, 0,
    #                                                                             np.where(ichimoku['spanB'] == 1, 1,
    #                                                                                      0))).astype(int)
    # ichimoku['tenkensenAndPriceWithKijunsen'] = np.where(ichimoku['kijunsen'] == -1, -1,
    #                                                      np.where(ichimoku['tenkensen'] == 0, 0,
    #                                                               np.where(ichimoku['tenkensen'] > ichimoku['kijunsen'], 1,
    #                                                                        0))).astype(int)
    # ichimoku['sAAndB'] = np.where(ichimoku['spanB'] == -1, -1,
    #                               np.where(ichimoku['spanA'] >= ichimoku['spanB'], 1, 0)).astype(int)
    #
    # ichimoku.chiku = ichimoku.chiku.shift(26)  # shif 26 rows for chiku
    # # ichimoku.chiku = ichimoku.chiku.fillna(value=-1)  # fill 26 first data that shifted with -1
    # ichimoku['sum'] = ichimoku['tenkensen-rec'] + ichimoku['kijunsen-rec'] + ichimoku['spanA-rec'] \
    #                   + ichimoku['spanB-rec'] + ichimoku['chiku-rec'] + ichimoku['kijunAndspanBCross']\
    #                   + ichimoku['tenkensenAndkijunsen'] + ichimoku['priceAndABspan'] +\
    #                   ichimoku['tenkensenAndPriceWithKijunsen']+ ichimoku['sAAndB']

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
        for i in range(0, len(ichimoku)):
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

signal(pd.read_csv('../Static/BTCUSDT-1hour.csv'))