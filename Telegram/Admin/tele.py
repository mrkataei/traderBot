""""
Mr.Kataei 8/4/2021
This section run in other bot only use with admins project
for see details about users and recommendations
"""
import os
import telebot
from Inc import functions
from Account.clients import User
import numpy as np
import subprocess
from Interfaces.telegram import Telegram
from Telegram.Client.message import admin_broadcast, admin_send_message

# @aranadminbot -> address
API_KEY = '1987746421:AAFjiQ22yuRXhzYOrRkVmeuuHM96sD4aqpA'
# test bot fro admin
# API_KEY = '1991184876:AAGfWUbxXEbnbWHeKrlh2knooi8lF1PSWKI'
# algowatch original API
API_KEY_MESSAGE = '1987308624:AAEow3hvRGt4w6ZFmz3bYaQz1J8p-OzRer0'
# test API
# API_KEY_MESSAGE = '1978536410:AAE_RMk3-4r_cLnt_nRcEnZHaSp-vIk9oVo'
_bot_ins = telebot.TeleBot(API_KEY_MESSAGE)


class AdminBot(Telegram):
    def __init__(self):
        Telegram.__init__(self, API_KEY=API_KEY)
        self.admins = np.array(functions.get_admins())

    def bot_actions(self):
        # /start command enter by admin
        @self.bot.message_handler(commands=['start'])
        def welcome(message):
            if not self.check_login(message):
                # welcome message and instructions
                self.bot.reply_to(message, "Hey " + message.chat.first_name + "!\n")
                # the markup help us we have call back with inlinekeyboard when yours tap one of those
                # some callback data send and we receive with @bot.callback_query_handler
                step_kb = telebot.types.InlineKeyboardMarkup()
                step_kb.add(telebot.types.InlineKeyboardButton('🔑Login', callback_data='login'))
                self.bot.send_message(chat_id=message.chat.id, text='Welcome Admin!\nPlease login',
                                      reply_markup=step_kb)

        # after callback @bot.callback_query_handler get function parameter ,this always true
        # and w8 to one case login and reg and .. happened . need to develop func in parameter
        @self.bot.callback_query_handler(func=lambda call: True)
        def query_handler(call):
            if call.data == "login":
                # create object from user and store in our dictionary with chat_id key value
                user = User()
                self.user_dict[call.message.chat.id] = user
                self.bot.reply_to(call.message, "🔑Enter your username")
                # handle next step message user enter after login
                self.bot.register_next_step_handler(call.message, callback=process_login_username)
            if "sure_question_" in call.data:
                user = self.user_dict[call.message.chat.id]
                msg = user.temp
                if str(call.data).split('_')[2] == "yes":
                    chat_ids = np.array(functions.get_chat_ids())
                    admin_broadcast(message=msg, chat_ids=chat_ids, bot_ins=_bot_ins)
                    self.bot.reply_to(call.message, "Done!\nyour message send to all")
                else:
                    self.bot.reply_to(call.message, "Deleted, try again /broadcast")
                user.temp = None

            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        """
                login handler
        """

        # get username and store in user dictionary (key:chat_id)
        def process_login_username(message):
            if message.text in self.admins:
                self.process_login_username(message)
            else:
                self.bot.reply_to(message, 'Invalid username')

        @self.bot.message_handler(commands=['users'])
        def show_users(message):
            if self.check_login(message):
                usernames = ''
                users = np.array(functions.get_usernames())
                for index, user in enumerate(users, start=1):
                    usernames += str(index) + '-' + str(user[0]) + ' ,'
                self.bot.reply_to(message, usernames)

        @self.bot.message_handler(commands=['message'])
        def show_users(message):
            if self.check_login(message):
                self.bot.reply_to(message, "Enter username")
                self.bot.register_next_step_handler(message, process_message_to_user_step1)

        def process_message_to_user_step1(message):
            self.bot.reply_to(message, "Enter your message")
            user = self.user_dict[message.chat.id]
            # id user in temp
            user.temp = message.text
            self.bot.register_next_step_handler(message, process_message_to_user_step2)

        def process_message_to_user_step2(message):
            user = self.user_dict[message.chat.id]
            try:
                chat_id = functions.get_user_chat_id(user.temp)
                admin_send_message(message=message.text, chat_id=chat_id, bot_ins=_bot_ins)
            except Exception as e:
                self.bot.reply_to(message, e)

        @self.bot.message_handler(commands=['log'])
        def show_users(message):
            if self.check_login(message):
                main_log = open('main.txt', 'r')
                admin_log = open('client.txt', 'r')
                client_log = open('admin.txt', 'r')
                self.bot.send_document(chat_id=message.chat.id, data=main_log)
                self.bot.send_document(chat_id=message.chat.id, data=admin_log)
                self.bot.send_document(chat_id=message.chat.id, data=client_log)

        @self.bot.message_handler(commands=['detail'])
        def show_users(message):
            if self.check_login(message):
                self.bot.reply_to(message, "Enter username")
                self.bot.register_next_step_handler(message, process_user_details)

        def process_user_details(message):
            try:
                # ('username', timestamp, 'role', assets, timeframe, analysis_is)
                qu = functions.get_user_details(message.text)[0]
                analysis = functions.get_analysis(qu[5])[0][0] if qu[5] else "No analysis"
                timeframe = functions.get_timeframe(qu[4])[0][0]
                coins = functions.get_user_coins(qu[0])
                res = f"Username:{qu[0]}\n" \
                      f"Join at:{qu[1]}\n" \
                      f"Assets:{qu[3]}\n" \
                      f"Role:{qu[2]}\n" \
                      f"Coins:{coins}\n" \
                      f"Analysis:{analysis}\n" \
                      f"Timeframe:{timeframe}"

                self.bot.reply_to(message, res)
            except Exception as e:
                self.bot.reply_to(message, 'Please try again')
                print(e)

        @self.bot.message_handler(commands=['ps'])
        def show_users(message):
            if self.check_login(message):
                result = subprocess.check_output('ps aux --sort -rss  | head -n 5', shell=True)
                self.bot.reply_to(message, result)

        @self.bot.message_handler(commands=['broadcast'])
        def show_users(message):
            if self.check_login(message):
                self.bot.reply_to(message, "Enter your message you want broadcast")
                self.bot.register_next_step_handler(message, process_broadcast)

        def process_broadcast(message):
            sure_question = telebot.types.InlineKeyboardMarkup()
            user = self.user_dict[message.chat.id]
            user.temp = message.text
            sure_question.add(telebot.types.InlineKeyboardButton('Ok, send it', callback_data="sure_question_yes"))
            sure_question.add(telebot.types.InlineKeyboardButton('Delete', callback_data="sure_question_no"))
            self.bot.send_message(chat_id=message.chat.id, text='Your message:\n' + message.text,
                                  reply_markup=sure_question)

        @self.bot.message_handler(commands=['restart'])
        def show_users(message):
            if message.chat.id not in self.user_dict:
                self.bot.reply_to(message, 'Please login /start')
            elif not self.user_dict[message.chat.id].session:
                self.bot.reply_to(message, 'Please login /start')
            else:
                self.bot.reply_to(message, "Enter PID process")
                self.bot.register_next_step_handler(message, process_restart_bot)

        def process_restart_bot(message):
            try:
                os.system(f'kill {int(message.text)}')
                os.system("cd /root/traderBot")
                os.system("nohup python3 -u main.py > main.txt &")
                self.bot.reply_to(message, "Done!\n /ps to watch process")
            except Exception as e:
                self.bot.reply_to(message, 'Something wrong please try again!')
                print(e)

        @self.bot.message_handler(commands=['logout'])
        def logout(message):
            if self.check_login(message):
                try:
                    self.user_dict[message.chat.id].session = False
                    self.bot.reply_to(message, '👋🏼Goodbye!\nFor login /start bot ')
                    del self.user_dict[message.chat.id]
                    print(self.user_dict)
                except Exception as e:
                    self.bot.reply_to(message, 'logout unsuccessful')
                    print(e)
