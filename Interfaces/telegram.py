import telebot
from time import sleep
from Inc import functions
from Auth import login
import numpy as np
from Libraries.definitions import *


class Telegram:
    def __init__(self, API_KEY: str = '1987308624:AAEow3hvRGt4w6ZFmz3bYaQz1J8p-OzRer0'):
        self.API_KEY = API_KEY
        self.bot = None
        self.user_dict = {}
        self.reg_dict = {}
        (__connection, __cursor) = functions.get_connection_and_cursor()
        self.coins_list = np.array(functions.get_coins())
        self.timeframes_list = np.array(functions.get_timeframe())
        self.analysis_list = np.array(functions.get_analysis())

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
            user = self.user_dict[message.chat.id]
            res = login.login(username=user.username, password=message.text)
            if res[0]:
                self.bot.delete_message(message.chat.id, message.message_id)
                self.bot.send_message(message.chat.id, res[1])
                user.session = True
                user.login = True
                # our client deleted his/her account and chat id not updated
                # this statement after login update his/her chat id
                if not functions.check_chat_id(message.chat.id):
                    functions.update_chat_id(username=user.username, chat_id=message.chat.id)
                print(self.user_dict)
            else:
                self.bot.send_message(message.chat.id, res[1])
                user.session = False
                # del self.user_dict[message.chat.id]
        except Exception as e:
            self.bot.reply_to(message, trans('C_please_start'))
            print(e)
            # del self.user_dict[message.chat.id]

    def easy_login(self, message):
        try:
            check = functions.check_chat_id(chat_id=message.chat.id)
            user = self.user_dict[message.chat.id]
            if check:
                user.username = check
                user.login = True
                self.bot.reply_to(message, trans('L_successful_login'))
            else:
                self.bot.reply_to(message, trans('L_something_wrong'))
                user.session = False
        # some exception need develop
        except Exception as e:
            self.bot.reply_to(message, trans('C_please_start'))
            del self.user_dict[message.chat.id]
            print(e)

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
            self.bot.reply_to(message, trans('C_start'))
            return False
        elif self.user_dict[message.chat.id].login:
            return True
        else:
            self.bot.reply_to(message, trans('C_please_login'))
            return False

    def keyboard(self, message):
        key_markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
        key_add = telebot.types.KeyboardButton(trans('C_add_keyboard'))
        key_new = telebot.types.KeyboardButton(trans('C_new_keyboard'))
        key_frame = telebot.types.KeyboardButton(trans('C_frame_keyboard'))
        key_analysis = telebot.types.KeyboardButton(trans('C_analysis_keyboard'))
        key_candle = telebot.types.KeyboardButton(trans('C_candle_keyboard'))
        key_show = telebot.types.KeyboardButton(trans('C_show_keyboard'))
        key_recommendation = telebot.types.KeyboardButton(trans('C_recommendation_keyboard'))
        key_remove = telebot.types.KeyboardButton(trans('C_remove_keyboard'))
        key_logout = telebot.types.KeyboardButton(trans('C_logout_keyboard'))
        key_help = telebot.types.KeyboardButton(trans('C_help_keyboard'))
        key_markup.add(key_add, key_new, key_frame, key_analysis, key_candle, key_show, key_recommendation,
                       key_remove, key_logout, key_help)
        self.bot.send_message(message.chat.id, trans('C_what_can_i_do'), reply_markup=key_markup)
