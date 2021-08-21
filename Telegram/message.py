"""
Mr.Kataei 8/15/2021

"""
import telebot
from mysql.connector import MySQLConnection
from Inc import functions
# from decouple import config

# API_KEY = config('API_KEY')
API_KEY = '1936293973:AAFLKY0TCP9qEMjqPDrewsdzGisNSQmB0ds'


def broadcast_messages(connection:MySQLConnection , coin_id:int , analysis_id:int , timeframe_id:int,
                       position:str , target_price:float , current_price:float , risk:str):
    users = functions.get_user_recommendation(connection, coin_id=coin_id,
                                              analysis_id=analysis_id, timeframe_id=timeframe_id)
    coin = functions.get_coin_name(connection , coin_id)
    analysis = functions.get_analysis(connection , analysis_id)
    timeframe = functions.get_timeframe(connection , timeframe_id)
    bot = telebot.TeleBot(API_KEY)
    for user in users:
        message = f'👋🏼 Hey {user[0]}!\n💥New received from *{analysis[0][0]}*!!!\n' \
                  f'*{coin}* now in *{position}* position\n' \
                  f'Current price: {current_price}$\n' \
                  f'Target price: {target_price}$\n' \
                  f'Risk: *{risk}*\n' \
                  f'Timeframe: {timeframe[0][0]}'
        bot.send_message(chat_id=int(functions.get_user_chat_id(connection , user[0]) ), text=message , parse_mode= 'Markdown')
    del bot