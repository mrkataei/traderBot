""""
Mr.Kataei 8/4/2021
This section run in other bot only use with admins project
for see details about users and recommendations
"""
import telebot
from Inc import db, functions
from time import sleep
from Account.clients import User
from Auth import login
import numpy as np
import os
import subprocess

# @aranadminbot -> address
# API_KEY = '1987746421:AAFjiQ22yuRXhzYOrRkVmeuuHM96sD4aqpA'
# test bot fro admin
API_KEY = '1991184876:AAGfWUbxXEbnbWHeKrlh2knooi8lF1PSWKI'
user_dict = {}
connection = db.con_db()
admins = np.array(functions.get_admins(connection))


def bot_polling():
    global bot
    print("Starting bot polling now")
    while True:
        try:
            print("New bot instance started")
            bot = telebot.TeleBot(API_KEY)  # Generate new bot instance
            bot_actions()  # If bot is used as a global variable, remove bot as an input param
            # broadcast_messages()
            bot.polling(none_stop=True, interval=2, timeout=30)
        except Exception as ex:  # Error in polling
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(30, ex))
            bot.stop_polling()
            sleep(2)
        else:  # Clean exit
            bot.stop_polling()
            print("Bot polling loop finished")
            break  # End loop


def bot_actions():
    # /start command enter by admin
    @bot.message_handler(commands=['start'])
    def welcome(message):
        if message.chat.id not in user_dict:
            # welcome message and instructions
            bot.reply_to(message, "Hey " + message.chat.first_name + "!\n")
            # the markup help us we have call back with inlinekeyboard when yours tap one of those
            # some callback data send and we receive with @bot.callback_query_handler
            step_kb = telebot.types.InlineKeyboardMarkup()
            step_kb.add(telebot.types.InlineKeyboardButton('🔑Login', callback_data='login'))
            bot.send_message(chat_id=message.chat.id, text='Welcome Admin!\nPlease login', reply_markup=step_kb)

    # after callback @bot.callback_query_handler get function parameter ,this always true
    # and w8 to one case login and reg and .. happened . need to develop func in parameter
    @bot.callback_query_handler(func=lambda call: True)
    def query_handler(call):
        if call.data == "login":
            # create object from user and store in our dictionary with chat_id key value
            user = User()
            user_dict[call.message.chat.id] = user
            bot.reply_to(call.message, "🔑Enter your username")
            # handle next step message user enter after login
            bot.register_next_step_handler(call.message, callback=process_login_username)

    """
            login handler
    """

    # get username and store in user dictionary (key:chat_id)
    def process_login_username(message):
        try:
            if message.text in admins:
                user = user_dict[message.chat.id]
                user.username = message.text
                # get password with process_password and register_next_step_handler
                # to handle next enter user's message
                msg = bot.reply_to(message, '🔒Enter your password')
                bot.register_next_step_handler(msg, process_password)
            else:
                bot.reply_to(message, 'Invalid username')
        # some exception need develop
        except Exception as e:
            bot.reply_to(message, 'Please /start bot again')
            del user_dict[message.chat.id]

    # if session assign True user login ,if any exception happened -
    # start again with /start and object user removed
    def process_password(message):
        try:
            connection = db.con_db()
            user = user_dict[message.chat.id]
            res = login.login(db_connection=connection, username=user.username, password=message.text)
            if res[0]:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, res[1])
                user.session = True
                print(user_dict)
            else:
                bot.send_message(message.chat.id, res[1])
                del user_dict[message.chat.id]
        except Exception as e:
            bot.reply_to(message, 'Please /start bot again')
            del user_dict[message.chat.id]

    @bot.message_handler(commands=['users'])
    def show_users(message):
        if message.chat.id not in user_dict:
            bot.reply_to(message, 'Please login /start')
        elif not user_dict[message.chat.id].session:
            bot.reply_to(message, 'Please login /start')
        else:
            connection = db.con_db()
            usernames = ''
            users = np.array(functions.get_usernames(connection))
            for index, user in enumerate(users, start=1):
                usernames += str(index) + '-' + str(user[0]) + ' ,'
            bot.reply_to(message, usernames)

    # @bot.message_handler(commands=['detail'])
    # def show_users(message):
    #     if message.chat.id not in user_dict:
    #         bot.reply_to(message, 'Please login /start')
    #     elif not user_dict[message.chat.id].session:
    #         bot.reply_to(message, 'Please login /start')
    #     else:
    #         bot.reply_to(message, "Enter username")
    #         bot.register_next_step_handler(message, process_user_details)
    #
    # def process_user_details(message):
    #     try:
    #         connection = db.con_db()
    #         # ('username', timestmp, 'role', assets, timeframe, analysis_is)
    #         qu = functions.get_user_details(connection, message.text)[0]
    #         analysis = functions.get_analysis(connection, qu[5])[0][0]
    #         timeframe = functions.get_timeframe(connection, qu[4])[0][0]
    #         coins = functions.get_user_coins(connection, qu[0])
    #         res = f"Username:{qu[0]}\n" \
    #               f"Join at:{qu[1]}\n" \
    #               f"Assets:{qu[3]}\n" \
    #               f"Role:{qu[2]}\n" \
    #               f"Coins:{coins}\n" \
    #               f"Analysis:{analysis}\n" \
    #               f"Timeframe:{timeframe}"
    #
    #         bot.reply_to(message, res)
    #     except Exception as e:
    #         bot.reply_to(message, 'Please try again')

    @bot.message_handler(commands=['ps'])
    def show_users(message):
        if message.chat.id not in user_dict:
            bot.reply_to(message, 'Please login /start')
        elif not user_dict[message.chat.id].session:
            bot.reply_to(message, 'Please login /start')
        else:
            result = subprocess.check_output('ps aux --sort -rss | grep main.py | head -n 1', shell=True)
            bot.reply_to(message, result)

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

    @bot.message_handler(commands=['logout'])
    def logout(message):
        if message.chat.id not in user_dict:
            bot.reply_to(message, '😪Please /start to login')
        # check user login
        elif user_dict[message.chat.id] and not user_dict[message.chat.id].session:
            bot.reply_to(message, '😪You are logged out')
        else:
            try:
                user_dict[message.chat.id].session = False
                bot.reply_to(message, '👋🏼Goodbye!\nFor login /start bot ')
                del user_dict[message.chat.id]
                print(user_dict)
            except Exception as e:
                bot.reply_to(message, 'logout unsuccessful')
