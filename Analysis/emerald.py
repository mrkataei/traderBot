"""
Mr.Kataei 11/12/2021
    this is all candle stick patterns function that some function work with 2 candles or 3 or 4 or 5 that commented
    you need to handled it for your usage - in pattern class handled it in preprocess all candles we need shifted in
    new column and attach in dataframe and in check_patterns the candle in parameter is on row we get from dataframe.
    in check_patterns first mange row wit _get_ohcl and get us series of c_open c_high , c_close and c_low
    and start use candle  stick patterns function already define in Libraries.patterns.py  at end patterns_detector with
     apply
    function apply check_patterns for all rows
    
"""
from Libraries.patterns import *
from Interfaces.strategy import Strategy


def _get_ohcl(candles):
    c_open = candles[['open', 'open1', 'open2', 'open3', 'open4']].to_numpy()
    c_high = candles[['high', 'high1', 'high2', 'high3', 'high4']].to_numpy()
    c_close = candles[['close', 'close1', 'close2', 'close3', 'close4']].to_numpy()
    c_low = candles[['low', 'low1', 'low2', 'low3', 'low4']].to_numpy()

    return c_open, c_high, c_close, c_low


class Emerald(Strategy):
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

    def __init__(self, data, coin_id: int, timeframe_id: int, bot_ins, analysis_id: int = 1):
        Strategy.__init__(self, data=data, coin_id=coin_id, analysis_id=analysis_id,
                          timeframe_id=timeframe_id, bot_ins=bot_ins)
        self.preprocess()

    def preprocess(self):
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

    def logic(self, row):
        # get array from get_ohcl function for open high close and low
        # --> c_open = [ 200.36 , 254.52 , 253.125, 5654.25 , 23265.366]
        pattern = ''
        c_open, c_high, c_close, c_low = _get_ohcl(row)
        # 2 candles patterns
        if hammer(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'hammer'] = True
            pattern = 'hammer'

        if hanging_man(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'hanging_man'] = True
            pattern = 'hanging_man'

        if shooting_star(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[row.name, 'shooting_star'] = True
            pattern = 'shooting_star'

        if harami_cross_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'harami_cross_bullish'] = True
            pattern = 'harami_cross_bullish'

        if harami_cross_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'harami_cross_bearish'] = True
            pattern = 'harami_cross_bearish'

        if doji_star_bullish(c_open=c_open, c_high=c_high, c_close=c_close, limit=0):
            self.data.loc[row.name, 'doji_star_bullish'] = True
            pattern = 'doji_star_bullish'

        if doji_star_bearish(c_open=c_open, c_close=c_close):
            self.data.loc[row.name, 'doji_star_bearish'] = True
            pattern = 'doji_star_bearish'

        if matching_low(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[row.name, 'matching_low'] = True
            pattern = 'matching_low'

        if matching_high(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'matching_high'] = True
            pattern = 'matching_high'

        if homing_pigeon(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'homing_pigeon'] = True
            pattern = 'homing_pigeon'

        if separating_lines_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0):
            self.data.loc[row.name, 'separating_lines_bullish'] = True
            pattern = 'separating_lines_bullish'

        if separating_lines_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0):
            self.data.loc[row.name, 'separating_lines_bearish'] = True
            pattern = 'separating_lines_bearish'

        if on_neck_line_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0):
            self.data.loc[row.name, 'on_neck_line_bullish'] = True
            pattern = 'on_neck_line_bullish'

        if on_neck_line_bearish(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'on_neck_line_bearish'] = True
            pattern = 'on_neck_line_bearish'

        if in_neck_line_bullish(c_open=c_open, c_close=c_close):
            self.data.loc[row.name, 'in_neck_line_bullish'] = True
            pattern = 'in_neck_line_bullish'

        if in_neck_line_bearish(c_open=c_open, c_close=c_close):
            self.data.loc[row.name, 'in_neck_line_bearish'] = True
            pattern = 'in_neck_line_bearish'

        if belt_hold_bullish(c_open=c_open, c_close=c_close, c_low=c_low, tolerance=0):
            self.data.loc[row.name, 'belt_hold_bullish'] = True
            pattern = 'belt_hold_bullish'

        if belt_hold_bearish(c_open=c_open, c_high=c_high, c_close=c_close, tolerance=0):
            self.data.loc[row.name, 'belt_hold_bearish'] = True
            pattern = 'belt_hold_bearish'

        if kicking_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0):
            self.data.loc[row.name, 'kicking_bullish'] = True
            pattern = 'kicking_bullish'

        if kicking_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0):
            self.data.loc[row.name, 'kicking_bearish'] = True
            pattern = 'kicking_bearish'

        # 3 candles patterns

        if inverted_hammer(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'inverted_hammer'] = True
            pattern = 'inverted_hammer'

        if morning_star(c_open=c_open, c_close=c_close):
            self.data.loc[row.name, 'morning_doji_star'] = True
            pattern = 'morning_doji_star'

        if evening_doji_star(c_open=c_open, c_high=c_high, c_close=c_close, limit=0):
            self.data.loc[row.name, 'evening_doji_star'] = True
            pattern = 'evening_doji_star'

        if abandoned_baby_bullish(c_open=c_open, c_high=c_high, c_close=c_close, limit=0):
            self.data.loc[row.name, 'abandoned_baby_bullish'] = True
            pattern = 'abandoned_baby_bullish'

        if abandoned_baby_bearish(c_open=c_open, c_high=c_high, c_close=c_close, limit=0):
            self.data.loc[row.name, 'abandoned_baby_bearish'] = True
            pattern = 'abandoned_baby_bearish'

        if tri_star_bullish(c_open=c_open, c_close=c_close, limit=0):
            self.data.loc[row.name, 'tri_star_bullish'] = True
            pattern = 'tri_star_bullish'

        if tri_star_bearish(c_open=c_open, c_close=c_close, limit=0):
            self.data.loc[row.name, 'tri_star_bearish'] = True
            pattern = 'tri_star_bearish'

        if three_inside_up(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'three_inside_up'] = True
            pattern = 'three_inside_up'

        if three_inside_down(c_open=c_open, c_close=c_close):
            self.data.loc[row.name, 'three_inside_down'] = True
            pattern = 'three_inside_down'

        if three_outside_up(c_open=c_open, c_close=c_close):
            self.data.loc[row.name, 'three_outside_up'] = True
            pattern = 'three_outside_up'

        if three_outside_down(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[row.name, 'three_outside_down'] = True
            pattern = 'three_outside_down'

        if unique_three_river(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'unique_three_river'] = True
            pattern = 'unique_three_river'

        if loentical_three_cross(c_open=c_open, c_close=c_close):
            self.data.loc[row.name, 'loentical_three_cross'] = True
            pattern = 'loentical_three_cross'

        if deliberation(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'deliberation'] = True
            pattern = 'deliberation'

        if upside_gap_two_crows(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[row.name, 'upside_gap_two_crows'] = True
            pattern = 'upside_gap_two_crows'

        if advance_block(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'advance_block'] = True
            pattern = 'advance_block'

        if two_crows(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'two_cows'] = True
            pattern = 'two_cows'

        if upside_tasuki_gap(c_open=c_open, c_close=c_close):
            self.data.loc[row.name, 'upside_tasuki_gap'] = True
            pattern = 'upside_tasuki_gap'

        if downside_tasuki_gap(c_open=c_open, c_close=c_close):
            self.data.loc[row.name, 'downside_tasuki_gap'] = True
            pattern = 'downside_tasuki_gap'

        if sidebyside_white_lines_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'sidebyside_white_lines_bullish'] = True
            pattern = 'sidebyside_white_lines_bullish'

        if sidebyside_white_lines_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'sidebyside_white_lines_bearish'] = True
            pattern = 'sidebyside_white_lines_bearish'

        if upside_gap_three_methods(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'upside_gap_three_methods'] = True
            pattern = 'upside_gap_three_methods'

        if downside_gap_three_methods(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'downside_gap_three_methods'] = True
            pattern = 'downside_gap_three_methods'

        if engulfing_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'engulfing_bullish'] = True
            pattern = 'engulfing_bullish'

        if engulfing_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'engulfing_bearish'] = True
            pattern = 'engulfing_bearish'

        if harami_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'harami_bullish'] = True
            pattern = 'harami_bullish'

        if harami_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'harami_bearish'] = True
            pattern = 'harami_bearish'

        if piercing_line(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'piercing_line'] = True
            pattern = 'piercing_line'

        if dark_cloud_cover(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[row.name, 'dark_cloud_cover'] = True
            pattern = 'dark_cloud_cover'

        if stick_sandwich(c_open=c_open, c_close=c_close, tolerance=0):
            self.data.loc[row.name, 'stick_sandwich'] = True
            pattern = 'stick_sandwich'

        if meeting_line_bullish(c_open=c_open, c_high=c_high, c_close=c_close, tolerance=0):
            self.data.loc[row.name, 'meeting_line_bullish'] = True
            pattern = 'meeting_line_bullish'

        if meeting_line_bearish(c_open=c_open, c_close=c_close, c_low=c_low, tolerance=0):
            self.data.loc[row.name, 'meeting_line_bearish'] = True
            pattern = 'meeting_line_bearish'

        # 4 candles patterns

        if concealing_baby(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[row.name, 'concealing_baby'] = True
            pattern = 'concealing_baby'

        if rising_three_methods(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'rising_three_methods'] = True
            pattern = 'rising_three_methods'

        if three_line_strike_bullish(c_open=c_open, c_high=c_high, c_close=c_close, tolerance=0):
            self.data.loc[row.name, 'three_line_strike_bullish'] = True
            pattern = 'three_line_strike_bullish'

        if three_line_strike_bearish(c_open=c_open, c_high=c_high, c_close=c_close, tolerance=0):
            self.data.loc[row.name, 'three_line_strike_bearish'] = True
            pattern = 'three_line_strike_bearish'

        if three_white_soldiers(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[row.name, 'three_white_soldiers'] = True
            pattern = 'three_white_soldiers'

        if three_black_crows(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'three_black_crows'] = True
            pattern = 'three_black_crows'

        if morning_star(c_open=c_open, c_close=c_close):
            self.data.loc[row.name, 'morning_star'] = True
            pattern = 'morning_star'

        if evening_star(c_open=c_open, c_close=c_close):
            self.data.loc[row.name, 'evening_star'] = True
            pattern = 'evening_star'

        if three_stars_in_the_south(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0):
            self.data.loc[row.name, 'three_stars_in_the_south'] = True
            pattern = 'three_stars_in_the_south'

        # 5 candles patterns

        if falling_three_methods(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'falling_three_methods'] = True
            pattern = 'falling_three_methods'

        if breakaway_bullish(c_open=c_open, c_close=c_close):
            self.data.loc[row.name, 'breakaway_bullish'] = True
            pattern = 'breakaway_bullish'

        if breakaway_bearish(c_open=c_open, c_close=c_close):
            self.data.loc[row.name, 'breakaway_bearish'] = True
            pattern = 'breakaway_bearish'

        if ladder_bottom(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[row.name, 'ladder_bottom'] = True
            pattern = 'ladder_bottom'

        if pattern in self.__bullish_patterns:
            self._set_recommendation(position='buy', risk='low', index=row.name)
        elif pattern in self.__bearish_patterns:
            self._set_recommendation(position='sell', risk='low', index=row.name)

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

    def get_all_patterns(self):
        self.signal_detector()
        self._clean_dataframe()
        return self.data
