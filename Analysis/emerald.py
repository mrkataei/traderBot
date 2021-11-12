"""
Mr.Kataei 11/12/2021
"""
import pandas as pd
from Libraries.patterns import *
from Libraries.patterns import last_limit_data as last
from Inc.functions import get_recommendations, set_recommendation
from Telegram.Client.message import broadcast_messages
import datetime


def signal(data: pd.DataFrame, gain: float, cost: float, coin_id: int, timeframe_id: int, bot_ins,
            symbol: str, timeframe: str):
    print(str(datetime.datetime.now()), "emerald checking ..." + symbol, timeframe)
    c2_open, c2_high, c2_close, c2_low = last(candles=data, limit=2)
    c3_open, c3_high, c3_close, c3_low = last(candles=data, limit=3)
    c4_open, c4_high, c4_close, c4_low = last(candles=data, limit=4)
    c5_open, c5_high, c5_close, c5_low = last(candles=data, limit=5)
    try:
        query = get_recommendations(analysis_id=1, timeframe_id=timeframe_id, coin_id=coin_id)
        old_position = query[0][2]
        # when no rows in database
    except Exception as e:
        old_position = 'sell'
        # print(e)

    def check():
        if hammer(c_open=c2_open, c_high=c2_high, c_close=c2_close, c_low=c2_low) \
                or inverted_hammer(c_open=c3_open, c_high=c3_high, c_close=c3_close, c_low=c3_low) \
                or belt_hold_bullish(c_open=c2_open, c_close=c2_close, c_low=c2_low, tolerance=0.05) \
                or engulfing_bullish(c_open=c3_open, c_high=c3_high, c_close=c3_low, c_low=c3_low) \
                or harami_bullish(c_open=c3_open, c_high=c3_high, c_close=c3_close, c_low=c3_low) \
                or harami_cross_bullish(c_open=c2_open, c_high=c2_high, c_close=c2_close, c_low=c2_low) \
                or piercing_line(c_open=c3_open, c_close=c3_close, c_low=c3_low) \
                or doji_star_bullish(c_open=c2_open, c_high=c2_high, c_close=c2_close, limit=20) \
                or meeting_line_bullish(c_open=c3_open, c_high=c3_high, c_close=c3_close, tolerance=0.05) \
                or three_white_soldiers(c_open=c4_open, c_high=c4_high, c_close=c4_close) \
                or morning_star(c_open=c4_open, c_close=c4_close) \
                or morning_doji_star(c_open=c3_open, c_close=c3_close, c_low=c3_low, limit=20) \
                or abandoned_baby_bullish(c_open=c3_open, c_high=c3_high, c_close=c3_close, limit=20) \
                or tri_star_bullish(c_open=c3_open, c_close=c3_close, limit=20) \
                or breakaway_bullish(c_open=c5_open, c_close=c5_close) \
                or three_inside_up(c_open=c3_open, c_close=c3_close, c_low=c3_low) \
                or three_outside_up(c_open=c3_open, c_close=c3_close) \
                or kicking_bullish(c_open=c2_open, c_high=c2_high, c_close=c2_close, c_low=c2_low, tolerance=0.05) \
                or three_stars_in_the_south(c_open=c4_open, c_high=c4_high, c_close=c4_close,
                                            c_low=c4_low, tolerance=0.05) \
                or concealing_baby(c_open=c4_open, c_high=c4_high, c_close=c4_close) \
                or stick_sandwich(c_open=c3_open, c_close=c3_close, tolerance=0.05) \
                or matching_low(c_open=c2_open, c_high=c2_high, c_close=c2_close) \
                or homing_pigeon(c_open=c2_open, c_high=c2_high, c_close=c2_close, c_low=c2_low) \
                or ladder_bottom(c_open=c5_open, c_close=c5_close, c_low=c5_low) \
                or separating_lines_bullish(c_open=c2_open, c_high=c2_high, c_close=c2_close,
                                            c_low=c2_low, tolerance=0.05) \
                or rising_three_methods(c_open=c4_open, c_high=c4_high, c_close=c4_close, c_low=c4_low) \
                or upside_tasuki_gap(c_open=c3_open, c_close=c3_close) \
                or sidebyside_white_lines_bullish(c_open=c3_open, c_high=c3_high, c_close=c3_close, c_low=c3_low) \
                or three_line_strike_bullish(c_open=c4_open, c_high=c4_high, c_close=c4_close, tolerance=0.05) \
                or upside_gap_three_methods(c_open=c3_open, c_high=c3_high, c_close=c3_close, c_low=c3_low) \
                or on_neck_line_bullish(c_open=c2_open, c_high=c2_high, c_close=c2_close,
                                        c_low=c2_low, tolerance=0.05) \
                or in_neck_line_bullish(c_open=c2_open, c_close=c2_close):

            return True

        elif hanging_man(c_open=c2_open, c_high=c2_high, c_close=c2_close, c_low=c2_low) \
                or shooting_star(c_open=c2_open, c_high=c2_high, c_close=c2_close) \
                or belt_hold_bearish(c_open=c2_open, c_high=c2_high, c_close=c2_close, tolerance=0.05) \
                or engulfing_bearish(c_open=c3_open, c_high=c3_high, c_close=c3_close, c_low=c3_low) \
                or harami_bearish(c_open=c3_open, c_high=c3_high, c_close=c3_close, c_low=c3_low) \
                or harami_cross_bearish(c_open=c2_open, c_high=c2_high, c_close=c2_close, c_low=c2_low) \
                or dark_cloud_cover(c_open=c3_open, c_high=c3_high, c_close=c3_close) \
                or doji_star_bearish(c_open=c2_open, c_close=c2_close) \
                or meeting_line_bearish(c_open=c3_open, c_close=c3_close, c_low=c3_low, tolerance=0.05) \
                or three_black_crows(c_open=c4_open, c_close=c4_close, c_low=c4_low) \
                or evening_star(c_open=c4_open, c_close=c4_close) \
                or evening_doji_star(c_open=c3_open, c_high=c3_high, c_close=c3_close, limit=20) \
                or abandoned_baby_bearish(c_open=c3_open, c_high=c3_high, c_close=c3_close, limit=20) \
                or tri_star_bearish(c_open=c3_open, c_close=c3_close, limit=20) \
                or three_inside_down(c_open=c3_open, c_close=c3_close) \
                or three_outside_down(c_open=c3_open, c_high=c3_high, c_close=c3_close) \
                or kicking_bearish(c_open=c2_open, c_high=c2_high, c_close=c2_close, c_low=c2_low, tolerance=0.05) \
                or loentical_three_cross(c_open=c3_open, c_close=c3_close) \
                or deliberation(c_open=c3_open, c_close=c3_close, c_low=c3_low) \
                or matching_high(c_open=c2_open, c_close=c2_close, c_low=c2_low) \
                or upside_gap_two_crows(c_open=c3_open, c_high=c3_high, c_close=c3_close) \
                or advance_block(c_open=c3_open, c_high=c3_high, c_close=c3_close, c_low=c3_low) \
                or two_crows(c_open=c3_open, c_high=c3_high, c_close=c3_close, c_low=c3_low) \
                or separating_lines_bearish(c_open=c2_open, c_high=c2_high, c_close=c2_close,
                                            c_low=c2_low, tolerance=0.005) \
                or falling_three_methods(c_open=c5_open, c_close=c5_close, c_low=c5_low) \
                or downside_tasuki_gap(c_open=c3_open, c_close=c3_close) \
                or sidebyside_white_lines_bearish(c_open=c3_open, c_high=c3_high, c_close=c3_close, c_low=c3_low) \
                or three_line_strike_bearish(c_open=c4_open, c_high=c4_high, c_close=c4_close, tolerance=0.05) \
                or downside_gap_three_methods(c_open=c3_open, c_high=c3_high, c_close=c3_close, c_low=c3_low)\
                or on_neck_line_bearish(c_open=c2_open, c_close=c2_close, c_low=c2_low) \
                or in_neck_line_bearish(c_open=c2_open, c_close=c2_close) \
                or breakaway_bearish(c_open=c5_open, c_close=c5_close):
            return False
        else:
            return None

    result = check()
    if result is not None:
        close = float(data.tail(1)['close'].values[0])
        target_price = close * gain + close if result else -close * gain + close
        position = 'buy' if result else 'sell'
        if old_position != position:
            set_recommendation(analysis_id=1, coin_id=coin_id, timeframe_id=timeframe_id, position=position,
                                     target_price=target_price, current_price=close, cost_price=cost, risk='low')
            broadcast_messages(coin_id=coin_id, analysis_id=1, timeframe_id=timeframe_id, position=position,
                               target_price=target_price, current_price=close, risk='low', bot_ins=bot_ins)
