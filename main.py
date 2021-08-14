from Telegram import tele
import threading
from Inc import db ,functions
from time import sleep
import telebot
import asyncio
from Analysis import ichimoku

connection = db.con_db()
API_KEY = '1936293973:AAFLKY0TCP9qEMjqPDrewsdzGisNSQmB0ds'
bot = telebot.TeleBot(API_KEY)

def broadcast_messages():
    users = functions.get_user_recommendation(connection, coin_id=1,
                                              analysis_id=1, timeframe_id=1)
    for user in users:
        bot.send_message(chat_id=int(functions.get_user_chat_id(connection , user[0]) ), text="salam")
def signal():
    while True:
        functions.set_recommendation(connection, 1, 1, 1, "sell", 2500, 2300, 2, "high")
        broadcast_messages()
        sleep(20)

polling_thread = threading.Thread(target=tele.bot_polling)
polling_thread.daemon = True
polling_thread.start()
polling_thread3 = threading.Thread(target=signal)
polling_thread3.daemon = True
polling_thread3.start()

if __name__ == '__main__':
    while True:
        print("connected")
        sleep(200)
