""""
Mr.Kataei 8/4/2021
This section run in other bot only use with admins project
for see details about users and recommendations
"""
import telebot
from Inc import db , functions
from time import sleep
from Account.clients import User
from Auth import login
import numpy as np
#@aranadminbot -> address
API_KEY = '1987746421:AAFjiQ22yuRXhzYOrRkVmeuuHM96sD4aqpA'
user_dict = {}
connection = db.con_db()
admins = np.array(functions.get_admins(connection))

def bot_polling():
    global bot
    print("Starting bot polling now")
    while True:
        try:
            print("New bot instance started")
            bot = telebot.TeleBot(API_KEY) #Generate new bot instance
            bot_actions() #If bot is used as a global variable, remove bot as an input param
            # broadcast_messages()
            bot.polling(none_stop=True, interval=2, timeout=30)
        except Exception as ex: #Error in polling
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(30, ex))
            bot.stop_polling()
            sleep(2)
        else: #Clean exit
            bot.stop_polling()
            print("Bot polling loop finished")
            break #End loop


def bot_actions():
    # /start command enter by admin
    @bot.message_handler(commands=['start'])
    def welcome(message):
        if not message.chat.id in user_dict :
            #welcome message and instructions
            bot.reply_to(message, "Hey " + message.chat.first_name + "!\n")
            #the markup help us we have call back with inlinekeyboard when yours tap one of those
            #some callback data send and we receive with @bot.callback_query_handler
            step_kb = telebot.types.InlineKeyboardMarkup()
            step_kb.add(telebot.types.InlineKeyboardButton('🔑Login', callback_data='login'))
            bot.send_message(chat_id=message.chat.id,text='Welcome Admin!\nPlease login',reply_markup=step_kb)
    #after callback @bot.callback_query_handler get function parameter ,this always true
    #and w8 to one case login and reg and .. happened . need to develop func in parameter
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
            if message.text in admins :
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
    #if session assign True user login ,if any exception happened -
    # start again with /start and object user removed
    def process_password(message):
        try:
            user = user_dict[message.chat.id]
            res = login.login(db_connection=connection , username=user.username , password=message.text)
            if res[0]:
                bot.delete_message(message.chat.id , message.message_id)
                bot.send_message(message.chat.id , res[1])
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
        if not message.chat.id in user_dict:
            bot.reply_to(message, 'Please login /start')
        elif not user_dict[message.chat.id].session:
            bot.reply_to(message, 'Please login /start')
        else:
            usernames = ''
            users = np.array(functions.get_usernames(connection))
            for index, user in enumerate(users, start=1):
                usernames += str(index) + '-' + str(user[0]) + ' ,'
            bot.reply_to(message, usernames)