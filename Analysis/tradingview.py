"""
Mr.Kataei 8/4/2021
tradingview api signals
"""
from tradingview_ta import TA_Handler, Interval


def get_time_interval(time):
    return {
        'day': Interval.INTERVAL_1_DAY,
        '1hour': Interval.INTERVAL_1_HOUR,
        '1month': Interval.INTERVAL_1_MONTH,
        '1week': Interval.INTERVAL_1_WEEK,
        '1min': Interval.INTERVAL_1_MINUTE,
        '4hour': Interval.INTERVAL_4_HOURS,
        '5min': Interval.INTERVAL_5_MINUTES,
        '15min': Interval.INTERVAL_15_MINUTES,
    }.get(time, Interval.INTERVAL_1_MINUTE)


class TradingView:
    __indicators = ['Recommend.Other', 'Recommend.All', 'Recommend.MA', 'RSI', 'RSI[1]', 'Stoch.K', 'Stoch.D',
                    'Stoch.K[1]', 'Stoch.D[1]', 'CCI20', 'CCI20[1]', 'ADX', 'ADX+DI', 'ADX-DI', 'ADX+DI[1]',
                    'ADX-DI[1]', 'AO', 'AO[1]', 'Mom', 'Mom[1]', 'MACD.macd', 'MACD.signal', 'Rec.Stoch.RSI',
                    'Stoch.RSI.K', 'Rec.WR', 'W.R', 'Rec.BBPower', 'BBPower', 'Rec.UO', 'UO', 'close', 'EMA5', 'SMA5',
                    'EMA10', 'SMA10', 'EMA20', 'SMA20', 'EMA30', 'SMA30', 'EMA50', 'SMA50', 'EMA100', 'SMA100',
                    'EMA200', 'SMA200', 'Rec.Ichimoku', 'Ichimoku.BLine', 'Rec.VWMA', 'VWMA', 'Rec.HullMA9', 'HullMA9',
                    'Pivot.M.Classic.S3', 'Pivot.M.Classic.S2', 'Pivot.M.Classic.S1', 'Pivot.M.Classic.Middle',
                    'Pivot.M.Classic.R1', 'Pivot.M.Classic.R2', 'Pivot.M.Classic.R3', 'Pivot.M.Fibonacci.S3',
                    'Pivot.M.Fibonacci.S2', 'Pivot.M.Fibonacci.S1', 'Pivot.M.Fibonacci.Middle', 'Pivot.M.Fibonacci.R1',
                    'Pivot.M.Fibonacci.R2', 'Pivot.M.Fibonacci.R3', 'Pivot.M.Camarilla.S3', 'Pivot.M.Camarilla.S2',
                    'Pivot.M.Camarilla.S1', 'Pivot.M.Camarilla.Middle', 'Pivot.M.Camarilla.R1', 'Pivot.M.Camarilla.R2',
                    'Pivot.M.Camarilla.R3', 'Pivot.M.Woodie.S3', 'Pivot.M.Woodie.S2', 'Pivot.M.Woodie.S1',
                    'Pivot.M.Woodie.Middle', 'Pivot.M.Woodie.R1', 'Pivot.M.Woodie.R2', 'Pivot.M.Woodie.R3',
                    'Pivot.M.Demark.S1', 'Pivot.M.Demark.Middle', 'Pivot.M.Demark.R1', 'open', 'P.SAR', 'BB.lower',
                    'BB.upper', 'AO[2]']
    __moving_averages = ['EMA10', 'SMA10', 'EMA20', 'SMA20', 'EMA30', 'SMA30', 'EMA50', 'SMA50', 'EMA100', 'SMA100',
                         'EMA200', 'SMA200', 'Ichimoku', 'VWMA', 'HullMA']
    __oscillators = ['RSI', 'STOCH.K', 'CCI', 'ADX', 'AO', 'Mom', 'MACD', 'Stoch.RSI', 'W%R', 'BBP', 'UO']

    def __init__(self, symbol, time_frame, screener, exchange):
        self.symbol = symbol
        self.screener = screener
        self.exchange = exchange
        self.interval = get_time_interval(time_frame)
        self.comp = TA_Handler(symbol=self.symbol, screener=self.screener, exchange=self.exchange,
                               interval=self.interval)

    def get_summary(self):
        print(self.comp.get_analysis().summary)

    def get_comp_obj(self):
        return self.comp.get_analysis()

    def get_indicators_names(self):
        for indi in self.__indicators:
            print(indi)

    def get_moving_average_names(self):
        for indi in self.__moving_averages:
            print(indi)

    def get_oscillators_names(self):
        for indi in self.__oscillators:
            print(indi)

    def get_indicators(self, indicator='all'):
        indi = self.comp.get_analysis().indicators
        if indicator == 'all':
            return indi
        else:
            return indi[str(indicator)]

    def get_moving_averages_rec(self, indicator='all'):
        indi = self.comp.get_analysis().moving_averages
        if indicator == 'all':
            return indi
        else:
            return indi['COMPUTE'][str(indicator)]

    def get_moving_averages_all_rec(self, recommendation='all'):
        indi = self.comp.get_analysis().moving_averages
        all = {'RECOMMENDATION': indi['RECOMMENDATION'], 'BUY': indi['BUY'], 'SELL': indi['SELL'],
               'NEUTRAL': indi['NEUTRAL']}
        return {
            'recommendation': indi['RECOMMENDATION'],
            'buy': indi['BUY'],
            'sell': indi['SELL'],
            'neutral': indi['NEUTRAL']
        }.get(recommendation, all)

    def get_oscillators_rec(self, indicator='all'):
        indi = self.comp.get_analysis().oscillators
        if indicator == 'all':
            return indi
        else:
            return indi['COMPUTE'][str(indicator)]

    def get_oscillators_all_rec(self, recommendation='all'):
        indi = self.get_oscillators_rec()
        all = {'RECOMMENDATION': indi['RECOMMENDATION'], 'BUY': indi['BUY'], 'SELL': indi['SELL'],
               'NEUTRAL': indi['NEUTRAL']}
        return {
            'recommendation': indi['RECOMMENDATION'],
            'buy': indi['BUY'],
            'sell': indi['SELL'],
            'neutral': indi['NEUTRAL']
        }.get(recommendation, all)
