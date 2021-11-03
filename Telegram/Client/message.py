"""
Mr.Kataei 8/15/2021

"""
from Inc.functions import get_user_recommendation, get_coin_name, get_analysis, get_timeframe, get_user_chat_id
from Libraries.definitions import *


def broadcast_messages(coin_id: int, analysis_id: int, timeframe_id: int, position: str, target_price: float,
                       current_price: float, risk: str, bot_ins):
    users = get_user_recommendation(coin_id=coin_id, analysis_id=analysis_id)
    coin = get_coin_name(coin_id)
    analysis = get_analysis(analysis_id)
    timeframe = get_timeframe(timeframe_id)
    for user in users:
        message = f'👋🏼 {trans("C_hello")} {user[0]}!\n💥{trans("M_new_signal")}*{analysis[0][0]}*!!!\n' \
                  f'*{coin}* {trans("C_now")} {trans("M_in")} *{position}* {trans("M_position")}\n' \
                  f'{trans("M_current_price")}: {current_price}$\n' \
                  f'{trans("M_target_price")}: {target_price}$\n' \
                  f'{trans("M_risk")}: *{risk}*\n' \
                  f'{trans("C_timeframe")}: {timeframe[0][0]}'
        try:
            bot_ins.send_message(chat_id=int(get_user_chat_id(user[0])), text=message,
                                 parse_mode='Markdown')
        except Exception as e:
            print(e)


def admin_broadcast(message: str, chat_ids, bot_ins):
    for chat_id in chat_ids:
        try:
            bot_ins.send_message(chat_id=int(chat_id[0]), text=message)
        except Exception as e:
            print(e)
            continue


def admin_send_message(message: str, chat_id, bot_ins):
    bot_ins.send_message(chat_id=int(chat_id), text=message)
