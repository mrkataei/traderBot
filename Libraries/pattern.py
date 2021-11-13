""""
Mr.Kataei 11/12/2021
this is all candle stick patterns function that some function work with 2 candles or 3 or 4 or 5 that commented
you need to handled it for your usage - in pattern class handled it in preprocess all candles we need shifted in
new column and attach in dataframe and in check_patterns the candle in parameter is on row we get from dataframe.
in check_patterns first mange row wit _get_ohcl and get us series of c_open c_high , c_close and c_low
and start use candle  stick patterns function already define in pattern.py  at end patterns_detector with apply
function apply check_patterns for all rows

you can use last_limit_data for handle 2 , 3 , 4 and 5 candle problem

"""
import pandas as pd
from Libraries.patterns import *


def last_limit_data(candles, limit: int):
    candles = candles.tail(limit).reset_index()
    c_high = candles['high']
    c_low = candles['low']
    c_close = candles['close']
    c_open = candles['open']
    return c_open, c_high, c_close, c_low


def _get_ohcl(candles):
    c_open = candles[['open', 'open1', 'open2', 'open3', 'open4']].to_numpy()
    c_high = candles[['high', 'high1', 'high2', 'high3', 'high4']].to_numpy()
    c_close = candles[['close', 'close1', 'close2', 'close3', 'close4']].to_numpy()
    c_low = candles[['low', 'low1', 'low2', 'low3', 'low4']].to_numpy()

    return c_open, c_high, c_close, c_low


class Patterns:

    __bullish_patterns = ['hammer', 'inverted_hammer', 'belt_hold_bullish', 'engulfing_bullish', 'harami_bullish',
                          'harami_cross_bullish', 'piercing_line', 'doji_star_bullish', 'meeting_line_bullish',
                          'three_white_soldiers', 'morning_star', 'morning_doji_star', 'abandoned_baby_bullish',
                          'tri_star_bullish', 'breakaway_bullish', 'three_inside_up', 'three_outside_up',
                          'kicking_bullish',
                          'three_stars_in_the_south', 'concealing_baby', 'stick_sandwich', 'matching_low',
                          'homing_pigeon',
                          'ladder_bottom', 'separating_lines_bullish', 'rising_three_methods', 'upside_tasuki_gap',
                          'sidebyside_white_lines_bullish', 'three_line_strike_bullish', 'upside_gap_three_methods',
                          'on_neck_line_bullish', 'in_neck_line_bullish'
                          ]
    __bearish_patterns = ['hanging_man', 'shooting_star', 'belt_hold_bearish', 'engulfing_bearish', 'harami_bearish',
                          'harami_cross_bearish', 'dark_cloud_cover', 'doji_star_bearish', 'meeting_line_bearish',
                          'three_black_crows', 'evening_star', 'evening_doji_star', 'abandoned_baby_bearish',
                          'tri_star_bearish', 'three_inside_down', 'three_outside_down', 'kicking_bearish',
                          'loentical_three_cross', 'deliberation', 'matching_high', 'upside_gap_two_crows',
                          'advance_block',
                          'two_crows', 'separating_lines_bearish', 'falling_three_methods', 'downside_tasuki_gap',
                          'sidebyside_white_lines_bearish', 'three_line_strike_bearish', 'downside_gap_three_methods',
                          'on_neck_line_bearish', 'in_neck_line_bearish', 'breakaway_bearish'
                          ]

    def __init__(self, dataframe: pd.DataFrame):
        self.data = dataframe
        self.preprocess_candles()

    def preprocess_candles(self):
        self.data['open1'] = self.data['open'].shift(-1, axis=0)
        self.data['open2'] = self.data['open'].shift(-2, axis=0)
        self.data['open3'] = self.data['open'].shift(-3, axis=0)
        self.data['open4'] = self.data['open'].shift(-4, axis=0)
        self.data['high1'] = self.data['high'].shift(-1, axis=0)
        self.data['high2'] = self.data['high'].shift(-2, axis=0)
        self.data['high3'] = self.data['high'].shift(-3, axis=0)
        self.data['high4'] = self.data['high'].shift(-4, axis=0)
        self.data['close1'] = self.data['close'].shift(-1, axis=0)
        self.data['close2'] = self.data['close'].shift(-2, axis=0)
        self.data['close3'] = self.data['close'].shift(-3, axis=0)
        self.data['close4'] = self.data['close'].shift(-4, axis=0)
        self.data['low1'] = self.data['low'].shift(-1, axis=0)
        self.data['low2'] = self.data['low'].shift(-2, axis=0)
        self.data['low3'] = self.data['low'].shift(-3, axis=0)
        self.data['low4'] = self.data['low'].shift(-4, axis=0)

    def _set_recommendation(self, pattern_name: str, index):
        if pattern_name in self.__bullish_patterns:
            self.data.loc[index, 'recommendation'] = 'buy'
        elif pattern_name in self.__bearish_patterns:
            self.data.loc[index, 'recommendation'] = 'sell'

    def check_patterns(self, candles, recom: bool = False):

        # get array from get_ohcl function for open high close and low
        # --> c_open = [ 200.36 , 254.52 , 253.125, 5654.25 , 23265.366]

        c_open, c_high, c_close, c_low = _get_ohcl(candles)
        # 2 candles patterns
        if hammer(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'hammer'] = True
            if recom:
                self._set_recommendation(pattern_name='hammer', index=candles.name)

        if hanging_man(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'hanging_man'] = True
            if recom:
                self._set_recommendation(pattern_name='hanging_man', index=candles.name)

        if shooting_star(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[candles.name, 'shooting_star'] = True
            if recom:
                self._set_recommendation(pattern_name='shooting_star', index=candles.name)

        if harami_cross_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'harami_cross_bullish'] = True
            if recom:
                self._set_recommendation(pattern_name='harami_cross_bullish', index=candles.name)

        if harami_cross_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'harami_cross_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='harami_cross_bearish', index=candles.name)

        if doji_star_bullish(c_open=c_open, c_high=c_high, c_close=c_close, limit=20):
            self.data.loc[candles.name, 'doji_star_bullish'] = True
            if recom:
                self._set_recommendation(pattern_name='doji_star_bullish', index=candles.name)

        if doji_star_bearish(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'doji_star_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='doji_star_bearish', index=candles.name)

        if matching_low(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[candles.name, 'matching_low'] = True
            if recom:
                self._set_recommendation(pattern_name='matching_low', index=candles.name)

        if matching_high(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'matching_high'] = True
            if recom:
                self._set_recommendation(pattern_name='matching_high', index=candles.name)

        if homing_pigeon(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'homing_pigeon'] = True
            if recom:
                self._set_recommendation(pattern_name='homing_pigeon', index=candles.name)

        if separating_lines_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'separating_lines_bullish'] = True
            if recom:
                self._set_recommendation(pattern_name='separating_lines_bullish', index=candles.name)
        if separating_lines_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'separating_lines_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='separating_lines_bearish', index=candles.name)

        if on_neck_line_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'on_neck_line_bullish'] = True
            if recom:
                self._set_recommendation(pattern_name='on_neck_line_bullish', index=candles.name)

        if on_neck_line_bearish(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'on_neck_line_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='on_neck_line_bearish', index=candles.name)

        if in_neck_line_bullish(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'in_neck_line_bullish'] = True
            if recom:
                self._set_recommendation(pattern_name='in_neck_line_bullish', index=candles.name)

        if in_neck_line_bearish(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'in_neck_line_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='in_neck_line_bearish', index=candles.name)

        if belt_hold_bullish(c_open=c_open, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'belt_hold_bullish'] = True
            if recom:
                self._set_recommendation(pattern_name='belt_hold_bullish', index=candles.name)

        if belt_hold_bearish(c_open=c_open, c_high=c_high, c_close=c_close, tolerance=0.005):
            self.data.loc[candles.name, 'belt_hold_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='belt_hold_bearish', index=candles.name)

        if kicking_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'kicking_bullish'] = True
            if recom:
                self._set_recommendation(pattern_name='kicking_bullish', index=candles.name)

        if kicking_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'kicking_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='kicking_bearish', index=candles.name)

        # 3 candles patterns

        if inverted_hammer(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'inverted_hammer'] = True
            if recom:
                self._set_recommendation(pattern_name='inverted_hammer', index=candles.name)

        if morning_star(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'morning_doji_star'] = True
            if recom:
                self._set_recommendation(pattern_name='morning_doji_star', index=candles.name)

        if evening_doji_star(c_open=c_open, c_high=c_high, c_close=c_close, limit=20):
            self.data.loc[candles.name, 'evening_doji_star'] = True
            if recom:
                self._set_recommendation(pattern_name='evening_doji_star', index=candles.name)

        if abandoned_baby_bullish(c_open=c_open, c_high=c_high, c_close=c_close, limit=20):
            self.data.loc[candles.name, 'abandoned_baby_bullish'] = True
            if recom:
                self._set_recommendation(pattern_name='abandoned_baby_bullish', index=candles.name)

        if abandoned_baby_bearish(c_open=c_open, c_high=c_high, c_close=c_close, limit=20):
            self.data.loc[candles.name, 'abandoned_baby_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='abandoned_baby_bearish', index=candles.name)

        if tri_star_bullish(c_open=c_open, c_close=c_close, limit=20):
            self.data.loc[candles.name, 'tri_star_bullish'] = True
            if recom:
                self._set_recommendation(pattern_name='tri_star_bullish', index=candles.name)

        if tri_star_bearish(c_open=c_open, c_close=c_close, limit=20):
            self.data.loc[candles.name, 'tri_star_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='tri_star_bearish', index=candles.name)

        if three_inside_up(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'three_inside_up'] = True
            if recom:
                self._set_recommendation(pattern_name='three_inside_up', index=candles.name)

        if three_inside_down(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'three_inside_down'] = True
            if recom:
                self._set_recommendation(pattern_name='three_inside_down', index=candles.name)

        if three_outside_up(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'three_outside_up'] = True
            if recom:
                self._set_recommendation(pattern_name='three_outside_up', index=candles.name)

        if three_outside_down(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[candles.name, 'three_outside_down'] = True
            if recom:
                self._set_recommendation(pattern_name='three_outside_down', index=candles.name)

        if unique_three_river(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'unique_three_river'] = True
            if recom:
                self._set_recommendation(pattern_name='unique_three_river', index=candles.name)

        if loentical_three_cross(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'loentical_three_cross'] = True
            if recom:
                self._set_recommendation(pattern_name='loentical_three_cross', index=candles.name)

        if deliberation(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'deliberation'] = True
            if recom:
                self._set_recommendation(pattern_name='deliberation', index=candles.name)

        if upside_gap_two_crows(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[candles.name, 'upside_gap_two_crows'] = True
            if recom:
                self._set_recommendation(pattern_name='upside_gap_two_crows', index=candles.name)

        if advance_block(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'advance_block'] = True
            if recom:
                self._set_recommendation(pattern_name='advance_block', index=candles.name)

        if two_crows(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'two_cows'] = True
            if recom:
                self._set_recommendation(pattern_name='two_cows', index=candles.name)

        if upside_tasuki_gap(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'upside_tasuki_gap'] = True
            if recom:
                self._set_recommendation(pattern_name='upside_tasuki_gap', index=candles.name)

        if downside_tasuki_gap(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'downside_tasuki_gap'] = True
            if recom:
                self._set_recommendation(pattern_name='downside_tasuki_gap', index=candles.name)

        if sidebyside_white_lines_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'sidebyside_white_lines_bullish'] = True
            if recom:
                self._set_recommendation(pattern_name='sidebyside_white_lines_bullish', index=candles.name)

        if sidebyside_white_lines_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'sidebyside_white_lines_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='sidebyside_white_lines_bearish', index=candles.name)

        if upside_gap_three_methods(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'upside_gap_three_methods'] = True
            if recom:
                self._set_recommendation(pattern_name='upside_gap_three_methods', index=candles.name)

        if downside_gap_three_methods(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'downside_gap_three_methods'] = True
            if recom:
                self._set_recommendation(pattern_name='downside_gap_three_methods', index=candles.name)

        if engulfing_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'engulfing_bullish'] = True
            self._set_recommendation(pattern_name='hammer', index=candles.name)

        if engulfing_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'engulfing_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='engulfing_bearish', index=candles.name)

        if harami_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'harami_bullish'] = True
            if recom:
                self._set_recommendation(pattern_name='harami_bullish', index=candles.name)

        if harami_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'harami_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='harami_bearish', index=candles.name)

        if piercing_line(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'piercing_line'] = True
            if recom:
                self._set_recommendation(pattern_name='piercing_line', index=candles.name)

        if dark_cloud_cover(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[candles.name, 'dark_cloud_cover'] = True
            if recom:
                self._set_recommendation(pattern_name='dark_cloud_cover', index=candles.name)

        if stick_sandwich(c_open=c_open, c_close=c_close, tolerance=0.005):
            self.data.loc[candles.name, 'stick_sandwich'] = True
            if recom:
                self._set_recommendation(pattern_name='stick_sandwich', index=candles.name)

        if meeting_line_bullish(c_open=c_open, c_high=c_high, c_close=c_close, tolerance=0.005):
            self.data.loc[candles.name, 'meeting_line_bullish'] = True
            if recom:
                self._set_recommendation(pattern_name='meeting_line_bullish', index=candles.name)

        if meeting_line_bearish(c_open=c_open, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'meeting_line_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='meeting_line_bearish', index=candles.name)

        # 4 candles patterns

        if concealing_baby(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[candles.name, 'concealing_baby'] = True
            if recom:
                self._set_recommendation(pattern_name='concealing_baby', index=candles.name)

        if rising_three_methods(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'rising_three_methods'] = True
            if recom:
                self._set_recommendation(pattern_name='rising_three_methods', index=candles.name)

        if three_line_strike_bullish(c_open=c_open, c_high=c_high, c_close=c_close, tolerance=0.005):
            self.data.loc[candles.name, 'three_line_strike_bullish'] = True
            if recom:
                self._set_recommendation(pattern_name='three_line_strike_bullish', index=candles.name)

        if three_line_strike_bearish(c_open=c_open, c_high=c_high, c_close=c_close, tolerance=0.005):
            self.data.loc[candles.name, 'three_line_strike_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='three_line_strike_bearish', index=candles.name)

        if three_white_soldiers(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[candles.name, 'three_white_soldiers'] = True
            if recom:
                self._set_recommendation(pattern_name='three_white_soldiers', index=candles.name)

        if three_black_crows(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'three_black_crows'] = True
            if recom:
                self._set_recommendation(pattern_name='three_black_crows', index=candles.name)

        if morning_star(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'morning_star'] = True
            if recom:
                self._set_recommendation(pattern_name='morning_star', index=candles.name)

        if evening_star(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'evening_star'] = True
            if recom:
                self._set_recommendation(pattern_name='evening_star', index=candles.name)

        if three_stars_in_the_south(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'three_stars_in_the_south'] = True
            if recom:
                self._set_recommendation(pattern_name='three_stars_in_the_south', index=candles.name)

        # 5 candles patterns

        if falling_three_methods(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'falling_three_methods'] = True
            if recom:
                self._set_recommendation(pattern_name='falling_three_methods', index=candles.name)

        if breakaway_bullish(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'breakaway_bullish'] = True
            if recom:
                self._set_recommendation(pattern_name='breakaway_bullish', index=candles.name)

        if breakaway_bearish(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'breakaway_bearish'] = True
            if recom:
                self._set_recommendation(pattern_name='breakaway_bearish', index=candles.name)

        if ladder_bottom(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'ladder_bottom'] = True
            if recom:
                self._set_recommendation(pattern_name='ladder_bottom', index=candles.name)

    def patterns_detector(self, recom: bool = False):
        self.data.apply(lambda row: self.check_patterns(candles=row, recom=recom), axis=1)
        self._clean_dataframe()
        return self.data

    def save_csv(self):
        self.data.to_csv('../Static/patterns_detector.csv')

    def _clean_dataframe(self):
        del self.data['open1']
        del self.data['open2']
        del self.data['open3']
        del self.data['open4']
        del self.data['close1']
        del self.data['close2']
        del self.data['close3']
        del self.data['close4']
        del self.data['high1']
        del self.data['high2']
        del self.data['high3']
        del self.data['high4']
        del self.data['low1']
        del self.data['low2']
        del self.data['low3']
        del self.data['low4']

    def get_recommendations(self):
        self.patterns_detector(recom=True)
        return self.data[['date', 'open', 'high', 'close', 'low', 'recommendation']].copy()
