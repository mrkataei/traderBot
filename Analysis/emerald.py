"""
Arman hajimirza & Mr.Kataei

database configure :
        coin_id -> 1=BTCUSDT , 2=ETHUSDT
        timeframe_id -> 1=30min , 2=1hour ,3=4hour ,4=1day
        analysis_id -> 1=ichimoku
use this query for get user who have this signal with this coin and time:
        users = functions.get_user_recommendation(connection, coin_id=1,analysis_id=1, timeframe_id=1)
and get chat_id for notify them with this query :
        chat_id = functions.get_user_chat_id(connection , user[0])
all of this in Telegram/message just use broadcast method
for insert new signal :
        functions.set_recommendation(connection, 1, 1, 1, "sell", 2500, 2300, 2, "high")
        broadcast_message(*args)
"""
import pandas as pd
from Libraries.patterns import *
from Inc.functions import get_recommendations, set_recommendation
from Telegram.Client.message import broadcast_messages
import datetime


def signal(data: pd.DataFrame, gain: float, cost: float, coin_id: int, timeframe_id: int, bot_ins,
            symbol: str, timeframe: str):
    print(str(datetime.datetime.now()), "emerald checking ..." + symbol, timeframe)
    try:
        query = get_recommendations(analysis_id=1, timeframe_id=timeframe_id, coin_id=coin_id)
        old_position = query[0][2]
        # when no rows in database
    except Exception as e:
        old_position = 'sell'
        # print(e)

    def check():
        if hammer(data) or inverted_hammer(data) or belt_hold_bullish(data, 0.05) or engulfing_bullish(data) \
                or harami_bullish(data) or harami_cross_bullish(data) or piercing_line(data) \
                or doji_star_bullish(data, 20) or meeting_line_bullish(data, 0.05) or three_white_soldiers(data) \
                or morning_star(data) or morning_doji_star(data, 20) or abandoned_baby_bullish(data, 20) \
                or tri_star_bullish(data, 20) or breakaway_bullish(data) or three_inside_up(data) \
                or three_outside_up(data) or kicking_bullish(data, 0.05) or three_stars_in_the_south(data, 0.05) \
                or concealing_baby(data) or stick_sandwich(data, 0.05) or matching_low(data) or homing_pigeon(data) \
                or ladder_bottom(data) or separating_lines_bullish(data, 0.05) or rising_three_methods(data) \
                or upside_tasuki_gap(data) or sidebyside_white_lines_bullish(data) \
                or three_line_strike_bullish(data, 0.05) or upside_gap_three_methods(data) \
                or on_neck_line_bullish(data, 0.05) or in_neck_line_bullish(data):
            return True
        elif hanging_man(data) or shooting_star(data) or belt_hold_bearish(data, 0.05) or engulfing_bearish(data) \
                or harami_bearish(data) or harami_cross_bearish(data) or dark_cloud_cover(data) \
                or doji_star_bearish(data) or meeting_line_bearish(data, 0.05) or three_black_crows(data) \
                or evening_star(data) or evening_doji_star(data, 20) or abandoned_baby_bearish(data, 20) \
                or tri_star_bearish(data, 20) or three_inside_down(data) or three_outside_down(data) \
                or kicking_bearish(data, 0.05) or loentical_three_cross(data) or deliberation(data) \
                or matching_high(data) or upside_gap_two_crows(data) or advance_block(data) or two_crows(data) \
                or separating_lines_bearish(data, 0.05) or falling_three_methods(data) or downside_tasuki_gap(data) \
                or sidebyside_white_lines_bearish(data) or three_line_strike_bearish(data, 0.05) \
                or on_neck_line_bearish(data) or in_neck_line_bearish(data):
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
