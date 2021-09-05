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
from Auth import register, reset_password
from Inc import db, functions
import numpy as np
from binance.client import Client
from Telegram.Client import candle
from Account.clients import User, Register
from Libraries.definitions import *
from Interfaces.telegram import Telegram

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


class ClientBot(Telegram):
    def __init__(self):
        Telegram.__init__(self, API_KEY=API_KEY)

    # def bot_actions(self):
    def bot_actions(self):
        @self.bot.middleware_handler(update_types=['message'])
        def activate_language(bot_instance, message):
            activate(message.from_user.language_code)

        # /start command enter by user
        @self.bot.message_handler(commands=['start'])
        def welcome(message):
            if not self.check_login(message):
                # some action with delay to typing bot
                self.bot.send_chat_action(chat_id=message.chat.id, action="typing")
                sleep(1)
                # welcome message and instructions
                self.bot.reply_to(message, trans('C_hello') + message.chat.first_name + "!\n" + trans('C_welcome'))
                # the markup help us we have call back with inlinekeyboard when yours tap one of those
                # some callback data send and we receive with @bot.callback_query_handler
                step_kb = telebot.types.InlineKeyboardMarkup()
                step_kb.add(telebot.types.InlineKeyboardButton(trans('C_login'), callback_data='login'))
                step_kb.add(telebot.types.InlineKeyboardButton(trans('C_register'), callback_data='reg'))
                step_kb.add(telebot.types.InlineKeyboardButton(trans('C_forget_password'), callback_data='forget'))
                self.bot.send_message(chat_id=message.chat.id, text=trans('C_any_account'), reply_markup=step_kb)

        # after callback @bot.callback_query_handler get function parameter ,this always true
        # and w8 to one case login and reg and .. happened . need to develop func in parameter
        @self.bot.callback_query_handler(func=lambda call: True)
        def query_handler(call):
            if call.data == "login":
                # create object from user and store in our dictionary with chat_id key value
                user = User()
                self.user_dict[call.message.chat.id] = user
                self.bot.reply_to(call.message, trans('C_enter_username'))
                # handle next step message user enter after login
                self.bot.register_next_step_handler(call.message, callback=self.process_login_username)
            if call.data == "reg":
                if functions.check_chat_id(connection, call.message.chat.id):
                    # create object from user and store in our dictionary with chat_id key value
                    user = Register(call.message.chat.id)
                    self.reg_dict[call.message.chat.id] = user
                    self.bot.reply_to(call.message, trans('C_enter_username'))
                    # handle next step message user enter after sign up
                    self.bot.register_next_step_handler(call.message, callback=process_reg_username)
                else:
                    username = functions.get_user_with_chat_id(connection, call.message.chat.id)
                    self.bot.reply_to(call.message,
                                      trans('C_already_have_account') + f" {username} \n" + trans('C_please_start'))
            if call.data == "1" or call.data == "2":
                # in other keyboard we need calls back from user choose which one question
                user = self.reg_dict[call.message.chat.id]
                # store in our object
                user.security_question_id = int(call.data)
                self.bot.reply_to(call.message, trans('C_enter_answer'))
                # handle next step message user enter after choose question
                self.bot.register_next_step_handler(call.message, callback=process_reg_answer)
            if call.data == "forget":
                # create object from user and store in our dictionary with chat_id key value
                user = Register(call.message.chat.id)
                self.reg_dict[call.message.chat.id] = user
                self.bot.reply_to(call.message, trans('C_enter_username'))
                # handle next step message user enter after forget password
                self.bot.register_next_step_handler(call.message, callback=process_forget_username)
            if call.data == "watchlist":
                coin_keyboard = telebot.types.InlineKeyboardMarkup()
                for index, coin in self.coins_list:
                    coin_keyboard.add(telebot.types.InlineKeyboardButton(coin, callback_data=coin))
                self.bot.send_message(chat_id=call.message.chat.id, text=trans('C_select_coin'),
                                      reply_markup=coin_keyboard)

            # need more develop
            if call.data in self.coins_list[:, 1]:
                coin = self.coins_list[np.where(self.coins_list[:, 1] == call.data)][0][0]
                # for coins in coins[:1]:
                user = self.user_dict[call.message.chat.id]
                if not functions.set_coin(connection, user.username, coin, user.watchlist[0][2])[0]:
                    self.bot.reply_to(call.message, trans('C_coin_already_exist'))
                else:
                    self.bot.reply_to(call.message, trans('C_done') + "\n"
                                      + trans('C_default_timeframe') + "\n" + trans('C_change_timeframe'))

            if call.data in self.timeframes_list[:, 1]:
                time_id = self.timeframes_list[np.where(self.timeframes_list[:, 1] == call.data)][0][0]
                time = self.timeframes_list[np.where(self.timeframes_list[:, 1] == call.data)][0][1]
                # for coins in coins[:1]:
                user = self.user_dict[call.message.chat.id]
                functions.update_timeframe(connection, user.username, time_id)
                self.bot.reply_to(call.message, trans('C_done') + trans('C_timeframe_changed') + time)

            if call.data in self.analysis_list[:, 1]:
                user = self.user_dict[call.message.chat.id]
                analysis_id = self.analysis_list[np.where(self.analysis_list[:, 1] == call.data)][0][0]
                functions.set_user_analysis(connection, user.username, int(analysis_id))
                self.bot.reply_to(call.message,
                                  trans('C_done') + "\n" + trans('C_now') + call.data + trans('C_working_for_you'))
            if call.data == "remove_watchlist":
                user = self.user_dict[call.message.chat.id]
                user.watchlist = functions.get_user_watchlist(connection, user.username)
                if user.watchlist:
                    watchlist_remove = telebot.types.InlineKeyboardMarkup()
                    # for watch in user.watchlist :
                    user.temp_watch = user.watchlist[0][2]
                    watchlist_remove.add(
                        telebot.types.InlineKeyboardButton(user.watchlist[0][2],
                                                           callback_data='watchlist_remove_step2'))
                    self.bot.send_message(chat_id=call.message.chat.id, text=trans('C_select_watchlist'),
                                          reply_markup=watchlist_remove)
                else:
                    self.bot.reply_to(call.message, trans('C_null_watchlist'))
            if call.data == "watchlist_remove_step2":
                user = self.user_dict[call.message.chat.id]
                functions.delete_watchlist(connection, user.username, user.temp_watch)
                self.bot.reply_to(call.message, trans('C_done') + '\n' + trans('C_create_watchlist'))

            if call.data == "remove_coins":
                user = self.user_dict[call.message.chat.id]
                user.watchlist = functions.get_user_watchlist(connection, user.username)
                if user.watchlist:
                    if functions.get_empty_coins_remain(connection, user.username, user.watchlist[0][2]) == 2:
                        self.bot.reply_to(call.message, trans('C_null_coin'))
                    else:
                        watchlist_remove = telebot.types.InlineKeyboardMarkup()
                        # for watch in user.watchlist :
                        user.temp_watch = user.watchlist[0][2]
                        watchlist_remove.add(telebot.types.InlineKeyboardButton(user.watchlist[0][2],
                                                                                callback_data='coins_remove_step2'))
                        self.bot.send_message(chat_id=call.message.chat.id, text=trans('C_select_watchlist'),
                                              reply_markup=watchlist_remove)
                else:
                    self.bot.reply_to(call.message,
                                      trans('C_create_watchlist_first') + '\n' + trans('C_create_watchlist'))
            if call.data == "coins_remove_step2":
                user = self.user_dict[call.message.chat.id]
                user.watchlist = functions.get_user_watchlist(connection, user.username)
                coin_keyboard = telebot.types.InlineKeyboardMarkup()
                user_coins = functions.get_user_coins(connection, user.username, user.watchlist[0][2])
                for coin in user_coins:
                    coin_keyboard.add(telebot.types.InlineKeyboardButton(coin, callback_data=coin + " delete"))
                self.bot.send_message(chat_id=call.message.chat.id, text=trans('C_select_coin'),
                                      reply_markup=coin_keyboard)

            if "delete" in call.data:
                user = self.user_dict[call.message.chat.id]
                temp = str(call.data).split(" ")
                coin = self.coins_list[np.where(self.coins_list[:, 1] == temp[0])][0][0]
                functions.set_null_coin_user(connection, user.username, coin)
                self.bot.reply_to(call.message, trans('C_done') + '\n' + trans('C_add_coins'))

            # after call back done keyboard delete
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        """
            register handler
        """

        def process_reg_username(message):
            try:
                # fetch object
                user = self.reg_dict[message.chat.id]
                user.username = message.text
                msg = self.bot.reply_to(message, '👮🏻‍♂' + trans('C_enter_password') + trans('C_password_instruction'))
                self.bot.register_next_step_handler(msg, process_reg_password)
            except Exception as e:
                self.bot.reply_to(message, trans('C_please_start'))
                del self.reg_dict[message.chat.id]
                print(e)

        def process_reg_password(message):
            try:
                user = self.reg_dict[message.chat.id]
                user.password1 = message.text
                msg = self.bot.reply_to(message, trans('C_enter_password') + trans('C_again'))
                self.bot.register_next_step_handler(msg, process_reg_password_again)
                # delete password for privacy
                self.bot.delete_message(message.chat.id, message.message_id)
            except Exception as e:
                self.bot.reply_to(message, trans('C_please_start'))
                del self.reg_dict[message.chat.id]
                print(e)

        def process_reg_password_again(message):
            try:
                user = self.reg_dict[message.chat.id]
                user.password2 = message.text
                question_dict = functions.get_security_questions(connection)
                self.bot.delete_message(message.chat.id, message.message_id)
                # select question
                questions = telebot.types.InlineKeyboardMarkup()
                questions.add(telebot.types.InlineKeyboardButton(question_dict[0][1], callback_data="1"))
                questions.add(telebot.types.InlineKeyboardButton(question_dict[1][1], callback_data="2"))
                self.bot.send_message(chat_id=message.chat.id, text='⚠️' + trans('C_select_security_question'),
                                      reply_markup=questions)
            except Exception as e:
                self.bot.reply_to(message, trans('C_please_start'))
                del self.reg_dict[message.chat.id]
                print(e)

        def process_reg_answer(message):
            try:
                user = self.reg_dict[message.chat.id]
                user.answer = message.text
                # insert to database
                res = register.register(db_connection=connection, username=user.username, chat_id=user.chat_id,
                                        password=user.password1, password2=user.password1,
                                        question_id=user.security_question_id, answer=user.answer)
                # initial default timeframe 1min
                functions.set_timeframe(connection, user.username, 1)
                # init first amount bank
                functions.set_amount_bank_user(connection, user.username, 10)
                self.bot.reply_to(message, res + "\n" + trans('C_please_start'))
                del self.reg_dict[message.chat.id]
            except Exception as e:
                self.bot.reply_to(message, trans('C_please_start'))
                del self.reg_dict[message.chat.id]
                print(e)

        """
            forget message  handler
        """

        def process_forget_username(message):
            try:
                user = self.reg_dict[message.chat.id]
                user.username = message.text
                # check user exists if dont handle this next step crashed ->get_user_security_id handled this
                q_id = functions.get_user_security_id(connection, user.username)
                question = functions.get_security_questions(connection, q_id)
                if q_id:
                    user.security_question_id = q_id
                    user.security_question = functions.get_security_questions(connection, q_id)
                    msg = self.bot.reply_to(message, question[0][1])
                    self.bot.register_next_step_handler(msg, process_forget_answer)
                else:
                    self.bot.send_message(chat_id=message.chat.id,
                                          text=trans('C_username_exist') + '\n' + trans('C_please_start'))
                    del self.reg_dict[message.chat.id]

            except Exception as e:
                self.bot.reply_to(message, trans('C_please_start'))
                del self.reg_dict[message.chat.id]
                print(e)

        def process_forget_answer(message):
            try:
                user = self.reg_dict[message.chat.id]
                user.answer = message.text
                msg = self.bot.reply_to(message, trans('C_new_password'))
                self.bot.register_next_step_handler(msg, process_forget_new_pass)
            except Exception as e:
                self.bot.reply_to(message, trans('C_please_start'))
                del self.reg_dict[message.chat.id]
                print(e)

        def process_forget_new_pass(message):
            try:
                user = self.reg_dict[message.chat.id]
                user.password1 = message.text
                msg = self.bot.reply_to(message, trans('C_enter_password') + trans('C_again'))
                self.bot.delete_message(message.chat.id, message.message_id)
                self.bot.register_next_step_handler(msg, process_forget_new_pass_again)
            except Exception as e:
                self.bot.reply_to(message, trans('C_please_start'))
                del self.reg_dict[message.chat.id]
                print(e)

        def process_forget_new_pass_again(message):
            try:
                user = self.reg_dict[message.chat.id]
                user.password2 = message.text
                # reset_password function handle all error about passwords and wrong answer
                res = reset_password.reset_password(db_connection=connection, username=user.username,
                                                    answer=user.answer,
                                                    new_password=user.password1, new_password2=user.password2)
                self.bot.reply_to(message, res)
                self.bot.delete_message(message.chat.id, message.message_id)
                # after reset password and update database we dont need this object
                del self.reg_dict[message.chat.id]
            except Exception as e:
                self.bot.reply_to(message, trans('C_please_start'))
                del self.reg_dict[message.chat.id]
                print(e)

        """
            new command handler / for new watchlist
        """

        @self.bot.message_handler(commands=['new'])
        def new_watchlist(message):
            if self.check_login(message):
                user = self.user_dict[message.chat.id]
                # if len(functions.get_user_watchlist(connection , user.username)) < 1:
                if not functions.get_user_watchlist(connection, user.username):
                    self.bot.reply_to(message, trans('C_enter_watchlist_name'))
                    self.bot.register_next_step_handler(message, process_new_watch)
                else:
                    self.bot.reply_to(message, trans('C_already_have_watchlist'))

        def process_new_watch(message):
            try:
                # fetch object
                user = self.user_dict[message.chat.id]
                for create in range(0, 2):
                    functions.create_watchlist(connection, user.username, message.text)
                user.watchlist = message.text
                self.bot.reply_to(message, trans('C_good') + "\n" + trans('C_add_coins'))
            except Exception as e:
                self.bot.reply_to(message, trans('C_please_start'))
                print(e)

        @self.bot.message_handler(commands=['add'])
        def add_coin(message):
            if self.check_login(message):
                user = self.user_dict[message.chat.id]
                user.watchlist = functions.get_user_watchlist(connection, user.username)
                if user.watchlist:
                    if functions.get_empty_coins_remain(connection, user.username, user.watchlist[0][2]) != 0:
                        watchlist = telebot.types.InlineKeyboardMarkup()
                        watchlist.add(
                            telebot.types.InlineKeyboardButton(user.watchlist[0][2], callback_data='watchlist'))
                        self.bot.send_message(chat_id=message.chat.id, text=trans('C_select_watchlist'),
                                              reply_markup=watchlist)
                    else:
                        self.bot.reply_to(message, trans('C_full_watchlist'))
                else:
                    self.bot.reply_to(message, trans('C_create_watchlist_first'))

        """
            timeframe command handler update 
        """

        @self.bot.message_handler(commands=['frame'])
        def update_timeframe(message):
            if self.check_login(message):
                time_keyboard = telebot.types.InlineKeyboardMarkup()
                for index, time in self.timeframes_list:
                    time_keyboard.add(telebot.types.InlineKeyboardButton(time, callback_data=time))
                self.bot.send_message(chat_id=message.chat.id, text=trans('C_select_timeframe'),
                                      reply_markup=time_keyboard)

        """
            show command handler
        """

        @self.bot.message_handler(commands=['show'])
        def update_timeframe(message):
            if self.check_login(message):
                user = self.user_dict[message.chat.id]
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
                    self.bot.reply_to(message, res)
                else:
                    self.bot.reply_to(message, trans('C_create_watchlist_first'))

        @self.bot.message_handler(commands=['candle'])
        def update_timeframe(message):
            if self.check_login(message):
                user = self.user_dict[message.chat.id]
                coins = functions.get_user_coins(connection, user.username)
                timeframe = functions.get_user_timeframe(connection, user.username)
                for coin in coins:
                    res = candle.candle_details_to_string(coin, timeframe)
                    self.bot.reply_to(message, res)

        @self.bot.message_handler(commands=['analysis'])
        def update_timeframe(message):
            if self.check_login(message):
                # if user dont have an analysis
                user = self.user_dict[message.chat.id]
                analysis = functions.get_user_analysis(connection, user.username)
                if not analysis:
                    analysis_keyboard = telebot.types.InlineKeyboardMarkup()
                    for index, analyze in self.analysis_list:
                        analysis_keyboard.add(telebot.types.InlineKeyboardButton(analyze, callback_data=analyze))
                    self.bot.send_message(chat_id=message.chat.id, text=trans('C_select_analysis'),
                                          reply_markup=analysis_keyboard)
                else:
                    self.bot.reply_to(message, trans('C_already_have_analysis') + analysis)

        """
                removes command handler
        """

        @self.bot.message_handler(commands=['remove'])
        def remove(message):
            if self.check_login(message):
                try:
                    remove_keyboard = telebot.types.InlineKeyboardMarkup()
                    remove_keyboard.add(telebot.types.InlineKeyboardButton(trans('C_watchlist'),
                                                                           callback_data="remove_watchlist"))
                    remove_keyboard.add(telebot.types.InlineKeyboardButton(trans('C_coin'),
                                                                           callback_data="remove_coins"))
                    self.bot.send_message(chat_id=message.chat.id, text=trans('C_select_option_delete'),
                                          reply_markup=remove_keyboard)

                except Exception as e:
                    self.bot.reply_to(message, trans('C_unsuccessful_operation'))
                    print(e)

        @self.bot.message_handler(commands=['help'])
        def remove(message):
            try:
                self.bot.reply_to(message, trans('C_help'))

            except Exception as e:
                self.bot.reply_to(message, trans('C_unsuccessful_operation'))
                print(e)

        """
            logout command handler
        """

        @self.bot.message_handler(commands=['logout'])
        def logout(message):
            if self.check_login(message):
                try:
                    self.user_dict[message.chat.id].session = False
                    self.bot.reply_to(message, trans('C_goodbye') + '\n' + trans('C_login_again'))
                    del self.user_dict[message.chat.id]
                    print(self.user_dict)
                except Exception as e:
                    self.bot.reply_to(message, trans('C_unsuccessful_logout'))
                    print(e)
