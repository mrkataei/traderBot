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


def _average(*inputs: float):
    result = 0.0
    for put in inputs:
        result += put
    return result / len(inputs)


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
        self.data = self.data.dropna()

    def check_patterns(self, candles):

        # get array from get_ohcl function for open high close and low
        # --> c_open = [ 200.36 , 254.52 , 253.125, 5654.25 , 23265.366]

        c_open, c_high, c_close, c_low = _get_ohcl(candles)
        # 2 candles patterns

        if hammer(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'hammer'] = True
        if hanging_man(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'hanging_man'] = True
        if shooting_star(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[candles.name, 'shooting_star'] = True
        if harami_cross_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'harami_cross_bullish'] = True
        if harami_cross_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'harami_cross_bearish'] = True
        if doji_star_bullish(c_open=c_open, c_high=c_high, c_close=c_close, limit=20):
            self.data.loc[candles.name, 'doji_star_bullish'] = True
        if doji_star_bearish(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'doji_star_bearish'] = True
        if matching_low(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[candles.name, 'matching_low'] = True
        if matching_high(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'matching_high'] = True
        if homing_pigeon(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'homing_pigeon'] = True
        if separating_lines_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'separating_lines_bullish'] = True
        if separating_lines_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'separating_lines_bearish'] = True
        if on_neck_line_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'on_neck_line_bullish'] = True
        if on_neck_line_bearish(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'on_neck_line_bearish'] = True
        if in_neck_line_bullish(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'in_neck_line_bullish'] = True
        if in_neck_line_bearish(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'in_neck_line_bearish'] = True
        if belt_hold_bullish(c_open=c_open, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'belt_hold_bullish'] = True
        if belt_hold_bearish(c_open=c_open, c_high=c_high, c_close=c_close, tolerance=0.005):
            self.data.loc[candles.name, 'belt_hold_bearish'] = True
        if kicking_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'kicking_bullish'] = True
        if kicking_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'kicking_bearish'] = True

        # 3 candles patterns

        if inverted_hammer(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'inverted_hammer'] = True
        if morning_star(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'morning_doji_star'] = True
        if evening_doji_star(c_open=c_open, c_high=c_high, c_close=c_close, limit=20):
            self.data.loc[candles.name, 'evening_doji_star'] = True
        if abandoned_baby_bullish(c_open=c_open, c_high=c_high, c_close=c_close, limit=20):
            self.data.loc[candles.name, 'abandoned_baby_bullish'] = True
        if abandoned_baby_bearish(c_open=c_open, c_high=c_high, c_close=c_close, limit=20):
            self.data.loc[candles.name, 'abandoned_baby_bearish'] = True
        if tri_star_bullish(c_open=c_open, c_close=c_close, limit=20):
            self.data.loc[candles.name, 'tri_star_bullish'] = True
        if tri_star_bearish(c_open=c_open, c_close=c_close, limit=20):
            self.data.loc[candles.name, 'tri_star_bearish'] = True
        if three_inside_up(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'three_inside_up'] = True
        if three_inside_down(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'three_inside_down'] = True
        if three_outside_up(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'three_outside_up'] = True
        if three_outside_down(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[candles.name, 'three_outside_down'] = True
        if unique_three_river(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'unique_three_river'] = True
        if loentical_three_cross(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'loentical_three_cross'] = True
        if deliberation(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'deliberation'] = True
        if upside_gap_two_crows(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[candles.name, 'upside_gap_two_crows'] = True
        if advance_block(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'advance_block'] = True
        if two_crows(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'two_cows'] = True
        if upside_tasuki_gap(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'upside_tasuki_gap'] = True
        if downside_tasuki_gap(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'downside_tasuki_gap'] = True
        if sidebyside_white_lines_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'sidebyside_white_lines_bullish'] = True
        if sidebyside_white_lines_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'sidebyside_white_lines_bearish'] = True
        if upside_gap_three_methods(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'upside_gap_three_methods'] = True
        if downside_gap_three_methods(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'downside_gap_three_methods'] = True
        if engulfing_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'engulfing_bullish'] = True
        if engulfing_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'engulfing_bearish'] = True
        if harami_bullish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'harami_bullish'] = True
        if harami_bearish(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'harami_bearish'] = True
        if piercing_line(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'piercing_line'] = True
        if dark_cloud_cover(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[candles.name, 'dark_cloud_cover'] = True
        if stick_sandwich(c_open=c_open, c_close=c_close, tolerance=0.005):
            self.data.loc[candles.name, 'stick_sandwich'] = True
        if meeting_line_bullish(c_open=c_open, c_high=c_high, c_close=c_close, tolerance=0.005):
            self.data.loc[candles.name, 'meeting_line_bullish'] = True
        if meeting_line_bearish(c_open=c_open, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'meeting_line_bearish'] = True

        # 4 candles patterns

        if concealing_baby(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[candles.name, 'concealing_baby'] = True
        if rising_three_methods(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'rising_three_methods'] = True
        if three_line_strike_bullish(c_open=c_open, c_high=c_high, c_close=c_close, tolerance=0.005):
            self.data.loc[candles.name, 'three_line_strike_bullish'] = True
        if three_line_strike_bearish(c_open=c_open, c_high=c_high, c_close=c_close, tolerance=0.005):
            self.data.loc[candles.name, 'three_line_strike_bearish'] = True
        if three_white_soldiers(c_open=c_open, c_high=c_high, c_close=c_close):
            self.data.loc[candles.name, 'three_white_soldiers'] = True
        if three_black_crows(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'three_black_crows'] = True
        if morning_star(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'morning_star'] = True
        if evening_star(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'evening_star'] = True
        if three_stars_in_the_south(c_open=c_open, c_high=c_high, c_close=c_close, c_low=c_low, tolerance=0.005):
            self.data.loc[candles.name, 'three_stars_in_the_south'] = True

        # 5 candles patterns

        if falling_three_methods(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'falling_three_methods'] = True
        if breakaway_bullish(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'breakaway_bullish'] = True
        if breakaway_bearish(c_open=c_open, c_close=c_close):
            self.data.loc[candles.name, 'breakaway_bearish'] = True
        if ladder_bottom(c_open=c_open, c_close=c_close, c_low=c_low):
            self.data.loc[candles.name, 'ladder_bottom'] = True

    def patterns_detector(self):
        self.data.apply(lambda row: self.check_patterns(candles=row), axis=1)
        self.data.to_csv('test.csv')

    def save_csv(self):
        self.data.to_csv('test.csv')


# all candles stick patterns

# 2 candles needed
def hammer(c_open, c_high, c_close, c_low):
    # work with at least 2 candle and return True if pattern be true
    if c_low[0] > c_open[1] > c_close[1] > c_low[1] and c_high[1] < c_low[0]:
        return True
    else:
        return False


def hanging_man(c_open, c_high, c_close, c_low):
    # work with at least 2 candle and return True if pattern be true
    if c_open[1] > c_close[1] > c_high[0] > c_low[1]:
        return True
    else:
        return False


def shooting_star(c_open, c_high, c_close):
    # work with at least 2 candle and return True if pattern be true
    if c_high[1] > c_high[0] > _average(c_open[1], c_close[1]) and c_open[1] > c_close[1] > c_close[0] \
            and c_open[1] > c_high[0]:
        return True
    else:
        return False


def harami_cross_bullish(c_open, c_high, c_close, c_low):
    # work with at least 2 candle and return True if pattern be true
    if c_open[0] > c_close[0] and c_open[0] > c_high[1] and c_close[0] < c_low[1]:
        return True
    else:
        return False


def harami_cross_bearish(c_open, c_high, c_close, c_low):
    # work with at least 2 candle and return True if pattern be true
    if c_open[0] < c_close[0] and c_open[0] < c_low[1] and c_close[0] > c_high[1]:
        return True
    else:
        return False


def doji_star_bullish(c_open, c_high, c_close, limit: float):
    # work with at least 2 candle and return True if pattern be true
    if c_open[0] > c_close[0] and abs(c_open[1] - c_close[1]) < limit and c_high[1] >= c_close[0]:
        return True
    else:
        return False


def doji_star_bearish(c_open, c_close):
    # work with at least 2 candle and return True if pattern be true
    if c_open[0] < c_close[0] and c_open[1] > c_close[1] and c_close[1] <= c_close[0] < _average(c_open[1], c_close[1]):
        return True
    else:
        return False


def matching_low(c_open, c_high, c_close):
    # work with at least 2 candle and return True if pattern be true
    if c_close[1] <= c_close[0] < c_open[0] <= c_high[1] and c_close[1] < c_open[1] <= c_open[0]:
        return True
    else:
        return False


def matching_high(c_open, c_close, c_low):
    # work with at least 2 candle and return True if pattern be true
    if c_close[0] > c_open[0] >= c_low[1] and c_close[0] >= c_close[1] > c_open[1] > c_open[0]:
        return True
    else:
        return False


def separating_lines_bullish(c_open, c_high, c_close, c_low, tolerance: float):
    # work with at least 2 candle and return True if pattern be true
    first = abs(c_open[1] - c_close[1])
    sec = abs(c_open[0] - c_close[0])

    if abs(first - sec) < tolerance and c_open[0] > c_close[0] and c_high[0] > c_open[1] and c_open[1] < c_close[1] \
            and c_low[1] < c_open[0] < c_open[1]:
        return True
    else:
        return False


def separating_lines_bearish(c_open, c_high, c_close, c_low, tolerance: float):
    # work with at least 2 candle and return True if pattern be true
    first = abs(c_open[1] - c_close[1])
    sec = abs(c_open[0] - c_close[0])

    if abs(first - sec) < tolerance and c_open[0] < c_close[0] < c_open[1] <= c_open[0] < c_high[1] \
            and c_low[0] < c_open[1]:
        return True
    else:
        return False


def on_neck_line_bullish(c_open, c_high, c_close, c_low, tolerance: float):
    # work with at least 2 candle and return True if pattern be true
    if c_open[0] < c_close[0] < c_close[1] < c_open[1] and abs(c_low[1] - c_close[1]) < tolerance \
            and abs(c_open[0] - c_close[0]) > abs(c_open[1] - c_close[1]) and c_close[1] <= c_high[0]:
        return True
    else:
        return False


def on_neck_line_bearish(c_open, c_close, c_low):
    # work with at least 2 candle and return True if pattern be true
    if c_open[0] > c_close[0] > c_close[1] > c_open[1] and abs(c_open[0] - c_close[0]) > abs(c_open[1] - c_close[1]) \
            and c_close[1] <= c_low[0]:
        return True
    else:
        return False


def in_neck_line_bullish(c_open, c_close):
    # work with at least 2 candle and return True if pattern be true
    if c_open[0] < c_close[0] <= c_close[1] < c_open[1] and abs(c_open[0] - c_close[0]) > abs(c_open[1] - c_close[1]):
        return True
    else:
        return False


def in_neck_line_bearish(c_open, c_close):
    # work with at least 2 candle and return True if pattern be true
    if c_open[0] > c_close[0] >= c_close[1] > c_open[1] and abs(c_open[0] - c_close[0]) > abs(c_open[1] - c_close[1]):
        return True
    else:
        return False


def belt_hold_bullish(c_open, c_close, c_low, tolerance: float):
    # work with at least 2 candle and return True if pattern be true
    if c_open[0] > c_close[0] > c_open[1] and c_low[0] > c_open[1] and abs(c_open[1] - c_low[1]) < tolerance \
            and c_close[1] > _average(c_close[1], c_open[1]):
        return True
    else:
        return False


def belt_hold_bearish(c_open, c_high, c_close, tolerance: float):
    # work with at least 2 candle and return True if pattern be true
    if c_open[0] < c_close[0] < c_open[1] and c_high[0] < c_open[1] \
            and abs(c_open[1] - c_high[1]) < tolerance and c_close[1] < _average(c_close[1], c_open[1]):
        return True
    else:
        return False


def kicking_bullish(c_open, c_high, c_close, c_low, tolerance: float):
    # work with at least 2 candle and return True if pattern be true
    if c_open[0] > c_close[0] and abs(c_open[0] - c_high[0]) < tolerance and abs(c_close[0] - c_low[0]) < tolerance \
            and c_open[1] > c_open[0] and abs(c_open[1] - c_low[1]) < tolerance \
            and abs(c_close[1] - c_high[1]) < tolerance and c_close[1] - c_open[1] > c_open[0] - c_close[0]:
        return True
    else:
        return False


def kicking_bearish(c_open, c_high, c_close, c_low, tolerance: float):
    # work with at least 2 candle and return True if pattern be true
    if c_open[0] < c_close[0] and abs(c_open[0] - c_low[0]) < tolerance and abs(c_close[0] - c_high[0]) < tolerance \
            and c_open[1] < c_open[0] and abs(c_open[1] - c_high[1]) < tolerance \
            and abs(c_close[1] - c_low[1]) < tolerance and c_open[1] - c_close[1] > c_close[0] - c_open[0]:
        return True
    else:
        return False


def homing_pigeon(c_open, c_high, c_close, c_low):
    # work with at least 2 candle and return True if pattern be true
    if c_high[0] > c_open[0] >= c_high[1] > c_open[1] > c_close[1] > c_low[1] > c_close[0] > c_low[0]:
        return True
    else:
        return False


# 3 candles needed

def inverted_hammer(c_open, c_high, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if c_low[0] > c_high[1] > c_high[2] > c_close[1] > c_close[2] and c_open[2] < c_close[1] and c_high[2] < c_open[1]:
        return True
    else:
        return False


def morning_doji_star(c_open, c_close, c_low, limit: float):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] > c_close[0] and abs(c_open[1] - c_close[1]) < limit and c_close[1] < c_open[2] < c_close[2] \
            and c_low[2] >= c_close[1]:
        return True
    else:
        return False


def evening_doji_star(c_open, c_high, c_close, limit: float):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] < c_close[0] and abs(c_open[1] - c_close[1]) < limit and c_close[1] > c_open[2] > c_close[2] \
            and c_high[2] <= c_close[1]:
        return True
    else:
        return False


def abandoned_baby_bullish(c_open, c_high, c_close, limit: float):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] > c_close[0] >= c_high[1] and abs(c_open[1] - c_close[1]) < limit and c_open[2] < c_close[2] \
            and c_close[2] > c_close[0] and c_close[2] >= _average(c_open[0], c_close[0]) and c_open[2] > c_close[1]:
        return True
    else:
        return False


def abandoned_baby_bearish(c_open, c_high, c_close, limit: float):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] < c_close[0] < c_close[1] and abs(c_open[1] - c_close[1]) < limit \
            and c_close[1] > c_open[2] > c_close[2] and _average(c_open[0], c_close[0]) >= c_close[2] \
            and c_high[2] <= c_close[1]:
        return True
    else:
        return False


def tri_star_bullish(c_open, c_close, limit: float):
    # work with at least 3 candle and return True if pattern be true
    if c_close[1] < c_close[2] < c_close[0] and abs(c_open[2] - c_close[2]) < limit \
            and abs(c_open[1] - c_close[1]) < limit and abs(c_open[0] - c_close[0]) < limit:
        return True
    else:
        return False


def tri_star_bearish(c_open, c_close, limit: float):
    # work with at least 3 candle and return True if pattern be true
    if c_close[0] < c_close[2] < c_close[1] and abs(c_open[2] - c_close[2]) < limit \
            and abs(c_open[1] - c_close[1]) < limit and abs(c_open[0] - c_close[0]) < limit:
        return True
    else:
        return False


def three_inside_up(c_open, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] > c_close[0] and c_open[0] > c_close[1] > c_open[1] > c_close[0] \
            and c_open[1] < c_open[2] < c_close[1] and c_open[2] < c_close[2] and c_low[2] >= c_open[1] \
            and c_close[2] > c_open[0]:
        return True
    else:
        return False


def three_inside_down(c_open, c_close):
    # work with at least 3 candle and return True if pattern be true
    if c_close[0] > c_open[1] > c_close[1] > c_open[0] > c_close[2] \
            and _average(c_open[1], c_close[1]) > c_open[2] > c_close[2]:
        return True
    else:
        return False


def three_outside_up(c_open, c_close):
    # work with at least 3 candle and return True if pattern be true
    if c_open[1] < c_close[0] < c_open[0] < c_close[1] and c_open[2] < c_close[1] < c_close[2]:
        return True
    else:
        return False


def three_outside_down(c_open, c_high, c_close):
    # work with at least 3 candle and return True if pattern be true
    if c_open[1] > c_close[0] > c_open[0] > c_close[1] > c_close[2] and c_open[2] > c_close[1] \
            and c_high[2] < c_open[1]:
        return True
    else:
        return False


def unique_three_river(c_open, c_high, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] > c_open[1] > c_close[1] > c_close[0] and c_low[1] < c_low[0] \
            and c_close[0] <= c_open[2] < c_close[2] < c_close[1] < c_high[2]:
        return True
    else:
        return False


def loentical_three_cross(c_open, c_close):
    # work with at least 3 candle and return True if pattern be true
    if c_close[2] < c_open[2] <= c_close[1] < c_open[1] <= c_close[0] < c_open[0]:
        return True
    else:
        return False


def deliberation(c_open, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] < c_close[0] and c_open[1] < c_close[1] and c_open[2] < c_close[2] and c_open[1] <= c_close[0] \
            and abs(c_open[2] - c_close[2]) < abs(c_open[1] - c_close[1]) and c_open[2] > c_close[1] and c_low[2] >= \
            c_close[1]:
        return True
    else:
        return False


def upside_gap_two_crows(c_open, c_high, c_close):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] < c_close[0] and c_open[2] > c_open[1] > c_close[1] > c_close[2] >= c_high[0]:
        return True
    else:
        return False


def advance_block(c_open, c_high, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if abs(c_open[2] - c_close[2]) < abs(c_open[1] - c_close[1]) < abs(c_open[0] - c_close[0]) \
            and c_open[0] < c_close[0] and c_open[1] < c_close[1] and c_open[2] < c_close[2] \
            and c_open[1] < c_close[0] and c_open[2] < c_close[1] and c_high[1] > c_close[2] \
            and c_low[2] < _average(c_open[1], c_close[1]):
        return True
    else:
        return False


def two_crows(c_open, c_high, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if abs(c_open[0] - c_close[0]) > abs(c_open[1] - c_close[1]) \
            and abs(c_open[2] - c_close[2]) > abs(c_open[1] - c_close[1]) and c_open[0] < c_close[0] \
            and c_high[0] <= c_low[1] and c_open[1] > c_close[1] \
            and c_close[1] < c_open[2] <= _average(c_open[1], c_close[1]) and c_open[2] > c_close[2] \
            and c_low[2] < _average(c_open[0], c_close[0]):
        return True
    else:
        return False


def upside_tasuki_gap(c_open, c_close):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] < c_close[0] < c_close[2] < c_open[1] < c_open[2] < c_close[1]:
        return True
    else:
        return False


def downside_tasuki_gap(c_open, c_close):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] > c_close[0] > c_close[2] > c_open[1] > c_open[2] > c_close[1]:
        return True
    else:
        return False


def sidebyside_white_lines_bullish(c_open, c_high, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] < c_close[0] < c_open[2] < c_open[1] < c_close[2] < c_close[1] <= c_high[2] and c_low[1] > c_high[0]:
        return True
    else:
        return False


def sidebyside_white_lines_bearish(c_open, c_high, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] > c_close[0] > c_close[1] >= c_close[2] > c_open[2] >= c_open[1] and c_high[1] <= c_low[0]:
        return True
    else:
        return False


def upside_gap_three_methods(c_open, c_high, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] < c_close[2] < c_close[0] < c_open[1] < c_open[2] < c_close[1] and c_low[1] > c_high[0]:
        return True
    else:
        return False


def downside_gap_three_methods(c_open, c_high, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] > c_close[2] > c_close[0] > c_open[1] > c_open[2] > c_close[1] and c_high[1] < c_low[0]:
        return True
    else:
        return False


def engulfing_bullish(c_open, c_high, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if c_high[2] > c_high[1] and c_low[2] < c_low[1] and c_open[2] < c_open[1] and c_close[2] > c_close[1] \
            and c_close[2] > c_open[2] and c_close[1] < c_close[0] and c_close[2] > c_open[1]:
        return True
    else:
        return False


def engulfing_bearish(c_open, c_high, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if c_high[2] > c_high[1] and c_low[2] < c_low[1] and c_open[2] > c_open[1] and c_close[2] < c_close[1] \
            and c_close[2] < c_open[2] and c_close[1] > c_close[0] and c_close[2] < c_open[1]:
        return True
    else:
        return False


def harami_bullish(c_open, c_high, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if c_open[1] > c_close[1] and c_close[1] < c_close[0] and c_close[1] < c_open[2] < c_open[1] \
            and c_close[1] < c_close[2] < c_open[1] and c_high[2] < c_high[1] and c_low[2] > c_low[1] \
            and c_close[2] >= c_open[2]:
        return True
    else:
        return False


def harami_bearish(c_open, c_high, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if c_open[1] < c_close[1] and c_close[1] > c_close[0] and c_close[1] > c_open[2] > c_open[1] \
            and c_close[1] > c_close[2] > c_open[1] and c_high[2] < c_high[1] and c_low[2] > c_low[1] \
            and c_close[2] <= c_open[2]:
        return True
    else:
        return False


def piercing_line(c_open, c_close, c_low):
    # work with at least 3 candle and return True if pattern be true
    if c_close[0] > c_close[1] and c_open[2] < c_low[1] and _average(c_open[1], c_close[1]) < c_close[2] < c_open[1]:
        return True
    else:
        return False


def dark_cloud_cover(c_open, c_high, c_close):
    # work with at least 3 candle and return True if pattern be true
    if c_close[0] < c_close[1] and c_open[2] > c_high[1] and _average(c_open[1], c_close[1]) > c_close[2] > c_open[1]:
        return True
    else:
        return False


def stick_sandwich(c_open, c_close, tolerance: float):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] > c_close[0] and c_close[0] < c_open[1] < c_close[1] < c_open[2] and c_open[2] > c_close[2] \
            and abs(c_close[2] - c_close[0]) < tolerance:
        return True
    else:
        return False


def meeting_line_bullish(c_open, c_high, c_close, tolerance: float):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] > c_close[0] and c_open[1] > c_close[1] and abs(c_close[1] - c_close[2]) < tolerance \
            and c_open[2] < c_close[2] and c_open[1] >= c_high[2]:
        return True
    else:
        return False


def meeting_line_bearish(c_open, c_close, c_low, tolerance: float):
    # work with at least 3 candle and return True if pattern be true
    if c_open[0] < c_close[0] and c_open[1] < c_close[1] and abs(c_close[1] - c_close[2]) < tolerance \
            and c_open[2] > c_close[2] and c_open[1] <= c_low[2]:
        return True
    else:
        return False


# 4 candles needed
def concealing_baby(c_open, c_high, c_close):
    # work with at least 4 candle and return True if pattern be true
    if c_open[0] > c_close[0] and c_open[1] > c_close[0] and c_open[1] > c_close[1] and c_high[2] > c_close[1] \
            and c_close[1] > c_open[2] > c_close[2] and c_open[3] >= c_high[2] and c_close[3] <= c_close[2]:
        return True
    else:
        return False


def rising_three_methods(c_open, c_high, c_close, c_low):
    # work with at least 4 candle and return True if pattern be true
    if c_low[3] >= c_low[0] and c_open[0] <= c_close[3] < c_open[3] < c_close[2] < c_open[2] <= c_close[1] \
            < c_close[1] < c_open[1] and c_high[3] > c_close[2]:
        return True
    else:
        return False


def three_line_strike_bullish(c_open, c_high, c_close, tolerance: float):
    # work with at least 4 candle and return True if pattern be true
    first = abs(c_open[2] - c_close[2])
    sec = abs(c_open[1] - c_close[1])
    third = abs(c_open[0] - c_close[0])

    if c_close[3] < c_open[0] < c_open[1] < c_close[0] <= c_open[2] < c_close[1] < c_close[2] <= c_open[3] \
            and c_high[2] >= c_high[3] and abs(first - sec) < tolerance and abs(sec - third) < tolerance:
        return True
    else:
        return False


def three_line_strike_bearish(c_open, c_high, c_close, tolerance: float):
    # work with at least 4 candle and return True if pattern be true
    first = abs(c_open[2] - c_close[2])
    sec = abs(c_open[1] - c_close[1])
    third = abs(c_open[0] - c_close[0])

    if c_open[3] < c_close[2] < c_close[1] < c_open[2] < c_close[0] < c_open[1] < c_open[0] < c_close[3] \
            and c_high[0] < c_close[3] and abs(first - sec) < tolerance and abs(sec - third) < tolerance:
        return True
    else:
        return False


def three_white_soldiers(c_open, c_high, c_close):
    # work with at least 4 candle and return True if pattern be true
    if c_open[0] > c_close[0] > c_open[1] and c_close[1] > _average(c_close[1], c_open[1]) \
            and c_open[1] < c_open[2] < c_close[1] and c_close[2] > _average(c_close[2], c_open[2]) \
            and c_open[2] < c_open[3] < c_close[2] and c_close[3] > _average(c_close[3], c_open[3]) \
            and c_high[1] < c_high[2] < c_high[3]:
        return True
    else:
        return False


def three_black_crows(c_open, c_close, c_low):
    # work with at least 4 candle and return True if pattern be true
    if c_open[0] < c_close[0] < c_open[1] and c_close[1] < _average(c_close[1], c_open[1]) \
            and c_open[1] > c_open[2] > c_close[1] and c_close[2] < _average(c_close[2], c_open[2]) \
            and c_open[2] > c_open[3] > c_close[2] and c_close[3] < _average(c_close[3], c_open[3]) \
            and c_low[1] > c_low[2] > c_low[3]:
        return True
    else:
        return False


def morning_star(c_open, c_close):
    # work with at least 4 candle and return True if pattern be true
    if c_close[0] > c_close[1] > c_open[2] and c_open[1] > c_close[1] > c_close[2] \
            and c_open[3] > c_open[2] and c_open[3] > c_close[2] and c_close[3] > c_close[1] \
            and c_open[1] - c_close[1] > c_close[3] - c_open[3]:
        return True
    else:
        return False


def evening_star(c_open, c_close):
    # work with at least 4 candle and return True if pattern be true
    if c_close[0] < c_close[1] < c_open[2] and c_open[1] < c_close[1] < c_close[2] \
            and c_open[3] < c_open[2] and c_open[3] < c_close[2] and c_close[3] < c_close[1] \
            and c_close[1] - c_open[1] > c_open[3] - c_close[3]:
        return True
    else:
        return False


def three_stars_in_the_south(c_open, c_high, c_close, c_low, tolerance: float):
    # work with at least 4 candle and return True if pattern be true
    if c_open[0] > c_close[0] and c_open[1] > c_close[1] and abs(c_open[1] - c_high[1]) < tolerance \
            and c_close[2] < c_open[2] < c_open[1] and c_open[2] > c_close[1] and c_low[2] > c_low[1] \
            and abs(c_open[2] - c_high[2]) < tolerance and c_close[3] < c_open[3] < c_open[2] \
            and c_open[3] > c_close[2] and abs(c_open[3] - c_high[3]) < tolerance \
            and abs(c_close[3] - c_low[3]) < tolerance and c_close[3] >= c_low[2]:
        return True
    else:
        return False


# 5 candles needed
def breakaway_bullish(c_open, c_close):
    # work with at least 5 candle and return True if pattern be true
    if c_open[0] > c_close[0] > c_open[1] and c_close[1] < c_close[2] < c_open[2] and c_open[3] > c_close[2] \
            and c_open[3] > c_close[3] and c_open[4] < c_close[4] and c_open[4] < c_open[3] and c_close[4] > c_open[1]:
        return True
    else:
        return False


def falling_three_methods(c_open, c_close, c_low):
    # work with at least 5 candle and return True if pattern be true
    if c_open[0] > c_close[0] \
            and c_close[4] < c_open[1] < c_open[2] < c_close[1] < c_close[2] < c_open[3] < c_close[3] \
            and c_close[3] > c_open[4] > c_open[3] and c_close[4] < c_low[0]:
        return True
    else:
        return False


def breakaway_bearish(c_open, c_close):
    # work with at least 5 candle and return True if pattern be true
    if c_open[0] < c_close[0] <= c_open[1] < c_close[1] < c_close[2] < c_open[1] < c_open[2] \
            and c_open[2] > c_close[2] and c_close[2] < c_open[3] < c_close[3] and c_close[3] > c_open[2] \
            and c_open[4] < _average(c_open[3], c_close[3]) and c_close[4] < c_open[1]:
        return True
    else:
        return False


def ladder_bottom(c_open, c_close, c_low):
    # work with at least 5 candle and return True if pattern be true
    if c_open[0] > c_close[0] and c_close[1] < c_open[1] < c_open[0] and c_close[2] < c_open[2] < c_open[1] \
            and c_close[3] < c_open[3] < c_open[2] and c_close[4] > c_open[4] > c_open[3] \
            and c_low[0] > c_low[1] > c_low[2] > c_low[3]:
        return True
    else:
        return False
