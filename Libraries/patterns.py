import pandas as pd


def _average(*inputs: float):
    result = 0.0
    for put in inputs:
        result += put
    return result / len(inputs)


def _last_limit_data(candles, limit: int):
    candles = candles.tail(limit).reset_index()
    c_high = candles['high']
    c_low = candles['low']
    c_close = candles['close']
    c_open = candles['open']
    return c_open, c_high, c_close, c_low


def get_ohcl(candles):
    candles = candles.reset_index(drop=True)
    c_high = candles['high']
    c_low = candles['low']
    c_close = candles['close']
    c_open = candles['open']
    return c_open, c_high, c_close, c_low


class Patterns:
    def __init__(self, dataframe: pd.DataFrame):
        self.data = dataframe

    def pattern_2_candles(self, candles):
        # work with at least 2 candle and add rows to dataframe 1 if pattern be true
        c_open, c_high, c_close, c_low = get_ohcl(self.data.loc[candles.index])
        if candles.index.stop <= len(self.data):
            if c_low[0] > c_open[1] > c_close[1] > c_low[1] and c_high[1] < c_low[0]:
                self.data.loc[candles.index.stop - 1, 'hammer'] = 1
            if c_open[1] > c_close[1] > c_high[0] > c_low[1]:
                self.data.loc[candles.index.stop - 1, 'hanging_man'] = 1
            if c_high[1] > c_high[0] > _average(c_open[1], c_close[1]) and c_open[1] > c_close[1] > c_close[0] \
                    and c_open[1] > c_high[0]:
                self.data.loc[candles.index.stop - 1, 'shooting_star'] = 1
            if c_open[0] > c_close[0] and c_open[0] > c_high[1] and c_close[0] < c_low[1]:
                self.data.loc[candles.index.stop - 1, 'harami_cross_bullish'] = 1
            if c_open[0] < c_close[0] and c_open[0] < c_low[1] and c_close[0] > c_high[1]:
                self.data.loc[candles.index.stop - 1, 'harami_cross_bearish'] = 1
            if c_open[0] > c_close[0] and abs(c_open[1] - c_close[1]) < 20 and c_high[1] >= c_close[0]:
                self.data.loc[candles.index.stop - 1, 'doji_star_bullish'] = 1
            if c_open[0] < c_close[0] and c_open[1] > c_close[1] and c_close[1] <= c_close[0] < _average(c_open[1],
                                                                                                         c_close[1]):
                self.data.loc[candles.index.stop - 1, 'doji_star_bearish'] = 1
            if c_close[1] <= c_close[0] < c_open[0] <= c_high[1] and c_close[1] < c_open[1] <= c_open[0]:
                self.data.loc[candles.index.stop - 1, 'matching_low'] = 1
            if c_close[0] > c_open[0] >= c_low[1] and c_close[0] >= c_close[1] > c_open[1] > c_open[0]:
                self.data.loc[candles.index.stop - 1, 'matching_high'] = 1
            if c_high[0] > c_open[0] >= c_high[1] > c_open[1] > c_close[1] > c_low[1] > c_close[0] > c_low[0]:
                self.data.loc[candles.index.stop - 1, 'homing_pigeon'] = 1
            if abs(abs(c_open[1] - c_close[1]) - abs(c_open[0] - c_close[0])) < 0.0005 and c_open[0] > c_close[0] \
                    and c_high[0] > c_open[1] and c_open[1] < c_close[1] and c_low[1] < c_open[0] < c_open[1]:
                self.data.loc[candles.index.stop - 1, 'separating_lines_bullish'] = 1
            if abs(abs(c_open[1] - c_close[1]) - abs(c_open[0] - c_close[0])) < 0.0005 \
                    and c_open[0] < c_close[0] < c_open[1] <= c_open[0] < c_high[1] and c_low[0] < c_open[1]:
                self.data.loc[candles.index.stop - 1, 'separating_lines_bearish'] = 1
            if c_open[0] < c_close[0] < c_close[1] < c_open[1] and abs(c_low[1] - c_close[1]) < 0.0005 \
                    and abs(c_open[0] - c_close[0]) > abs(c_open[1] - c_close[1]) and c_close[1] <= c_high[0]:
                self.data.loc[candles.index.stop - 1, 'on_neck_line_bullish'] = 1
            if c_open[0] > c_close[0] > c_close[1] > c_open[1] and abs(c_open[0] - c_close[0]) > abs(
                    c_open[1] - c_close[1]) and c_close[1] <= c_low[0]:
                self.data.loc[candles.index.stop - 1, 'on_neck_line_bearish'] = 1
            if c_open[0] < c_close[0] <= c_close[1] < c_open[1] and abs(c_open[0] - c_close[0]) > abs(
                    c_open[1] - c_close[1]):
                self.data.loc[candles.index.stop - 1, 'in_neck_line_bullish'] = 1
            if c_open[0] > c_close[0] >= c_close[1] > c_open[1] and abs(c_open[0] - c_close[0]) > abs(
                    c_open[1] - c_close[1]):
                self.data.loc[candles.index.stop - 1, 'in_neck_line_bearish'] = 1
            if c_open[0] > c_close[0] > c_open[1] and c_low[0] > c_open[1] and abs(c_open[1] - c_low[1]) < 0.0005 \
                    and c_close[1] > _average(c_close[1], c_open[1]):
                self.data.loc[candles.index.stop - 1, 'belt_hold_bullish'] = 1
            if c_open[0] < c_close[0] < c_open[1] and c_high[0] < c_open[1] \
                    and abs(c_open[1] - c_high[1]) < 0.0005 and c_close[1] < _average(c_close[1], c_open[1]):
                self.data.loc[candles.index.stop - 1, 'belt_hold_bearish'] = 1
            if c_open[0] > c_close[0] and abs(c_open[0] - c_high[0]) < 0.0005 and abs(c_close[0] - c_low[0]) < 0.0005 \
                    and c_open[1] > c_open[0] and abs(c_open[1] - c_low[1]) < 0.0005 \
                    and abs(c_close[1] - c_high[1]) < 0.0005 and c_close[1] - c_open[1] > c_open[0] - c_close[0]:
                self.data.loc[candles.index.stop - 1, 'kicking_bullish'] = 1
            if c_open[0] < c_close[0] and abs(c_open[0] - c_low[0]) < 0.0005 and abs(c_close[0] - c_high[0]) < 0.0005 \
                    and c_open[1] < c_open[0] and abs(c_open[1] - c_high[1]) < 0.0005 \
                    and abs(c_close[1] - c_low[1]) < 0.0005 and c_open[1] - c_close[1] > c_close[0] - c_open[0]:
                self.data.loc[candles.index.stop - 1, 'kicking_bearish'] = 1
        return 0

    def pattern_3_candles(self, candles):
        # work with at least 3 candle and add rows to dataframe 1 if pattern be true
        c_open, c_high, c_close, c_low = get_ohcl(self.data.loc[candles.index])
        if candles.index.stop <= len(self.data):
            if c_low[0] > c_high[1] > c_high[2] > c_close[1] > c_close[2] and c_open[2] < c_close[1] and c_high[2] < \
                    c_open[1]:
                self.data.loc[candles.index.stop - 1, 'inverted_hammer'] = 1
            if c_open[0] > c_close[0] and abs(c_open[1] - c_close[1]) < 20 and c_close[1] < c_open[2] < c_close[2] \
                    and c_low[2] >= c_close[1]:
                self.data.loc[candles.index.stop - 1, 'morning_doji_star'] = 1
            if c_open[0] < c_close[0] and abs(c_open[1] - c_close[1]) < 20 and c_close[1] > c_open[2] > c_close[2] \
                    and c_high[2] <= c_close[1]:
                self.data.loc[candles.index.stop - 1, 'evening_doji_star'] = 1
            if c_open[0] > c_close[0] >= c_high[1] and abs(c_open[1] - c_close[1]) < 20 and c_open[2] < c_close[2] \
                    and c_close[2] > c_close[0] and c_close[2] >= _average(c_open[0], c_close[0]) \
                    and c_open[2] > c_close[1]:
                self.data.loc[candles.index.stop - 1, 'abandoned_baby_bullish'] = 1
            if c_open[0] < c_close[0] < c_close[1] and abs(c_open[1] - c_close[1]) < 20 \
                    and c_close[1] > c_open[2] > c_close[2] and _average(c_open[0], c_close[0]) >= c_close[2] \
                    and c_high[2] <= c_close[1]:
                self.data.loc[candles.index.stop - 1, 'abandoned_baby_bearish'] = 1
            if c_close[1] < c_close[2] < c_close[0] and abs(c_open[2] - c_close[2]) < 20 \
                    and abs(c_open[1] - c_close[1]) < 20 and abs(c_open[0] - c_close[0]) < 20:
                self.data.loc[candles.index.stop - 1, 'tri_star_bullish'] = 1
            if c_close[0] < c_close[2] < c_close[1] and abs(c_open[2] - c_close[2]) < 20 \
                    and abs(c_open[1] - c_close[1]) < 20 and abs(c_open[0] - c_close[0]) < 20:
                self.data.loc[candles.index.stop - 1, 'tri_star_bearish'] = 1
            if c_open[0] > c_close[0] and c_open[0] > c_close[1] > c_open[1] > c_close[0] \
                    and c_open[1] < c_open[2] < c_close[1] and c_open[2] < c_close[2] and c_low[2] >= c_open[1] \
                    and c_close[2] > c_open[0]:
                self.data.loc[candles.index.stop - 1, 'three_inside_up'] = 1
            if c_close[0] > c_open[1] > c_close[1] > c_open[0] > c_close[2] \
                    and _average(c_open[1], c_close[1]) > c_open[2] > c_close[2]:
                self.data.loc[candles.index.stop - 1, 'three_inside_down'] = 1
            if c_open[1] < c_close[0] < c_open[0] < c_close[1] and c_open[2] < c_close[1] < c_close[2]:
                self.data.loc[candles.index.stop - 1, 'three_outside_up'] = 1
            if c_open[1] > c_close[0] > c_open[0] > c_close[1] > c_close[2] and c_open[2] > c_close[1] \
                    and c_high[2] < c_open[1]:
                self.data.loc[candles.index.stop - 1, 'three_outside_down'] = 1
            if c_open[0] > c_open[1] > c_close[1] > c_close[0] and c_low[1] < c_low[0] \
                    and c_close[0] <= c_open[2] < c_close[2] < c_close[1] < c_high[2]:
                self.data.loc[candles.index.stop - 1, 'unique_three_river'] = 1
            if c_close[2] < c_open[2] <= c_close[1] < c_open[1] <= c_close[0] < c_open[0]:
                self.data.loc[candles.index.stop - 1, 'loentical_three_cross'] = 1
            if c_open[0] < c_close[0] and c_open[1] < c_close[1] and c_open[2] < c_close[2] and c_open[1] <= c_close[0] \
                    and abs(c_open[2] - c_close[2]) < abs(c_open[1] - c_close[1]) and c_open[2] > c_close[1] \
                    and c_low[2] >= c_close[1]:
                self.data.loc[candles.index.stop - 1, 'deliberation'] = 1
            if c_open[0] < c_close[0] and c_open[2] > c_open[1] > c_close[1] > c_close[2] >= c_high[0]:
                self.data.loc[candles.index.stop - 1, 'upside_gap_two_crows'] = 1
            if abs(c_open[2] - c_close[2]) < abs(c_open[1] - c_close[1]) < abs(c_open[0] - c_close[0]) \
                    and c_open[0] < c_close[0] and c_open[1] < c_close[1] and c_open[2] < c_close[2] \
                    and c_open[1] < c_close[0] and c_open[2] < c_close[1] and c_high[1] > c_close[2] \
                    and c_low[2] < _average(c_open[1], c_close[1]):
                self.data.loc[candles.index.stop - 1, 'advance_block'] = 1
            if abs(c_open[0] - c_close[0]) > abs(c_open[1] - c_close[1]) \
                    and abs(c_open[2] - c_close[2]) > abs(c_open[1] - c_close[1]) and c_open[0] < c_close[0] \
                    and c_high[0] <= c_low[1] and c_open[1] > c_close[1] \
                    and c_close[1] < c_open[2] <= _average(c_open[1], c_close[1]) and c_open[2] > c_close[2] \
                    and c_low[2] < _average(c_open[0], c_close[0]):
                self.data.loc[candles.index.stop - 1, 'two_cows'] = 1
            if c_open[0] < c_close[0] < c_close[2] < c_open[1] < c_open[2] < c_close[1]:
                self.data.loc[candles.index.stop - 1, 'upside_tasuki_gap'] = 1
            if c_open[0] > c_close[0] > c_close[2] > c_open[1] > c_open[2] > c_close[1]:
                self.data.loc[candles.index.stop - 1, 'downside_tasuki_gap'] = 1
            if c_open[0] < c_close[0] < c_open[2] < c_open[1] < c_close[2] < c_close[1] <= c_high[2] \
                    and c_low[1] > c_high[0]:
                self.data.loc[candles.index.stop - 1, 'sidebyside_white_lines_bullish'] = 1
            if c_open[0] > c_close[0] > c_close[1] >= c_close[2] > c_open[2] >= c_open[1] and c_high[1] <= c_low[0]:
                self.data.loc[candles.index.stop - 1, 'sidebyside_white_lines_bearish'] = 1
            if c_open[0] < c_close[2] < c_close[0] < c_open[1] < c_open[2] < c_close[1] and c_low[1] > c_high[0]:
                self.data.loc[candles.index.stop - 1, 'upside_gap_three_methods'] = 1
            if c_open[0] > c_close[2] > c_close[0] > c_open[1] > c_open[2] > c_close[1] and c_high[1] < c_low[0]:
                self.data.loc[candles.index.stop - 1, 'downside_gap_three_methods'] = 1
            if c_high[2] > c_high[1] and c_low[2] < c_low[1] and c_open[2] < c_open[1] and c_close[2] > c_close[1] \
                    and c_close[2] > c_open[2] and c_close[1] < c_close[0] and c_close[2] > c_open[1]:
                self.data.loc[candles.index.stop - 1, 'engulfing_bullish'] = 1
            if c_high[2] > c_high[1] and c_low[2] < c_low[1] and c_open[2] > c_open[1] and c_close[2] < c_close[1] \
                    and c_close[2] < c_open[2] and c_close[1] > c_close[0] and c_close[2] < c_open[1]:
                self.data.loc[candles.index.stop - 1, 'engulfing_bearish'] = 1
            if c_open[1] > c_close[1] and c_close[1] < c_close[0] and c_close[1] < c_open[2] < c_open[1] \
                    and c_close[1] < c_close[2] < c_open[1] and c_high[2] < c_high[1] and c_low[2] > c_low[1] \
                    and c_close[2] >= c_open[2]:
                self.data.loc[candles.index.stop - 1, 'harami_bullish'] = 1
            if c_open[1] < c_close[1] and c_close[1] > c_close[0] and c_close[1] > c_open[2] > c_open[1] \
                    and c_close[1] > c_close[2] > c_open[1] and c_high[2] < c_high[1] and c_low[2] > c_low[1] \
                    and c_close[2] <= c_open[2]:
                self.data.loc[candles.index.stop - 1, 'harami_bearish'] = 1
            if c_close[0] > c_close[1] and c_open[2] < c_low[1] \
                    and _average(c_open[1], c_close[1]) < c_close[2] < c_open[1]:
                self.data.loc[candles.index.stop - 1, 'piercing_line'] = 1
            if c_close[0] < c_close[1] and c_open[2] > c_high[1] \
                    and _average(c_open[1], c_close[1]) > c_close[2] > c_open[1]:
                self.data.loc[candles.index.stop - 1, 'dark_cloud_cover'] = 1
            if c_open[0] > c_close[0] and c_close[0] < c_open[1] < c_close[1] < c_open[2] and c_open[2] > c_close[2] \
                    and abs(c_close[2] - c_close[0]) < 0.0005:
                self.data.loc[candles.index.stop - 1, 'stick_sandwich'] = 1
            if c_open[0] > c_close[0] and c_open[1] > c_close[1] and abs(c_close[1] - c_close[2]) < 0.0005 \
                    and c_open[2] < c_close[2] and c_open[1] >= c_high[2]:
                self.data.loc[candles.index.stop - 1, 'meeting_line_bullish'] = 1
            if c_open[0] < c_close[0] and c_open[1] < c_close[1] and abs(c_close[1] - c_close[2]) < 0.0005 \
                    and c_open[2] > c_close[2] and c_open[1] <= c_low[2]:
                self.data.loc[candles.index.stop - 1, 'meeting_line_bearish'] = 1
        return 0

    def pattern_4_candles(self, candles):
        # work with at least 4 candle and add rows to dataframe 1 if pattern be true
        c_open, c_high, c_close, c_low = get_ohcl(self.data.loc[candles.index])
        if candles.index.stop <= len(self.data):
            if c_open[0] > c_close[0] and c_open[1] > c_close[0] and c_open[1] > c_close[1] and c_high[2] > c_close[1] \
                    and c_close[1] > c_open[2] > c_close[2] and c_open[3] >= c_high[2] and c_close[3] <= c_close[2]:
                self.data.loc[candles.index.stop - 1, 'concealing_baby'] = 1
            if c_low[3] >= c_low[0] and c_open[0] <= c_close[3] < c_open[3] < c_close[2] < c_open[2] <= c_close[1] \
                    < c_close[1] < c_open[1] and c_high[3] > c_close[2]:
                self.data.loc[candles.index.stop - 1, 'rising_three_methods'] = 1
            if c_close[3] < c_open[0] < c_open[1] < c_close[0] <= c_open[2] < c_close[1] < c_close[2] <= c_open[3] \
                    and c_high[2] >= c_high[3] and abs(
                abs(c_open[2] - c_close[2]) - abs(c_open[1] - c_close[1])) < 0.0005 \
                    and abs(abs(c_open[1] - c_close[1]) - abs(c_open[0] - c_close[0])) < 0.0005:
                self.data.loc[candles.index.stop - 1, 'three_line_strike_bullish'] = 1
            if c_open[3] < c_close[2] < c_close[1] < c_open[2] < c_close[0] < c_open[1] < c_open[0] < c_close[3] \
                    and c_high[0] < c_close[3] and abs(
                abs(c_open[2] - c_close[2]) - abs(c_open[1] - c_close[1])) < 0.0005 \
                    and abs(abs(c_open[1] - c_close[1]) - abs(c_open[0] - c_close[0])) < 0.0005:
                self.data.loc[candles.index.stop - 1, 'three_line_strike_beearish'] = 1
            if c_open[0] > c_close[0] > c_open[1] and c_close[1] > _average(c_close[1], c_open[1]) \
                    and c_open[1] < c_open[2] < c_close[1] and c_close[2] > _average(c_close[2], c_open[2]) \
                    and c_open[2] < c_open[3] < c_close[2] and c_close[3] > _average(c_close[3], c_open[3]) \
                    and c_high[1] < c_high[2] < c_high[3]:
                self.data.loc[candles.index.stop - 1, 'three_white_soldiers'] = 1
            if c_open[0] < c_close[0] < c_open[1] and c_close[1] < _average(c_close[1], c_open[1]) \
                    and c_open[1] > c_open[2] > c_close[1] and c_close[2] < _average(c_close[2], c_open[2]) \
                    and c_open[2] > c_open[3] > c_close[2] and c_close[3] < _average(c_close[3], c_open[3]) \
                    and c_low[1] > c_low[2] > c_low[3]:
                self.data.loc[candles.index.stop - 1, 'three_black_crows'] = 1
            if c_close[0] > c_close[1] > c_open[2] and c_open[1] > c_close[1] > c_close[2] \
                    and c_open[3] > c_open[2] and c_open[3] > c_close[2] and c_close[3] > c_close[1] \
                    and c_open[1] - c_close[1] > c_close[3] - c_open[3]:
                self.data.loc[candles.index.stop - 1, 'morning_star'] = 1
            if c_close[0] < c_close[1] < c_open[2] and c_open[1] < c_close[1] < c_close[2] \
                    and c_open[3] < c_open[2] and c_open[3] < c_close[2] and c_close[3] < c_close[1] \
                    and c_close[1] - c_open[1] > c_open[3] - c_close[3]:
                self.data.loc[candles.index.stop - 1, 'evening_star'] = 1
            if c_open[0] > c_close[0] and c_open[1] > c_close[1] and abs(c_open[1] - c_high[1]) < 0.0005 \
                    and c_close[2] < c_open[2] < c_open[1] and c_open[2] > c_close[1] and c_low[2] > c_low[1] \
                    and abs(c_open[2] - c_high[2]) < 0.0005 and c_close[3] < c_open[3] < c_open[2] \
                    and c_open[3] > c_close[2] and abs(c_open[3] - c_high[3]) < 0.0005 \
                    and abs(c_close[3] - c_low[3]) < 0.0005 and c_close[3] >= c_low[2]:
                self.data.loc[candles.index.stop - 1, 'three_stars_in_the_south'] = 1

        return 0

    def pattern_5_candles(self, candles):
        # work with at least 5 candle and add rows to dataframe 1 if pattern be true
        c_open, c_high, c_close, c_low = get_ohcl(self.data.loc[candles.index])
        if candles.index.stop <= len(self.data):
            if c_open[0] > c_close[0] \
                    and c_close[4] < c_open[1] < c_open[2] < c_close[1] < c_close[2] < c_open[3] < c_close[3] \
                    and c_close[3] > c_open[4] > c_open[3] and c_close[4] < c_low[0]:
                self.data.loc[candles.index.stop - 1, 'falling_three_methods'] = 1
            if c_open[0] > c_close[0] > c_open[1] and c_close[1] < c_close[2] < c_open[2] and c_open[3] > c_close[2] \
                    and c_open[3] > c_close[3] and c_open[4] < c_close[4] and c_open[4] < c_open[3] \
                    and c_close[4] > c_open[1]:
                self.data.loc[candles.index.stop - 1, 'breakaway_bullish'] = 1
            if c_open[0] < c_close[0] <= c_open[1] < c_close[1] < c_close[2] < c_open[1] < c_open[2] \
                    and c_open[2] > c_close[2] and c_close[2] < c_open[3] < c_close[3] and c_close[3] > c_open[2] \
                    and c_open[4] < _average(c_open[3], c_close[3]) and c_close[4] < c_open[1]:
                self.data.loc[candles.index.stop - 1, 'breakaway_bearish'] = 1
            if c_open[0] > c_close[0] and c_close[1] < c_open[1] < c_open[0] and c_close[2] < c_open[2] < c_open[1] \
                    and c_close[3] < c_open[3] < c_open[2] and c_close[4] > c_open[4] > c_open[3] \
                    and c_low[0] > c_low[1] > c_low[2] > c_low[3]:
                self.data.loc[candles.index.stop - 1, 'ladder_bottom'] = 1

        return 0

    def rolling_2candle(self):
        window = self.data.rolling(2)
        window.apply(self.pattern_2_candles, raw=False)

    def rolling_3candle(self):
        window = self.data.rolling(3)
        window.apply(self.pattern_3_candles, raw=False)

    def rolling_4candle(self):
        window = self.data.rolling(4)
        window.apply(self.pattern_4_candles, raw=False)

    def rolling_5candle(self):
        window = self.data.rolling(5)
        window.apply(self.pattern_5_candles, raw=False)

    def rolling_all(self):
        self.rolling_2candle()
        self.rolling_3candle()
        self.rolling_4candle()
        self.rolling_5candle()

    def save_csv(self):
        self.data.to_csv('test.csv')


# test
# data = pd.read_csv('../Static/Bitcoin-30m.csv')
# del data['date']
# del data['volume']
# pat = Patterns(data)
# pat.rolling_2candle()
# pat.save_csv()


def hammer(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_low[0] > c_open[1] > c_close[1] > c_low[1] and c_high[1] < c_low[0]:
        return True
    else:
        return False


def hanging_man(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[1] > c_close[1] > c_high[0] > c_low[1]:
        return True
    else:
        return False


def inverted_hammer(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_low[0] > c_high[1] > c_high[2] > c_close[1] > c_close[2] and c_open[2] < c_close[1] and c_high[2] < c_open[1]:
        return True
    else:
        return False


def shooting_star(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_high[1] > c_high[0] > _average(c_open[1], c_close[1]) and c_open[1] > c_close[1] > c_close[0] \
            and c_open[1] > c_high[0]:
        return True
    else:
        return False


def harami_cross_bullish(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[0] > c_close[0] and c_open[0] > c_high[1] and c_close[0] < c_low[1]:
        return True
    else:
        return False


def harami_cross_bearish(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[0] < c_close[0] and c_open[0] < c_low[1] and c_close[0] > c_high[1]:
        return True
    else:
        return False


def doji_star_bullish(candles, limit: float):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[0] > c_close[0] and abs(c_open[1] - c_close[1]) < limit and c_high[1] >= c_close[0]:
        return True
    else:
        return False


def doji_star_bearish(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[0] < c_close[0] and c_open[1] > c_close[1] and c_close[1] <= c_close[0] < _average(c_open[1], c_close[1]):
        return True
    else:
        return False


def morning_doji_star(candles, limit: float):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] > c_close[0] and abs(c_open[1] - c_close[1]) < limit and c_close[1] < c_open[2] < c_close[2] \
            and c_low[2] >= c_close[1]:
        return True
    else:
        return False


def evening_doji_star(candles, limit: float):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] < c_close[0] and abs(c_open[1] - c_close[1]) < limit and c_close[1] > c_open[2] > c_close[2] \
            and c_high[2] <= c_close[1]:
        return True
    else:
        return False


def abandoned_baby_bullish(candles, limit: float):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] > c_close[0] >= c_high[1] and abs(c_open[1] - c_close[1]) < limit and c_open[2] < c_close[2] \
            and c_close[2] > c_close[0] and c_close[2] >= _average(c_open[0], c_close[0]) and c_open[2] > c_close[1]:
        return True
    else:
        return False


def abandoned_baby_bearish(candles, limit: float):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] < c_close[0] < c_close[1] and abs(c_open[1] - c_close[1]) < limit \
            and c_close[1] > c_open[2] > c_close[2] and _average(c_open[0], c_close[0]) >= c_close[2] \
            and c_high[2] <= c_close[1]:
        return True
    else:
        return False


def tri_star_bullish(candles, limit: float):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_close[1] < c_close[2] < c_close[0] and abs(c_open[2] - c_close[2]) < limit \
            and abs(c_open[1] - c_close[1]) < limit and abs(c_open[0] - c_close[0]) < limit:
        return True
    else:
        return False


def tri_star_bearish(candles, limit: float):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_close[0] < c_close[2] < c_close[1] and abs(c_open[2] - c_close[2]) < limit \
            and abs(c_open[1] - c_close[1]) < limit and abs(c_open[0] - c_close[0]) < limit:
        return True
    else:
        return False


def three_inside_up(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] > c_close[0] and c_open[0] > c_close[1] > c_open[1] > c_close[0] \
            and c_open[1] < c_open[2] < c_close[1] and c_open[2] < c_close[2] and c_low[2] >= c_open[1] \
            and c_close[2] > c_open[0]:
        return True
    else:
        return False


def three_inside_down(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_close[0] > c_open[1] > c_close[1] > c_open[0] > c_close[2] \
            and _average(c_open[1], c_close[1]) > c_open[2] > c_close[2]:
        return True
    else:
        return False


def three_outside_up(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[1] < c_close[0] < c_open[0] < c_close[1] and c_open[2] < c_close[1] < c_close[2]:
        return True
    else:
        return False


def three_outside_down(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[1] > c_close[0] > c_open[0] > c_close[1] > c_close[2] and c_open[2] > c_close[1] \
            and c_high[2] < c_open[1]:
        return True
    else:
        return False


def unique_three_river(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] > c_open[1] > c_close[1] > c_close[0] and c_low[1] < c_low[0] \
            and c_close[0] <= c_open[2] < c_close[2] < c_close[1] < c_high[2]:
        return True
    else:
        return False


def concealing_baby(candles):
    # work with at least 4 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 4)
    if c_open[0] > c_close[0] and c_open[1] > c_close[0] and c_open[1] > c_close[1] and c_high[2] > c_close[1] \
            and c_close[1] > c_open[2] > c_close[2] and c_open[3] >= c_high[2] and c_close[3] <= c_close[2]:
        return True
    else:
        return False


def loentical_three_cross(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_close[2] < c_open[2] <= c_close[1] < c_open[1] <= c_close[0] < c_open[0]:
        return True
    else:
        return False


def deliberation(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] < c_close[0] and c_open[1] < c_close[1] and c_open[2] < c_close[2] and c_open[1] <= c_close[0] \
            and abs(c_open[2] - c_close[2]) < abs(c_open[1] - c_close[1]) and c_open[2] > c_close[1] and c_low[2] >= \
            c_close[1]:
        return True
    else:
        return False


def matching_low(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_close[1] <= c_close[0] < c_open[0] <= c_high[1] and c_close[1] < c_open[1] <= c_open[0]:
        return True
    else:
        return False


def matching_high(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_close[0] > c_open[0] >= c_low[1] and c_close[0] >= c_close[1] > c_open[1] > c_open[0]:
        return True
    else:
        return False


def upside_gap_two_crows(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] < c_close[0] and c_open[2] > c_open[1] > c_close[1] > c_close[2] >= c_high[0]:
        return True
    else:
        return False


def homing_pigeon(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_high[0] > c_open[0] >= c_high[1] > c_open[1] > c_close[1] > c_low[1] > c_close[0] > c_low[0]:
        return True
    else:
        return False


def advance_block(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if abs(c_open[2] - c_close[2]) < abs(c_open[1] - c_close[1]) < abs(c_open[0] - c_close[0]) \
            and c_open[0] < c_close[0] and c_open[1] < c_close[1] and c_open[2] < c_close[2] \
            and c_open[1] < c_close[0] and c_open[2] < c_close[1] and c_high[1] > c_close[2] \
            and c_low[2] < _average(c_open[1], c_close[1]):
        return True
    else:
        return False


def two_crows(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if abs(c_open[0] - c_close[0]) > abs(c_open[1] - c_close[1]) \
            and abs(c_open[2] - c_close[2]) > abs(c_open[1] - c_close[1]) and c_open[0] < c_close[0] \
            and c_high[0] <= c_low[1] and c_open[1] > c_close[1] \
            and c_close[1] < c_open[2] <= _average(c_open[1], c_close[1]) and c_open[2] > c_close[2] \
            and c_low[2] < _average(c_open[0], c_close[0]):
        return True
    else:
        return False


def rising_three_methods(candles):
    # work with at least 4 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 4)
    if c_low[3] >= c_low[0] and c_open[0] <= c_close[3] < c_open[3] < c_close[2] < c_open[2] <= c_close[1] \
            < c_close[1] < c_open[1] and c_high[3] > c_close[2]:
        return True
    else:
        return False


def falling_three_methods(candles):
    # work with at least 5 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 5)
    if c_open[0] > c_close[0] \
            and c_close[4] < c_open[1] < c_open[2] < c_close[1] < c_close[2] < c_open[3] < c_close[3] \
            and c_close[3] > c_open[4] > c_open[3] and c_close[4] < c_low[0]:
        return True
    else:
        return False


def upside_tasuki_gap(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] < c_close[0] < c_close[2] < c_open[1] < c_open[2] < c_close[1]:
        return True
    else:
        return False


def downside_tasuki_gap(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] > c_close[0] > c_close[2] > c_open[1] > c_open[2] > c_close[1]:
        return True
    else:
        return False


def sidebyside_white_lines_bullish(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] < c_close[0] < c_open[2] < c_open[1] < c_close[2] < c_close[1] <= c_high[2] and c_low[1] > c_high[0]:
        return True
    else:
        return False


def sidebyside_white_lines_bearish(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] > c_close[0] > c_close[1] >= c_close[2] > c_open[2] >= c_open[1] and c_high[1] <= c_low[0]:
        return True
    else:
        return False


def three_line_strike_bullish(candles, tolerance: float):
    # work with at least 4 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 4)
    first = abs(c_open[2] - c_close[2])
    sec = abs(c_open[1] - c_close[1])
    third = abs(c_open[0] - c_close[0])

    if c_close[3] < c_open[0] < c_open[1] < c_close[0] <= c_open[2] < c_close[1] < c_close[2] <= c_open[3] \
            and c_high[2] >= c_high[3] and abs(first - sec) < tolerance and abs(sec - third) < tolerance:
        return True
    else:
        return False


def separating_lines_bullish(candles, tolerance: float):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    first = abs(c_open[1] - c_close[1])
    sec = abs(c_open[0] - c_close[0])

    if abs(first - sec) < tolerance and c_open[0] > c_close[0] and c_high[0] > c_open[1] and c_open[1] < c_close[1] \
            and c_low[1] < c_open[0] < c_open[1]:
        return True
    else:
        return False


def separating_lines_bearish(candles, tolerance: float):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    first = abs(c_open[1] - c_close[1])
    sec = abs(c_open[0] - c_close[0])

    if abs(first - sec) < tolerance and c_open[0] < c_close[0] < c_open[1] <= c_open[0] < c_high[1] \
            and c_low[0] < c_open[1]:
        return True
    else:
        return False


def three_line_strike_bearish(candles, tolerance: float):
    # work with at least 4 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 4)
    first = abs(c_open[2] - c_close[2])
    sec = abs(c_open[1] - c_close[1])
    third = abs(c_open[0] - c_close[0])

    if c_open[3] < c_close[2] < c_close[1] < c_open[2] < c_close[0] < c_open[1] < c_open[0] < c_close[3] \
            and c_high[0] < c_close[3] and abs(first - sec) < tolerance and abs(sec - third) < tolerance:
        return True
    else:
        return False


def upside_gap_three_methods(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] < c_close[2] < c_close[0] < c_open[1] < c_open[2] < c_close[1] and c_low[1] > c_high[0]:
        return True
    else:
        return False


def downside_gap_three_methods(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] > c_close[2] > c_close[0] > c_open[1] > c_open[2] > c_close[1] and c_high[1] < c_low[0]:
        return True
    else:
        return False


def on_neck_line_bullish(candles, tolerance: float):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[0] < c_close[0] < c_close[1] < c_open[1] and abs(c_low[1] - c_close[1]) < tolerance \
            and abs(c_open[0] - c_close[0]) > abs(c_open[1] - c_close[1]) and c_close[1] <= c_high[0]:
        return True
    else:
        return False


def on_neck_line_bearish(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[0] > c_close[0] > c_close[1] > c_open[1] and abs(c_open[0] - c_close[0]) > abs(c_open[1] - c_close[1]) \
            and c_close[1] <= c_low[0]:
        return True
    else:
        return False


def breakaway_bullish(candles):
    # work with at least 5 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 5)
    if c_open[0] > c_close[0] > c_open[1] and c_close[1] < c_close[2] < c_open[2] and c_open[3] > c_close[2] \
            and c_open[3] > c_close[3] and c_open[4] < c_close[4] and c_open[4] < c_open[3] and c_close[4] > c_open[1]:
        return True
    else:
        return False


def breakaway_bearish(candles):
    # work with at least 5 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 5)
    if c_open[0] < c_close[0] <= c_open[1] < c_close[1] < c_close[2] < c_open[1] < c_open[2] \
            and c_open[2] > c_close[2] and c_close[2] < c_open[3] < c_close[3] and c_close[3] > c_open[2] \
            and c_open[4] < _average(c_open[3], c_close[3]) and c_close[4] < c_open[1]:
        return True
    else:
        return False


def in_neck_line_bullish(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[0] < c_close[0] <= c_close[1] < c_open[1] and abs(c_open[0] - c_close[0]) > abs(c_open[1] - c_close[1]):
        return True
    else:
        return False


def in_neck_line_bearish(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[0] > c_close[0] >= c_close[1] > c_open[1] and abs(c_open[0] - c_close[0]) > abs(c_open[1] - c_close[1]):
        return True
    else:
        return False


# pin script
def three_white_soldiers(candles):
    # work with at least 4 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 4)
    if c_open[0] > c_close[0] > c_open[1] and c_close[1] > _average(c_close[1], c_open[1]) \
            and c_open[1] < c_open[2] < c_close[1] and c_close[2] > _average(c_close[2], c_open[2]) \
            and c_open[2] < c_open[3] < c_close[2] and c_close[3] > _average(c_close[3], c_open[3]) \
            and c_high[1] < c_high[2] < c_high[3]:
        return True
    else:
        return False


def three_black_crows(candles):
    # work with at least 4 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 4)
    if c_open[0] < c_close[0] < c_open[1] and c_close[1] < _average(c_close[1], c_open[1]) \
            and c_open[1] > c_open[2] > c_close[1] and c_close[2] < _average(c_close[2], c_open[2]) \
            and c_open[2] > c_open[3] > c_close[2] and c_close[3] < _average(c_close[3], c_open[3]) \
            and c_low[1] > c_low[2] > c_low[3]:
        return True
    else:
        return False


def engulfing_bullish(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_high[2] > c_high[1] and c_low[2] < c_low[1] and c_open[2] < c_open[1] and c_close[2] > c_close[1] \
            and c_close[2] > c_open[2] and c_close[1] < c_close[0] and c_close[2] > c_open[1]:
        return True
    else:
        return False


def engulfing_bearish(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_high[2] > c_high[1] and c_low[2] < c_low[1] and c_open[2] > c_open[1] and c_close[2] < c_close[1] \
            and c_close[2] < c_open[2] and c_close[1] > c_close[0] and c_close[2] < c_open[1]:
        return True
    else:
        return False


def harami_bullish(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[1] > c_close[1] and c_close[1] < c_close[0] and c_close[1] < c_open[2] < c_open[1] \
            and c_close[1] < c_close[2] < c_open[1] and c_high[2] < c_high[1] and c_low[2] > c_low[1] \
            and c_close[2] >= c_open[2]:
        return True
    else:
        return False


def harami_bearish(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[1] < c_close[1] and c_close[1] > c_close[0] and c_close[1] > c_open[2] > c_open[1] \
            and c_close[1] > c_close[2] > c_open[1] and c_high[2] < c_high[1] and c_low[2] > c_low[1] \
            and c_close[2] <= c_open[2]:
        return True
    else:
        return False


def piercing_line(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_close[0] > c_close[1] and c_open[2] < c_low[1] and _average(c_open[1], c_close[1]) < c_close[2] < c_open[1]:
        return True
    else:
        return False


def dark_cloud_cover(candles):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_close[0] < c_close[1] and c_open[2] > c_high[1] and _average(c_open[1], c_close[1]) > c_close[2] > c_open[1]:
        return True
    else:
        return False


def morning_star(candles):
    # work with at least 4 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 4)
    if c_close[0] > c_close[1] > c_open[2] and c_open[1] > c_close[1] > c_close[2] \
            and c_open[3] > c_open[2] and c_open[3] > c_close[2] and c_close[3] > c_close[1] \
            and c_open[1] - c_close[1] > c_close[3] - c_open[3]:
        return True
    else:
        return False


def evening_star(candles):
    # work with at least 4 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 4)
    if c_close[0] < c_close[1] < c_open[2] and c_open[1] < c_close[1] < c_close[2] \
            and c_open[3] < c_open[2] and c_open[3] < c_close[2] and c_close[3] < c_close[1] \
            and c_close[1] - c_open[1] > c_open[3] - c_close[3]:
        return True
    else:
        return False


def belt_hold_bullish(candles, tolerance: float):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[0] > c_close[0] > c_open[1] and c_low[0] > c_open[1] and abs(c_open[1] - c_low[1]) < tolerance \
            and c_close[1] > _average(c_close[1], c_open[1]):
        return True
    else:
        return False


def belt_hold_bearish(candles, tolerance: float):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[0] < c_close[0] < c_open[1] and c_high[0] < c_open[1] \
            and abs(c_open[1] - c_high[1]) < tolerance and c_close[1] < _average(c_close[1], c_open[1]):
        return True
    else:
        return False


def three_stars_in_the_south(candles, tolerance: float):
    # work with at least 4 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 4)
    if c_open[0] > c_close[0] and c_open[1] > c_close[1] and abs(c_open[1] - c_high[1]) < tolerance \
            and c_close[2] < c_open[2] < c_open[1] and c_open[2] > c_close[1] and c_low[2] > c_low[1] \
            and abs(c_open[2] - c_high[2]) < tolerance and c_close[3] < c_open[3] < c_open[2] \
            and c_open[3] > c_close[2] and abs(c_open[3] - c_high[3]) < tolerance \
            and abs(c_close[3] - c_low[3]) < tolerance and c_close[3] >= c_low[2]:
        return True
    else:
        return False


def stick_sandwich(candles, tolerance: float):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] > c_close[0] and c_close[0] < c_open[1] < c_close[1] < c_open[2] and c_open[2] > c_close[2] \
            and abs(c_close[2] - c_close[0]) < tolerance:
        return True
    else:
        return False


def meeting_line_bullish(candles, tolerance: float):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] > c_close[0] and c_open[1] > c_close[1] and abs(c_close[1] - c_close[2]) < tolerance \
            and c_open[2] < c_close[2] and c_open[1] >= c_high[2]:
        return True
    else:
        return False


def meeting_line_bearish(candles, tolerance: float):
    # work with at least 3 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 3)
    if c_open[0] < c_close[0] and c_open[1] < c_close[1] and abs(c_close[1] - c_close[2]) < tolerance \
            and c_open[2] > c_close[2] and c_open[1] <= c_low[2]:
        return True
    else:
        return False


def kicking_bullish(candles, tolerance: float):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[0] > c_close[0] and abs(c_open[0] - c_high[0]) < tolerance and abs(c_close[0] - c_low[0]) < tolerance \
            and c_open[1] > c_open[0] and abs(c_open[1] - c_low[1]) < tolerance \
            and abs(c_close[1] - c_high[1]) < tolerance and c_close[1] - c_open[1] > c_open[0] - c_close[0]:
        return True
    else:
        return False


def kicking_bearish(candles, tolerance: float):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[0] < c_close[0] and abs(c_open[0] - c_low[0]) < tolerance and abs(c_close[0] - c_high[0]) < tolerance \
            and c_open[1] < c_open[0] and abs(c_open[1] - c_high[1]) < tolerance \
            and abs(c_close[1] - c_low[1]) < tolerance and c_open[1] - c_close[1] > c_close[0] - c_open[0]:
        return True
    else:
        return False


def ladder_bottom(candles):
    # work with at least 5 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 5)
    if c_open[0] > c_close[0] and c_close[1] < c_open[1] < c_open[0] and c_close[2] < c_open[2] < c_open[1] \
            and c_close[3] < c_open[3] < c_open[2] and c_close[4] > c_open[4] > c_open[3] \
            and c_low[0] > c_low[1] > c_low[2] > c_low[3]:
        return True
    else:
        return False