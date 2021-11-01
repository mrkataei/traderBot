from Libraries.data_collector import get_candle_bitfinex as candle


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
    if c_high[1] > c_low[0] and c_high[1] > c_high[2] > c_close[1] and c_high[2] < c_open[1]:
        return True
    else:
        return False


def shooting_star(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_high[1] > c_high[0] > _average(c_open[1], c_close[1]) and c_open[1] > c_close[1] > c_close[1] > c_close[0] \
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
    if c_close[0] > c_open[1] > c_close[1] > c_open[0] and c_open[2] > _average(c_open[1], c_close[1]) \
            and c_open[2] > c_close[2] and c_close[2] < c_open[0]:
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
    if c_open[0] < c_close[0] < c_close[1] < c_open[1] < c_open[2] and c_close[2] >= c_high[0]:
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
    if c_open[0] > c_close[0] and c_close[4] < c_open[1] < c_open[2] < c_close[1] < c_close[2] < c_open[3] < c_close[3] \
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
            and c_high[2] > c_high[3] and abs(first - sec) < tolerance and abs(sec - third) < tolerance:
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


def in_neck_line_bullish(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[1] < c_close[0] <= c_close[1] < c_open[1] and abs(c_open[0] - c_close[0]) > abs(c_open[1] - c_close[1]):
        return True
    else:
        return False


def in_neck_line_bearish(candles):
    # work with at least 2 candle and return True if pattern be true
    c_open, c_high, c_close, c_low = _last_limit_data(candles, 2)
    if c_open[1] > c_close[0] >= c_close[1] > c_open[1] and abs(c_open[0] - c_close[0]) > abs(c_open[1] - c_close[1]):
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


print(harami_cross_bearish(candle('BTCUSDT', '30m', 20)))
