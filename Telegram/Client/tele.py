""""
Mr.Kataei 8/4/2021
for telebot library need token which father bot make for us , for now we define it ,
in static variable in future define and use in environment linux

this file have 2 class for store users already use bot 1-User , 2-Register
*User for all users that already sign up to system we store their chat_id and name and session
(session shows us user login or not)
*Register for all new users we store chat_id and username and 2 password and
security question and question id and answer for insert to database after insert the object remove for
avoid memory leak ,
"""
import telebot
from telebot import apihelper
from time import sleep
from Auth import login, register, reset_password
from Inc import db, functions
import numpy as np
from binance.client import Client
from Telegram.Client import candle
from Account.clients import User, Register
from Libraries.definitions import *

apihelper.ENABLE_MIDDLEWARE = True

# from decouple import config
# statics
# API_KEY = config('API_KEY', default='')

# API_KEY = config('API_KEY')
# master bot already run on vps dont use this @arantraderbot -> address
# API_KEY = '1936293973:AAFLKY0TCP9qEMjqPDrewsdzGisNSQmB0ds'
# @testkourosh2bot -> address // use this bot for test your code
API_KEY = '1978536410:AAE_RMk3-4r_cLnt_nRcEnZHaSp-vIk9oVo'

client = Client()
connection = db.con_db()
user_dict = {}
reg_dict = {}
coins_list = np.array(functions.get_coins(connection))
timeframes_list = np.array(functions.get_timeframe(connection))
analysis_list = np.array(functions.get_analysis(connection))


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


# need more develop on classes

def bot_actions():
    @bot.middleware_handler(update_types=['message'])
    def activate_language(bot_instance, message):
        activate(message.from_user.language_code)

    # /start command enter by user
    @bot.message_handler(commands=['start'])
    def welcome(message):
        if message.chat.id not in user_dict:
            # some action with delay to typing bot
            bot.send_chat_action(chat_id=message.chat.id, action="typing")
            sleep(1)
            # welcome message and instructions
            bot.reply_to(message, trans('C_hello') + message.chat.first_name + "!\n" + trans('C_welcome'))
            # the markup help us we have call back with inlinekeyboard when yours tap one of those
            # some callback data send and we receive with @bot.callback_query_handler
            step_kb = telebot.types.InlineKeyboardMarkup()
            step_kb.add(telebot.types.InlineKeyboardButton(trans('C_login'), callback_data='login'))
            step_kb.add(telebot.types.InlineKeyboardButton(trans('C_register'), callback_data='reg'))
            step_kb.add(telebot.types.InlineKeyboardButton(trans('C_forget_password'), callback_data='forget'))
            bot.send_message(chat_id=message.chat.id, text=trans('C_any_account'), reply_markup=step_kb)

    # after callback @bot.callback_query_handler get function parameter ,this always true
    # and w8 to one case login and reg and .. happened . need to develop func in parameter
    @bot.callback_query_handler(func=lambda call: True)
    def query_handler(call):
        if call.data == "login":
            # create object from user and store in our dictionary with chat_id key value
            user = User()
            user_dict[call.message.chat.id] = user
            bot.reply_to(call.message, trans('C_enter_username'))
            # handle next step message user enter after login
            bot.register_next_step_handler(call.message, callback=process_login_username)
        if call.data == "reg":
            if functions.check_chat_id(connection, call.message.chat.id):
                # create object from user and store in our dictionary with chat_id key value
                user = Register(call.message.chat.id)
                reg_dict[call.message.chat.id] = user
                bot.reply_to(call.message, trans('C_enter_username'))
                # handle next step message user enter after sign up
                bot.register_next_step_handler(call.message, callback=process_reg_username)
            else:
                username = functions.get_user_with_chat_id(connection, call.message.chat.id)
                bot.reply_to(call.message,
                             trans('C_already_have_account') + f" {username} \n" + trans('C_please_start'))
        if call.data == "1" or call.data == "2":
            # in other keyboard we need calls back from user choose which one question
            user = reg_dict[call.message.chat.id]
            # store in our object
            user.security_question_id = int(call.data)
            bot.reply_to(call.message, trans('C_enter_answer'))
            # handle next step message user enter after choose question
            bot.register_next_step_handler(call.message, callback=process_reg_answer)
        if call.data == "forget":
            # create object from user and store in our dictionary with chat_id key value
            user = Register(call.message.chat.id)
            reg_dict[call.message.chat.id] = user
            bot.reply_to(call.message, trans('C_enter_username'))
            # handle next step message user enter after forget password
            bot.register_next_step_handler(call.message, callback=process_forget_username)
        if call.data == "watchlist":
            coin_keyboard = telebot.types.InlineKeyboardMarkup()
            for index, coin in coins_list:
                coin_keyboard.add(telebot.types.InlineKeyboardButton(coin, callback_data=coin))
            bot.send_message(chat_id=call.message.chat.id, text=trans('C_select_coin'), reply_markup=coin_keyboard)

        # need more develop
        if call.data in coins_list[:, 1]:
            coin = coins_list[np.where(coins_list[:, 1] == call.data)][0][0]
            # for coins in coins[:1]:
            user = user_dict[call.message.chat.id]
            if not functions.set_coin(connection, user.username, coin, user.watchlist[0][2])[0]:
                bot.reply_to(call.message, trans('C_coin_already_exist'))
            else:
                bot.reply_to(call.message, trans('C_done') + "\n"
                             + trans('C_default_timeframe') + "\n" + trans('C_change_timeframe'))

        if call.data in timeframes_list[:, 1]:
            time_id = timeframes_list[np.where(timeframes_list[:, 1] == call.data)][0][0]
            time = timeframes_list[np.where(timeframes_list[:, 1] == call.data)][0][1]
            # for coins in coins[:1]:
            user = user_dict[call.message.chat.id]
            functions.update_timeframe(connection, user.username, time_id)
            bot.reply_to(call.message, trans('C_done') + time + trans('C_timeframe_changed'))

        if call.data in analysis_list[:, 1]:
            user = user_dict[call.message.chat.id]
            analysis_id = analysis_list[np.where(analysis_list[:, 1] == call.data)][0][0]
            functions.set_user_analysis(connection, user.username, int(analysis_id))
            bot.reply_to(call.message, trans('C_done') + "\n" + trans('C_now') + call.data + trans('C_working_for_you'))
        if call.data == "remove_watchlist":
            user = user_dict[call.message.chat.id]
            user.watchlist = functions.get_user_watchlist(connection, user.username)
            if user.watchlist:
                watchlist_remove = telebot.types.InlineKeyboardMarkup()
                # for watch in user.watchlist :
                user.temp_watch = user.watchlist[0][2]
                watchlist_remove.add(
                    telebot.types.InlineKeyboardButton(user.watchlist[0][2], callback_data='watchlist_remove_step2'))
                bot.send_message(chat_id=call.message.chat.id, text=trans('C_select_watchlist'),
                                 reply_markup=watchlist_remove)
            else:
                bot.reply_to(call.message, trans('C_null_watchlist'))
        if call.data == "watchlist_remove_step2":
            user = user_dict[call.message.chat.id]
            functions.delete_watchlist(connection, user.username, user.temp_watch)
            bot.reply_to(call.message, trans('C_done') + '\n' + trans('C_create_watchlist'))

        if call.data == "remove_coins":
            user = user_dict[call.message.chat.id]
            user.watchlist = functions.get_user_watchlist(connection, user.username)
            if user.watchlist:
                if functions.get_empty_coins_remain(connection, user.username, user.watchlist[0][2]) == 2:
                    bot.reply_to(call.message, trans('C_null_coin'))
                else:
                    watchlist_remove = telebot.types.InlineKeyboardMarkup()
                    # for watch in user.watchlist :
                    user.temp_watch = user.watchlist[0][2]
                    watchlist_remove.add(telebot.types.InlineKeyboardButton(user.watchlist[0][2],
                                                                            callback_data='coins_remove_step2'))
                    bot.send_message(chat_id=call.message.chat.id, text=trans('C_select_watchlist'),
                                     reply_markup=watchlist_remove)
            else:
                bot.reply_to(call.message, trans('C_create_watchlist_first') + '\n' + trans('C_create_watchlist'))
        if call.data == "coins_remove_step2":
            user = user_dict[call.message.chat.id]
            user.watchlist = functions.get_user_watchlist(connection, user.username)
            coin_keyboard = telebot.types.InlineKeyboardMarkup()
            user_coins = functions.get_user_coins(connection, user.username, user.watchlist[0][2])
            for coin in user_coins:
                coin_keyboard.add(telebot.types.InlineKeyboardButton(coin, callback_data=coin + " delete"))
            bot.send_message(chat_id=call.message.chat.id, text=trans('C_select_coin'), reply_markup=coin_keyboard)

        if "delete" in call.data:
            user = user_dict[call.message.chat.id]
            temp = str(call.data).split(" ")
            coin = coins_list[np.where(coins_list[:, 1] == temp[0])][0][0]
            functions.set_null_coin_user(connection, user.username, coin)
            bot.reply_to(call.message, trans('C_done') + '\n' + trans('C_add_coins'))

        # after call back done keyboard delete
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    """
        login handler
    """

    # get username and store in user dictionary (key:chat_id)
    def process_login_username(message):
        try:
            user = user_dict[message.chat.id]
            user.username = message.text
            # get password with process_password and register_next_step_handler
            # to handle next enter user's message
            msg = bot.reply_to(message, trans('C_enter_password'))
            bot.register_next_step_handler(msg, process_password)
        # some exception need develop
        except Exception as e:
            bot.reply_to(message, trans('C_please_start'))
            del user_dict[message.chat.id]

    # if session assign True user login ,if any exception happened -
    # start again with /start and object user removed
    def process_password(message):
        try:
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
            bot.reply_to(message, trans('C_please_start'))
            del user_dict[message.chat.id]

    """
        register handler
    """

    def process_reg_username(message):
        try:
            # fetch object
            user = reg_dict[message.chat.id]
            user.username = message.text
            msg = bot.reply_to(message, '👮🏻‍♂' + trans('C_enter_password') + trans('C_password_instruction'))
            bot.register_next_step_handler(msg, process_reg_password)
        except Exception as e:
            bot.reply_to(message, trans('C_please_start'))
            del reg_dict[message.chat.id]

    def process_reg_password(message):
        try:
            user = reg_dict[message.chat.id]
            user.password1 = message.text
            msg = bot.reply_to(message, trans('C_enter_password') + trans('C_again'))
            bot.register_next_step_handler(msg, process_reg_password_again)
            # delete password for privacy
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            bot.reply_to(message, trans('C_please_start'))
            del reg_dict[message.chat.id]

    def process_reg_password_again(message):
        try:
            user = reg_dict[message.chat.id]
            user.password2 = message.text
            question_dict = functions.get_security_questions(connection)
            bot.delete_message(message.chat.id, message.message_id)
            # select question
            questions = telebot.types.InlineKeyboardMarkup()
            questions.add(telebot.types.InlineKeyboardButton(question_dict[0][1], callback_data="1"))
            questions.add(telebot.types.InlineKeyboardButton(question_dict[1][1], callback_data="2"))
            bot.send_message(chat_id=message.chat.id, text='⚠️' + trans('C_select_security_question'),
                             reply_markup=questions)
        except Exception as e:
            bot.reply_to(message, trans('C_please_start'))
            del reg_dict[message.chat.id]

    def process_reg_answer(message):
        try:
            user = reg_dict[message.chat.id]
            user.answer = message.text
            # insert to database
            res = register.register(db_connection=connection, username=user.username, chat_id=user.chat_id,
                                    password=user.password1, password2=user.password1,
                                    question_id=user.security_question_id, answer=user.answer)
            # initial default timeframe 1min
            functions.set_timeframe(connection, user.username, 1)
            # init first amount bank
            functions.set_amount_bank_user(connection, user.username, 10)
            bot.reply_to(message, res + "\n" + trans('C_please_start'))
            del reg_dict[message.chat.id]
        except Exception as e:
            bot.reply_to(message, trans('C_please_start'))
            del reg_dict[message.chat.id]

    """
        forget message  handler
    """

    def process_forget_username(message):
        try:
            user = reg_dict[message.chat.id]
            user.username = message.text
            # check user exists if dont handle this next step crashed ->get_user_security_id handled this
            q_id = functions.get_user_security_id(connection, user.username)
            question = functions.get_security_questions(connection, q_id)
            if q_id:
                user.security_question_id = q_id
                user.security_question = functions.get_security_questions(connection, q_id)
                msg = bot.reply_to(message, question[0][1])
                bot.register_next_step_handler(msg, process_forget_answer)
            else:
                bot.send_message(chat_id=message.chat.id,
                                 text=trans('C_username_exist') + '\n' + trans('C_please_start'))
                del reg_dict[message.chat.id]

        except Exception as e:
            bot.reply_to(message, trans('C_please_start'))
            del reg_dict[message.chat.id]

    def process_forget_answer(message):
        try:
            user = reg_dict[message.chat.id]
            user.answer = message.text
            msg = bot.reply_to(message, trans('C_new_password'))
            bot.register_next_step_handler(msg, process_forget_new_pass)
        except Exception as e:
            bot.reply_to(message, trans('C_please_start'))
            del reg_dict[message.chat.id]

    def process_forget_new_pass(message):
        try:
            user = reg_dict[message.chat.id]
            user.password1 = message.text
            msg = bot.reply_to(message, trans('C_enter_password') + trans('C_again'))
            bot.delete_message(message.chat.id, message.message_id)
            bot.register_next_step_handler(msg, process_forget_new_pass_again)
        except Exception as e:
            bot.reply_to(message, trans('C_please_start'))
            del reg_dict[message.chat.id]

    def process_forget_new_pass_again(message):
        try:
            user = reg_dict[message.chat.id]
            user.password2 = message.text
            # reset_password function handle all error about passwords and wrong answer
            res = reset_password.reset_password(db_connection=connection, username=user.username, answer=user.answer,
                                                new_password=user.password1, new_password2=user.password2)
            bot.reply_to(message, res)
            bot.delete_message(message.chat.id, message.message_id)
            # after reset password and update database we dont need this object
            del reg_dict[message.chat.id]
        except Exception as e:
            bot.reply_to(message, trans('C_please_start'))
            del reg_dict[message.chat.id]

    """
        new command handler / for new watchlist
    """

    @bot.message_handler(commands=['new'])
    def new_watchlist(message):
        if message.chat.id not in user_dict:
            bot.reply_to(message, trans('C_please_start'))
        elif not user_dict[message.chat.id].session:
            bot.reply_to(message, trans('C_please_start'))
        else:
            user = user_dict[message.chat.id]
            # if len(functions.get_user_watchlist(connection , user.username)) < 1:
            if not functions.get_user_watchlist(connection, user.username):
                bot.reply_to(message, trans('C_enter_watchlist_name'))
                bot.register_next_step_handler(message, process_new_watch)
            else:
                bot.reply_to(message, trans('C_already_have_watchlist'))

    def process_new_watch(message):
        try:
            # fetch object
            user = user_dict[message.chat.id]
            for create in range(0, 2):
                functions.create_watchlist(connection, user.username, message.text)
            user.watchlist = message.text
            bot.reply_to(message, trans('C_good') + "\n" + trans('C_add_coins'))
        except Exception as e:
            bot.reply_to(message, trans('C_please_start'))

    @bot.message_handler(commands=['add'])
    def add_coin(message):
        if message.chat.id not in user_dict:
            bot.reply_to(message, trans('C_please_start'))
        elif not user_dict[message.chat.id].session:
            bot.reply_to(message, trans('C_please_start'))
        else:
            user = user_dict[message.chat.id]
            user.watchlist = functions.get_user_watchlist(connection, user.username)
            if user.watchlist:
                if functions.get_empty_coins_remain(connection, user.username, user.watchlist[0][2]) != 0:
                    watchlist = telebot.types.InlineKeyboardMarkup()
                    watchlist.add(telebot.types.InlineKeyboardButton(user.watchlist[0][2], callback_data='watchlist'))
                    bot.send_message(chat_id=message.chat.id, text=trans('C_select_watchlist'), reply_markup=watchlist)
                else:
                    bot.reply_to(message, trans('C_full_watchlist'))
            else:
                bot.reply_to(message, trans('C_create_watchlist_first'))

    """
        timeframe command handler update 
    """

    @bot.message_handler(commands=['frame'])
    def update_timeframe(message):
        if message.chat.id not in user_dict:
            bot.reply_to(message, trans('C_please_start'))
        # check user login
        elif user_dict[message.chat.id] and not user_dict[message.chat.id].session:
            bot.reply_to(message, trans('C_logged_out'))
        else:
            time_keyboard = telebot.types.InlineKeyboardMarkup()
            for index, time in timeframes_list:
                time_keyboard.add(telebot.types.InlineKeyboardButton(time, callback_data=time))
            bot.send_message(chat_id=message.chat.id, text=trans('C_select_timeframe'), reply_markup=time_keyboard)

    """
        show command handler
    """

    @bot.message_handler(commands=['show'])
    def update_timeframe(message):
        if message.chat.id not in user_dict:
            bot.reply_to(message, trans('C_please_start'))
        # check user login
        elif user_dict[message.chat.id] and not user_dict[message.chat.id].session:
            bot.reply_to(message, trans('C_logged_out'))
        else:
            user = user_dict[message.chat.id]
            user.watchlist = functions.get_user_watchlist(connection, user.username)
            if user.watchlist:
                amount = functions.get_amount_bank_user(connection, user.username)
                timeframe = functions.get_user_timeframe(connection, user.username)
                coins = ""
                for watchlist in user.watchlist:
                    if watchlist[1]:
                        coin = str(functions.get_coin_name(connection, int(watchlist[1])))
                        percent = candle.get_percent_candle(coin, timeframe)
                        percent = str(percent) + " 🔴" if percent < 0 else str(percent) + " 🟢"
                        coins += coin + " %" + percent + "\n"
                # amount = 0
                res = "💰 " + trans('C_assets') + "\n" + str(amount) + "$\n\n👀 " \
                      + trans('C_watchlist') + "\n" + user.watchlist[0][2] + "\n\n💎 " \
                      + trans('C_coin') + "\n" + coins + "\n⏱ " + trans('C_timeframe') + "\n" + timeframe
                bot.reply_to(message, res)
            else:
                bot.reply_to(message, trans('C_create_watchlist_first'))

    @bot.message_handler(commands=['analysis'])
    def update_timeframe(message):
        if message.chat.id not in user_dict:
            bot.reply_to(message, trans('C_please_start'))
        # check user login
        elif user_dict[message.chat.id] and not user_dict[message.chat.id].session:
            bot.reply_to(message, trans('C_logged_out'))
        else:
            # if user dont have an analysis
            user = user_dict[message.chat.id]
            analysis = functions.get_user_analysis(connection, user.username)
            if not analysis:
                analysis_keyboard = telebot.types.InlineKeyboardMarkup()
                for index, analy in analysis_list:
                    analysis_keyboard.add(telebot.types.InlineKeyboardButton(analy, callback_data=analy))
                bot.send_message(chat_id=message.chat.id, text=trans('C_select_analysis'),
                                 reply_markup=analysis_keyboard)
            else:
                bot.reply_to(message, trans('C_already_have_analysis') + analysis)

    """
            removes command handler
    """

    @bot.message_handler(commands=['remove'])
    def remove(message):
        if message.chat.id not in user_dict:
            bot.reply_to(message, trans('C_please_start'))
        # check user login
        elif not user_dict[message.chat.id].session:
            bot.reply_to(message, trans('C_please_start'))
        else:
            try:
                remove_keyboard = telebot.types.InlineKeyboardMarkup()
                remove_keyboard.add(telebot.types.InlineKeyboardButton(trans('C_watchlist')
                                                                       , callback_data="remove_watchlist"))
                remove_keyboard.add(telebot.types.InlineKeyboardButton(trans('C_coin')
                                                                       , callback_data="remove_coins"))
                bot.send_message(chat_id=message.chat.id, text=trans('C_select_option_delete'),
                                 reply_markup=remove_keyboard)

            except Exception as e:
                bot.reply_to(message, trans('C_unsuccessful_operation'))

    """
        logout command handler
    """

    @bot.message_handler(commands=['logout'])
    def logout(message):
        if message.chat.id not in user_dict:
            bot.reply_to(message, trans('C_please_start'))
        # check user login
        elif user_dict[message.chat.id] and not user_dict[message.chat.id].session:
            bot.reply_to(message, trans('C_logged_out'))
        else:
            try:
                user_dict[message.chat.id].session = False
                bot.reply_to(message, trans('C_goodbye') + '\n' + trans('C_login_again'))
                del user_dict[message.chat.id]
                print(user_dict)
            except Exception as e:
                bot.reply_to(message, trans('C_unsuccessful_logout'))
