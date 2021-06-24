import pandas as pd
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
    return {
        'ichimoku' : data.ta.ichimoku()[0],
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
    col = ['ITS_9_tenkensen', 'IKS_26_kijunsen', 'ISA_9_spanA', 'ISB_26_spanB', 'IKS_26_chiku',
           'kijunAndSpanBCross']
    #-1 no idea , 0 sell ,  1 buy
    recommend = pd.DataFrame(columns=col)
    recommend['ITS_9_tenkensen'] = np.where(ichimoku['ITS_9'] == 0, -1, np.where(ichimoku['ITS_9'] < price_data['close'], 1, 0))
    recommend['IKS_26_kijunsen'] = np.where(ichimoku['IKS_26'] == 0, -1, np.where(ichimoku['IKS_26'] < price_data['close'], 1, 0))
    recommend['ISA_9_spanA'] = np.where(ichimoku['ISA_9'] == 0, -1, np.where(ichimoku['ISA_9'] < price_data['close'], 1, 0))
    recommend['ISB_26_spanB'] = np.where(ichimoku['ISB_26'] == 0, -1, np.where(ichimoku['ISB_26'] < price_data['close'], 1, 0))
    recommend['IKS_26_chiku'] = np.where(ichimoku['IKS_26'] == 0, -1, np.where(ichimoku['IKS_26'] > price_data['close'], 1, 0))
    recommend['kijunAndSpanBCross'] = np.where(ichimoku['ISB_26'] == 0 , -1 ,np.where(ichimoku['IKS_26'] == ichimoku['ISB_26'] ,-1 , np.where(ichimoku['IKS_26'] > ichimoku['ISB_26'] ,1 , 0)))

    return recommend


class Indicators:
    __data = None
    __first_time = True
    col = ['ITS_9_tenkensen' ,'IKS_26_kijunsen' ,'ISA_9_spanA' , 'ISB_26_spanB' , 'IKS_26_chiku' ,'kijunAndSpanBCross']
    __ichirecom = pd.DataFrame(columns= col)
    def __init__(self ,data:pd.DataFrame ):
        self.__data = cast_to_float(data)

    def get_indicators_names(self):
        return self.__data.ta.indicators()
    def set_data(self ,data:pd.DataFrame):
        self.__data = cast_to_float(data)

