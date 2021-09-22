"""
Mr.Kataei 8/15/2021

"""
import telebot
from mysql.connector import MySQLConnection
from Inc import functions
from Libraries.definitions import *

# from decouple import config

# API_KEY = config('API_KEY')
# master bot already run on vps dont use this @algowatchbot -> address
API_KEY = '1987308624:AAEow3hvRGt4w6ZFmz3bYaQz1J8p-OzRer0'
# @testkourosh2bot -> address // use this bot for test your code
#API_KEY = '1978536410:AAE_RMk3-4r_cLnt_nRcEnZHaSp-vIk9oVo'


def broadcast_messages(connection: MySQLConnection, coin_id: int, analysis_id: int, timeframe_id: int,
                       position: str, target_price: float, current_price: float, risk: str):
    users = functions.get_user_recommendation(connection, coin_id=coin_id,
                                              analysis_id=analysis_id, timeframe_id=timeframe_id)
    coin = functions.get_coin_name(connection, coin_id)
    analysis = functions.get_analysis(connection, analysis_id)
    timeframe = functions.get_timeframe(connection, timeframe_id)
    bot = telebot.TeleBot(API_KEY)
    for user in users:
        message = f'👋🏼 {trans("C_hello")} {user[0]}!\n💥{trans("M_new_signal")}*{analysis[0][0]}*!!!\n' \
                  f'*{coin}* {trans("C_now")} {trans("M_in")} *{position}* {trans("M_position")}\n' \
                  f'{trans("M_current_price")}: {current_price}$\n' \
                  f'{trans("M_target_price")}: {target_price}$\n' \
                  f'{trans("M_risk")}: *{risk}*\n' \
                  f'{trans("C_timeframe")}: {timeframe[0][0]}'
        try:
            bot.send_message(chat_id=int(functions.get_user_chat_id(connection, user[0])), text=message,
                             parse_mode='Markdown')
        except Exception as e:
            print(e)
    del bot


def admin_broadcast(message: str, chat_ids):
    bot = telebot.TeleBot(API_KEY)
    try:
        for chat_id in chat_ids:
            print(int(chat_id[0]))
            bot.send_message(chat_id=int(chat_id[0]), text=message)
    except Exception as e:
        print(e)
    del bot


def admin_send_message(message: str, chat_id):
    bot = telebot.TeleBot(API_KEY)
    bot.send_message(chat_id=int(chat_id), text=message)
    del bot

# test
