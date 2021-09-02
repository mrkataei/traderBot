""""
Mr.Kataei 8/4/2021
This section run in other bot only use with admins project
for see details about users and recommendations
"""
import telebot
from Inc import db, functions
from Account.clients import User
import numpy as np
import subprocess
from Interfaces.telegram import Telegram

# @aranadminbot -> address
# API_KEY = '1987746421:AAFjiQ22yuRXhzYOrRkVmeuuHM96sD4aqpA'
# test bot fro admin
API_KEY = '1991184876:AAGfWUbxXEbnbWHeKrlh2knooi8lF1PSWKI'


class AdminBot(Telegram):
    def __init__(self):
        Telegram.__init__(self, API_KEY=API_KEY)
        __connection = db.con_db()
        self.admins = np.array(functions.get_admins(__connection))

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
                connection = db.con_db()
                usernames = ''
                users = np.array(functions.get_usernames(connection))
                for index, user in enumerate(users, start=1):
                    usernames += str(index) + '-' + str(user[0]) + ' ,'
                self.bot.reply_to(message, usernames)

        @self.bot.message_handler(commands=['detail'])
        def show_users(message):
            if self.check_login(message):
                self.bot.reply_to(message, "Enter username")
                self.bot.register_next_step_handler(message, process_user_details)

        def process_user_details(message):
            try:
                connection = db.con_db()
                # ('username', timestamp, 'role', assets, timeframe, analysis_is)
                qu = functions.get_user_details(connection, message.text)[0]
                analysis = functions.get_analysis(connection, qu[5])[0][0] if qu[5] else "No analysis"
                timeframe = functions.get_timeframe(connection, qu[4])[0][0]
                coins = functions.get_user_coins(connection, qu[0])
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
                result = subprocess.check_output('ps aux --sort -rss | grep main.py | head -n 1', shell=True)
                self.bot.reply_to(message, result)

        # @bot.message_handler(commands=['restart'])
        # def show_users(message):
        #     if message.chat.id not in user_dict:
        #         bot.reply_to(message, 'Please login /start')
        #     elif not user_dict[message.chat.id].session:
        #         bot.reply_to(message, 'Please login /start')
        #     else:
        #         bot.reply_to(message, "Enter PID process")
        #         bot.register_next_step_handler(message, process_restart_bot)
        #
        # def process_restart_bot(message):
        #     try:
        #         os.system(f'kill {message.text}')
        #         os.system("nohup python3 main.py &")
        #         bot.reply_to(message, "Done!\n /ps to watch process")
        #     except Exception as e:
        #         bot.reply_to(message, 'Something wrong please try again!')

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
