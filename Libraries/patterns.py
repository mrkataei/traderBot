def _average(*inputs: float):
    result = 0.0
    for put in inputs:
        result += put
    return result / len(inputs)


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
