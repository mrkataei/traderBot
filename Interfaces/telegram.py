import telebot
from time import sleep
from Inc import db, functions
from Auth import login
import numpy as np
from Libraries.definitions import *


class Telegram:
    def __init__(self, API_KEY: str):
        self.API_KEY = API_KEY
        self.bot = None
        self.user_dict = {}
        self.reg_dict = {}
        __connection = db.con_db()
        self.coins_list = np.array(functions.get_coins(__connection))
        self.timeframes_list = np.array(functions.get_timeframe(__connection))
        self.analysis_list = np.array(functions.get_analysis(__connection))

    def bot_polling(self):
        print("Starting bot polling now")
        while True:
            try:
                print("New bot instance started")
                self.bot = telebot.TeleBot(self.API_KEY)  # Generate new bot instance
                self.bot_actions()  # If bot is used as a global variable, remove bot as an input param
                self.bot.polling(none_stop=True, interval=2, timeout=30)
            except Exception as ex:  # Error in polling
                print("Bot polling failed, restarting in {}sec. Error:\n{}".format(30, ex))
                self.bot.stop_polling()
                sleep(2)
            else:  # Clean exit
                self.bot.stop_polling()
                print("Bot polling loop finished")
                break  # End loop

    def bot_actions(self):
        raise Exception("NotImplementedException")

    def process_password(self, message):
        try:
            connection = db.con_db()
            user = self.user_dict[message.chat.id]
            res = login.login(db_connection=connection, username=user.username, password=message.text)
            if res[0]:
                self.bot.delete_message(message.chat.id, message.message_id)
                self.bot.send_message(message.chat.id, res[1])
                user.session = True
                del connection
                print(self.user_dict)
            else:
                self.bot.send_message(message.chat.id, res[1])
                # del self.user_dict[message.chat.id]
        except Exception as e:
            self.bot.reply_to(message, trans('C_please_start'))
            print(e)
            # del self.user_dict[message.chat.id]

    def process_login_username(self, message):
        try:
            user = self.user_dict[message.chat.id]
            user.username = message.text
            # get password with process_password and register_next_step_handler
            # to handle next enter user's message
            msg = self.bot.reply_to(message, trans('C_enter_password'))
            self.bot.register_next_step_handler(msg, self.process_password)
        # some exception need develop
        except Exception as e:
            self.bot.reply_to(message, trans('C_please_start'))
            del self.user_dict[message.chat.id]
            print(e)

    def check_login(self, message):
        if message.chat.id not in self.user_dict:
            self.bot.reply_to(message, trans('C_please_start'))
            return False
        elif not self.user_dict[message.chat.id].session:
            self.bot.reply_to(message, trans('C_please_start'))
            return False
        else:
            return True
