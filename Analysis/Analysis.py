import pandas as pd
import matplotlib.pyplot as plt
import pandas_ta as ta
import numpy as np

# aberration, above, above_value, accbands, ad, adosc, adx,\
# alma, amat, ao, aobv, apo, aroon, atr, bbands, below, below_value,\
# bias, bop, brar, cci, cdl_doji, cdl_inside, cfo, cg, chop, cksp,\
# cmf, cmo, coppock, cross, cross_value, decay, decreasing, dema, \
# donchian, dpo, ebsw, efi, ema, entropy, eom, er, eri, fisher,\
# fwma, ha, hilo, hl2, hlc3, hma, hwc, hwma, ichimoku, increasing, \
# inertia, kama, kc, kdj, kst, kurtosis, linreg, log_return, long_run,\
# macd, mad, massi, mcgd, median, mfi, midpoint, midprice, mom, natr,\
# nvi, obv, ohlc4, pdist, percent_return, pgo, ppo, psar, psl, pvi, \
# pvo, pvol, pvr, pvt, pwma, qqe, qstick, quantile, rma, roc, rsi,\
# rsx, rvgi, rvi, short_run, sinwma, skew, slope, sma, smi, squeeze, \
# ssf, stdev, stoch, stochrsi, supertrend, swma, t3, tema, thermo, \
# trend_return, trima, trix, true_range, tsi, ttm_trend, ui, uo, variance,\
# vidya, vortex, vp, vwap, vwma, wcp, willr, wma, zlma, zscore
#stockrsix , ichimoku , rsi
#data must has same name column name such open , close , high , low


def to_csv(data:pd.DataFrame , path:str='' , name:str='data.csv'):
    data.to_csv(path + name)

def get_indicators_col(data:pd.DataFrame, name:str= 'ichimoku'):
    data = cast_to_float(data).fillna(value=-1)
    return {
        'ichimoku' : data.ta.ichimoku(tenkan=10, kijun=30 , senkou=60)[0],
        'macd'     : data.ta.macd(),
        'stochrsi' : data.ta.stochrsi()
    }.get(name ,data.ta.ichimoku()[0])


def cast_to_float(data:pd.DataFrame):
    data['open'] = data['open'].astype(float)
    data['high'] = data['high'].astype(float)
    data['close'] = data['close'].astype(float)
    data['low'] = data['low'].astype(float)
    return data


def ichimoku_recommend(price_data:pd.DataFrame, ichimoku:pd.DataFrame):
    col = [ 'date','tenkensen', 'kijunsen', 'spanA', 'spanB', 'chiku' ,
           'kijunAndSpanBCross' , 'tenkensenAndkijunsen' , 'priceAndABSpan' ,
           'tenkensenAndPriceWithKijunsen' ,'sAAndB']

    #ISA->SpanA->col0 , ISB-> SpanB -> col1 , ITS->tenkensen->col2 , IKS->kijunsen->col3 , ICS_26->chiku->col4

    SpanA = ichimoku.columns[0]
    SpanB = ichimoku.columns[1]
    tenkensen = ichimoku.columns[2]
    kijunsen = ichimoku.columns[3]
    chiku = ichimoku.columns[4]

    #-1 no idea , 0 sell ,  1 buy
    recommend = pd.DataFrame(columns=col)
    recommend['date'] = price_data ['date']
    recommend['tenkensen'] = np.where(ichimoku[tenkensen] == -1, -1, np.where(ichimoku[tenkensen] < price_data['close'], 1, 0)).astype(int)
    recommend['kijunsen'] = np.where(ichimoku[kijunsen] == -1, -1, np.where(ichimoku[kijunsen] < price_data['close'], 1, 0)).astype(int)
    recommend['spanA'] = np.where(ichimoku[SpanA] == -1, -1, np.where(ichimoku[SpanA] < price_data['close'], 1, 0)).astype(int)
    recommend['spanB'] = np.where(ichimoku[SpanB] == -1, -1, np.where(ichimoku[SpanB] < price_data['close'], 1, 0)).astype(int)
    recommend['chiku'] = np.where(ichimoku[chiku] ==-1 , -1 , np.where(ichimoku[chiku] > price_data['close'], 1, 0) ).astype(int)
    recommend['kijunAndSpanBCross'] = np.where(ichimoku[SpanB] == -1 , -1 ,np.where(ichimoku[kijunsen] == ichimoku[SpanB] ,-1 , np.where(ichimoku[kijunsen] > ichimoku[SpanB] ,1 , 0))).astype(int)
    recommend['tenkensenAndkijunsen'] = np.where(ichimoku[kijunsen] == -1 ,-1 ,  np.where(ichimoku[tenkensen] == ichimoku[kijunsen],0 ,np.where(ichimoku[tenkensen] >ichimoku[kijunsen] , 1 , 0))).astype(int)
    recommend['priceAndABSpan'] = np.where(ichimoku[SpanB] == -1 , -1 ,np.where(recommend['spanA'] ==0 ,0 , np.where(recommend['spanB']==1 ,1 ,0 ))).astype(int)
    recommend['tenkensenAndPriceWithKijunsen'] = np.where(ichimoku[kijunsen] == -1, -1 , np.where(recommend['tenkensen'] ==0 ,0 ,np.where(ichimoku[tenkensen] >ichimoku[kijunsen] , 1 , 0))).astype(int)
    recommend['sAAndB'] = np.where(ichimoku[SpanB] == -1 , -1  , np.where(ichimoku[SpanA] >= ichimoku[SpanB] , 1 , 0)).astype(int)
    recommend.chiku = recommend.chiku.shift(26) #shif 26 rows for chiku
    recommend.chiku = recommend.chiku.fillna(value=-1) #fill 26 first data that shifted with -1
    # recommend.astype(int)
    return recommend
def sum_sell_buy(symbol_data:pd.DataFrame , indicator_recommendations:pd.DataFrame):
    col = ['buy' , 'sell' , 'recommendation']
    element_numbers = len(indicator_recommendations.columns) - 1
    regression =  pd.DataFrame(columns=col)
    regression['buy'] = indicator_recommendations.sum(axis=1)
    #
    regression['recommendation'] = symbol_data['close'].pct_change()
    regression.recommendation = regression.recommendation.shift(-1)
    regression['sell'] =  element_numbers - regression['buy']
    def draw_plot():
        x = regression['buy']
        y = regression['sell']
        z = regression['recommendation']
        fig = plt.figure()
        fig.add_subplot()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel("buy")
        ax.set_ylabel("sell")
        ax.set_zlabel("recommendation")
        ax.scatter(x, y, z)
        plt.show()
    draw_plot()
    return  regression



def recom_without_noidea(recom_ichi:pd.DataFrame ,start_time:str ):
    correct_data = recom_ichi.loc[(recom_ichi['date'] >= start_time)]
    del correct_data['date']
    correct_data = np.array(correct_data).astype(int)
    return correct_data

# class Indicators:
#     __data = None
#     __first_time = True
#     col = ['ITS_9_tenkensen' ,'IKS_26_kijunsen' ,'ISA_9_spanA' , 'ISB_26_spanB' , 'IKS_26_chiku' ,'kijunAndSpanBCross']
#     __ichirecom = pd.DataFrame(columns= col)
#     def __init__(self ,data:pd.DataFrame ):
#         self.__data = cast_to_float(data)
#
#     def get_indicators_names(self):
#         return self.__data.ta.indicators()
#     def set_data(self ,data:pd.DataFrame):
#         self.__data = cast_to_float(data)

