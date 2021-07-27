import pandas as pd
import pandas_ta as ta
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
        #tenkan=10, kijun=30 , senkou=60
        'ichimoku' : data.ta.ichimoku()[0],
        #fast=12, slow=26, signal=9
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
    #ISA->SpanA->col0 , ISB-> SpanB -> col1 , ITS->tenkensen->col2 , IKS->kijunsen->col3 , ICS_26->chiku->col4
    SpanA = ichimoku.columns[0]
    SpanB = ichimoku.columns[1]
    tenkensen = ichimoku.columns[2]
    kijunsen = ichimoku.columns[3]
    chiku = ichimoku.columns[4]

    #-1 no idea , 0 sell ,  1 buy
    recommend = pd.DataFrame()
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
    element_numbers = len(indicator_recommendations.columns) - 1
    regression =  pd.DataFrame()
    regression[regression==1].sum(axis=1)
    regression['date'] = indicator_recommendations['date']
    regression['buy'] = indicator_recommendations.sum(axis=1)
    regression['sell'] = - (element_numbers - regression['buy'])
    regression['sum'] = regression['buy'] + regression['sell']
    regression['change'] = symbol_data['close'].pct_change()
    regression.change = regression.change.shift(-1)

    def draw_plot(point:True=True , x:str='date' , y:str='sum' ):
        reg = regression.tail(300)
        if not point:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=reg[x], y=reg[y]),
                          row=1, col=1 )
        else:
            fig = go.Figure(data=[go.Scatter(x=reg[x], y=reg[y] ,
                                             mode='markers',
                                             marker=dict(
                                                 color=regression['change'],
                                                 colorscale='Viridis',
                                                 showscale=True
                                             ))])
        fig.show()
    draw_plot(point=True )
    return  regression



def recom_without_noidea(recom_ichi:pd.DataFrame ,start_time:str ):
    correct_data = recom_ichi.loc[(recom_ichi['date'] >= start_time)]
    del correct_data['date']
    correct_data = np.array(correct_data).astype(int)
    return correct_data
#mojtaba

