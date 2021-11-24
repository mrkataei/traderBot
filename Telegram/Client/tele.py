""""
Mr.Kataei 11/23/2021

"""
from time import sleep

from telebot import types
from telebot import apihelper
from Auth.register import register
from Inc import functions
from Account.clients import User
# from Libraries.definitions import *
from Interfaces.telegram import Telegram
import numpy as np

# from Libraries.data_collector import get_candle_binance as candles
# from Analysis.emerald import Emerald
# from Test.strategy_tester import StrategyTaster

apihelper.ENABLE_MIDDLEWARE = True

# @testkourosh2bot -> address // use this bot for test your code
API_KEY = '1978536410:AAE_RMk3-4r_cLnt_nRcEnZHaSp-vIk9oVo'

timeframe_binance_dictionary = {
    '30min': '30m',
    '1hour': '1h',
    '4hour': '4h',
    '1day': '1d',
    '1min': '1m'
}


def start_keyboard():
    key_markup = types.ReplyKeyboardMarkup(row_width=2)
    key_add_account = types.KeyboardButton('🏛 add exchange')
    key_add_strategy = types.KeyboardButton('📊 add strategy')
    key_tutorials = types.KeyboardButton('📚 tutorials')
    key_plans = types.KeyboardButton('💳 plans')
    key_profile = types.KeyboardButton('🙍🏻‍♂️profile')
    key_back_test = types.KeyboardButton('🧭 back test')
    key_help = types.KeyboardButton('🤔 help')
    key_markup.add(key_add_account, key_add_strategy, key_tutorials, key_plans, key_profile, key_back_test, key_help)
    return key_markup


def analysis_keyboard():
    """
    :return:
    """
    analysis = np.array(functions.get_analysis())
    key_markup = types.ReplyKeyboardMarkup(row_width=1)
    key_markup.add(*analysis[:, 1])
    return key_markup


def coins_keyboard():
    """
    :return:
    """
    coins = np.array(functions.get_coins())
    key_markup = types.ReplyKeyboardMarkup(row_width=3)
    key_markup.add(*coins[:, 1])
    return key_markup


def timeframe_keyboard():
    """
    :return:
    """
    timeframes = np.array(functions.get_timeframes())
    key_markup = types.ReplyKeyboardMarkup(row_width=3)
    key_markup.add(*timeframes[:, 1])
    return key_markup


def user_exchanges_account_keyboard(message):
    """
    :return:
    """
    exchanges = functions.get_user_exchanges(message.chat.id)
    if exchanges:
        exchanges = np.array(exchanges)
        key_markup = types.ReplyKeyboardMarkup(row_width=1)
        key_markup.add(*exchanges[:, 0])
        return key_markup
    else:
        return False


def exchanges_keyboard():
    """
    :return:
    """
    exchanges = np.array(functions.get_exchanges())
    key_markup = types.ReplyKeyboardMarkup(row_width=1)
    key_markup.add(*exchanges[:, 1])
    return key_markup


class ClientBot(Telegram):
    def __init__(self):
        Telegram.__init__(self, API_KEY=API_KEY)
        self.exchanges = np.array(functions.get_exchanges())
        self.coins = np.array(functions.get_coins())
        self.analysis = np.array(functions.get_analysis())
        self.timeframes = np.array(functions.get_timeframes())

    def is_valid_user(self, message):
        user = functions.get_user(message.chat.id)
        if not user:
            self.bot.send_message(message.chat.id, 'Sorry\n 😥You should signup')
            return False
        else:
            result = functions.check_expire_plan(chat_id=message.chat.id)
            if result:
                self.bot.send_message(message.chat.id, 'Your plan is expire!😪\n'
                                                       'Recharge your plan please.')
                return False
            else:
                return True

    def can_start_bot(self, message):
        if message.chat.id in self.user_dict:
            return False
        else:
            self.bot.send_message(message.chat.id, '⚠️ Please /start Bot')
            return True

    def is_valid_command(self, message):
        if not self.can_start_bot(message=message) and self.is_valid_user(message=message):
            return True
        else:
            return False

    def check_add_command(self, message):
        if self.is_valid_command(message=message):
            user = self.user_dict[message.chat.id]
            user.update_user_plan_limit()
            if user.strategy > len(functions.get_user_watchlist(username=user.username)):
                # if message.text == '📊 add strategy' and not user.is_in_process:
                return True
            else:
                self.bot.send_message(message.chat.id, '❌ Your strategies is full\n'
                                                       '🤓 Upgrade your plan or edit it in your profile')
                return False
        else:
            return False

    def check_setup_command(self, message):
        if self.is_valid_command(message=message):
            user = self.user_dict[message.chat.id]
            user.update_user_plan_limit()
            if user.account > len(functions.get_user_exchange(chat_id=message.chat.id)):
                return True
            else:
                self.bot.send_message(message.chat.id, '❌ Your exchange accounts is full\n'
                                                       '🤓 Upgrade your plan or edit it in your profile')
                return False
        else:
            return False

    def check_test_command(self, message):
        if self.is_valid_command(message=message):
            return True
        else:
            return False

    def bot_actions(self):
        @self.bot.message_handler(commands=['start'], func=self.can_start_bot)
        def welcome(message):
            user = functions.get_user(message.chat.id)
            markup = start_keyboard()
            # is typing bot ..
            self.bot.send_chat_action(chat_id=message.chat.id, action="typing")
            sleep(1)

            self.bot.send_message(message.chat.id, '🙋🏽‍♂️ Hey ' + message.chat.first_name + "!\n" +
                                  'I am AI Trader, your trade assistance\n /help to show what can i do for you😎',
                                  reply_markup=markup)
            self.user_dict[message.chat.id] = User(chat_id=message.chat.id)  # create object for register user session
            if not user:
                # if user deleted telegram account need develop
                keyboard = types.ReplyKeyboardMarkup()
                reg_button = types.KeyboardButton(text="📞 Share your phone number", request_contact=True)
                keyboard.add(reg_button)
                self.bot.send_message(message.chat.id, "You should sign up with your phone number 🙄",
                                      reply_markup=keyboard)
            else:
                self.user_dict[message.chat.id].username = user[0][0]
                if self.is_valid_user(message=message):
                    functions.update_user_online(username=user[0][0], online=True)
                    # markup_key = start_keyboard()
                    self.bot.send_message(message.chat.id, '🤩 Welcome back')

        @self.bot.message_handler(content_types=['contact'],
                                  func=lambda message: functions.is_user_signup(message.chat.id))
        def register_handler(message):
            markup = types.ReplyKeyboardRemove(selective=False)
            self.bot.send_message(message.chat.id, '🙍🏻‍♂️ Please enter your username', reply_markup=markup)
            self.bot.register_next_step_handler(message=message, callback=reg_step_1,
                                                phone=message.contact.phone_number)

        def reg_step_1(message, phone: str):
            user = self.user_dict[message.chat.id]
            try:
                if functions.check_username_exist(username=message.text):
                    self.bot.send_message(message.chat.id, '⛔️ Username already exist!\nTry again!')
                    self.bot.register_next_step_handler(message=message, callback=reg_step_1,
                                                        phone=phone)
                else:
                    user.username = message.text
                    error, detail = register(username=user.username, chat_id=user.chat_id, phone=phone)
                    if error:
                        self.bot.reply_to(message, '⛔️ Try again')
                    else:
                        functions.update_user_online(username=user.username, online=True)
                        markup = start_keyboard()
                        self.bot.send_message(message.chat.id, '🥳 Welcome!\n'
                                                               'Your account created!\n'
                                                               '⚠️ Free plan is available for 30 day\n'
                                                               'Enjoy!', reply_markup=markup)
            except Exception as e:
                self.bot.reply_to(message, '⛔️ Try again')
                print(e)

        @self.bot.message_handler(commands=['set'], func=self.check_setup_command)
        def add_exchange(message):
            try:
                key_markup = exchanges_keyboard()
                self.bot.send_message(message.chat.id, '🏛  Please Select your exchange account',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_1)

            except Exception as e:
                self.bot.reply_to(message, '⛔️ Error')
                print(e)

        def add_exchange_step_1(message):
            try:
                exchanges_id = np.where(self.exchanges[:, 1] == message.text)[0][0]
                key_markup = types.ReplyKeyboardRemove(selective=False)
                self.bot.send_message(message.chat.id, '🔐 Enter your public API', reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_2,
                                                    exchange_id=self.exchanges[exchanges_id][0])
            except IndexError:
                self.bot.send_message(message.chat.id, '⛔️ wrong exchange')
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_1)

        def add_exchange_step_2(message, exchange_id: int):
            if message.content_type == 'text':
                self.bot.send_message(message.chat.id, '🔐 Enter your secret API')
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_3,
                                                    exchange_id=exchange_id, public=message.text)
                self.bot.delete_message(message.chat.id, message.message_id)
            else:
                self.bot.send_message(message.chat.id, '⛔️ wrong API')
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_2,
                                                    exchange_id=exchange_id)

        def add_exchange_step_3(message, exchange_id: int, public: str):
            if message.content_type == 'text':
                user = self.user_dict[message.chat.id]
                error, result = functions.set_user_setting(username=str(user.username), exchange_id=int(exchange_id),
                                                           public=str(public), secret=str(message.text))
                self.bot.delete_message(message.chat.id, message.message_id)
                markup = start_keyboard()
                if error:
                    self.bot.send_message(message.chat.id, '😥 Something is wrong\n Try again! ', markup)
                else:
                    self.bot.send_message(message.chat.id, '✅ success', reply_markup=markup)
            else:
                self.bot.send_message(message.chat.id, '⛔️ wrong API')
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_3,
                                                    exchange_id=exchange_id, public=public)

        @self.bot.message_handler(commands=['test'], func=self.check_test_command)
        def back_test(message):
            try:
                key_markup = analysis_keyboard()
                self.bot.send_message(message.chat.id, '📊 Please Select analysis',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=back_test_step_1)

            except Exception as e:
                self.bot.reply_to(message, '⛔️ Error')
                print(e)

        def back_test_step_1(message):
            try:
                analysis_id = np.where(self.analysis[:, 1] == message.text)[0][0]
                key_markup = coins_keyboard()
                self.bot.send_message(message.chat.id, '🪙 Choose Coin',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=back_test_step_2,
                                                    analysis_id=self.analysis[analysis_id][0])
            except IndexError:
                self.bot.send_message(message.chat.id, '⛔️ wrong analysis')
                self.bot.register_next_step_handler(message=message, callback=back_test_step_1)

        def back_test_step_2(message, analysis_id: int):
            try:
                coin_id = np.where(self.coins[:, 1] == message.text)[0][0]
                key_markup = timeframe_keyboard()
                self.bot.send_message(message.chat.id, '⏱ Choose timeframe',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=back_test_step_3,
                                                    analysis_id=analysis_id, coin_id=self.coins[coin_id][0])

            except IndexError:
                self.bot.send_message(message.chat.id, '⛔️ wrong coin')
                self.bot.register_next_step_handler(message=message, callback=back_test_step_2,
                                                    analysis_id=analysis_id)

        def back_test_step_3(message, analysis_id: int, coin_id: int):
            try:
                timeframe_id = np.where(self.timeframes[:, 1] == message.text)[0][0]
                print(self.timeframes)
                key_markup = types.ReplyKeyboardRemove(selective=False)
                self.bot.send_message(message.chat.id, '💰 Please enter amount of founds initially available for'
                                                       ' the strategies for trade(⚠️ greater than 0)',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=back_test_step_4,
                                                    analysis_id=analysis_id, coin_id=coin_id,
                                                    timeframe_id=self.timeframes[timeframe_id][0])
            except IndexError:
                self.bot.send_message(message.chat.id, '⛔️ wrong timeframe')
                self.bot.register_next_step_handler(message=message, callback=back_test_step_3,
                                                    analysis_id=analysis_id, coin_id=coin_id)

        def back_test_step_4(message, analysis_id: int, coin_id: int, timeframe_id: int):
            try:
                amount = float(message.text)
                if not 0 < amount:
                    self.bot.send_message(message.chat.id, '⚠️ Amount must be greater than 0')
                    self.bot.register_next_step_handler(message=message, callback=back_test_step_4,
                                                        analysis_id=analysis_id, coin_id=coin_id,
                                                        timeframe_id=timeframe_id)
                else:
                    # timeframe_id = self.timeframes[timeframe_id[0][0]][0]
                    print(analysis_id, coin_id, timeframe_id)
                    # symbol = functions.get_coins(coin_id=int(coin_id))[0][0]
                    # timeframe = functions.get_timeframes(timeframe_id=int(timeframe_id))[0][0]
                    # data = candles(symbol=symbol, timeframe=timeframe_binance_dictionary[timeframe], limit=400)
                    # data = Emerald(data=data, coin_id=coin_id, timeframe_id=timeframe_id,
                    #                bot_ins=1).get_recommendations()
                    markup = start_keyboard()
                    self.bot.send_message(message.chat.id, '✅ success', reply_markup=markup)

            except (ValueError, TypeError):
                self.bot.send_message(message.chat.id, '⚠️ Amount must be greater than 0')
                self.bot.register_next_step_handler(message=message, callback=back_test_step_4,
                                                    analysis_id=analysis_id, coin_id=coin_id,
                                                    timeframe_id=timeframe_id)

        @self.bot.message_handler(commands=['add'], func=self.check_add_command)
        def add_strategy(message):
            try:
                key_markup = user_exchanges_account_keyboard(message=message)
                if key_markup:
                    self.bot.send_message(message.chat.id, '🏛  Please Select your exchange account',
                                          reply_markup=key_markup)
                    self.bot.register_next_step_handler(message=message, callback=add_strategy_step_1)
                else:
                    self.bot.send_message(message.chat.id, '⛔️ Please set your exchange account first')

            except Exception as e:
                self.bot.reply_to(message, '⛔️ Error')
                print(e)

        def add_strategy_step_1(message):
            try:
                exchanges_id = np.where(self.exchanges[:, 1] == message.text)[0][0]
                key_markup = coins_keyboard()
                self.bot.send_message(message.chat.id, '🪙 Choose Coin',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_2,
                                                    exchange_id=self.exchanges[exchanges_id][0])
            except IndexError:
                self.bot.send_message(message.chat.id, '⛔️ wrong exchange')
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_1)

        def add_strategy_step_2(message, exchange_id: int):
            try:
                coin_id = np.where(self.coins[:, 1] == message.text)[0][0]
                key_markup = analysis_keyboard()
                self.bot.send_message(message.chat.id, '📊 Please Select analysis',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_3,
                                                    exchange_id=exchange_id, coin_id=self.coins[coin_id][0])
            except IndexError:
                self.bot.send_message(message.chat.id, '⛔️ wrong coin')
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_2,
                                                    exchange_id=exchange_id)

        def add_strategy_step_3(message, exchange_id: int, coin_id: int):
            try:
                analysis_id = np.where(self.analysis[:, 1] == message.text)[0][0]
                key_markup = types.ReplyKeyboardRemove(selective=False)
                self.bot.send_message(message.chat.id, '💰 Please enter percent of coin \n'
                                                       'You want to trade (⚠️ between 0 - 100)',
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_4,
                                                    exchange_id=exchange_id, coin_id=coin_id,
                                                    analysis_id=self.analysis[analysis_id][0])
            except IndexError:
                self.bot.send_message(message.chat.id, '⛔️ wrong analysis')
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_3,
                                                    exchange_id=exchange_id, coin_id=coin_id)

        def add_strategy_step_4(message, exchange_id: int, coin_id: int, analysis_id: int):
            user = self.user_dict[message.chat.id]
            try:
                percent = float(message.text)
                if not 0 < percent < 100:
                    self.bot.send_message(message.chat.id, '⚠️ Percent must be between 0 - 100')
                    self.bot.register_next_step_handler(message=message, callback=add_strategy_step_4,
                                                        exchange_id=exchange_id, coin_id=coin_id,
                                                        analysis_id=analysis_id)
                else:
                    setting_id = functions.get_user_settings_id(chat_id=message.chat.id,
                                                                exchange_id=exchange_id)[0][0]
                    error, result = functions.set_watchlist(user_setting_id=int(setting_id), coin_id=int(coin_id),
                                                            username=user.username, analysis_id=int(analysis_id),
                                                            amount=percent)
                    markup = start_keyboard()
                    if error:
                        self.bot.send_message(message.chat.id, '😥You already have this strategy '
                                                               'with selected coin and analysis', reply_markup=markup)
                    else:
                        self.bot.send_message(message.chat.id, '✅ success', reply_markup=markup)

            except (ValueError, TypeError):
                self.bot.send_message(message.chat.id, '⚠️ percent must be between 0 - 100')
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_4,
                                                    exchange_id=exchange_id, coin_id=coin_id,
                                                    analysis_id=analysis_id)

        @self.bot.message_handler(commands=['profile'])
        def profile(message):
            profile_option = types.InlineKeyboardMarkup()
            plan, valid = functions.get_user_plan_profile(chat_id=message.chat.id)
            strategies = functions.get_user_exchanges_strategies_profile(chat_id=message.chat.id)
            accounts = functions.get_user_exchange(chat_id=message.chat.id)
            accounts_dict = "\n"
            strategies_dict = "\n"
            for i, strategy in enumerate(strategies, 1):
                strategies_dict += f"{i}-\t 🪙Coin : {strategy[0]}  📊Analysis: {strategy[1]}\n\t\t" \
                                   f"  💰Amount: {strategy[2]}  🏛Exchange: {strategy[3]}\n\n"

            for account in accounts:
                accounts_dict += f"🔹 {account[0]}\n"

            profile_option.add(types.InlineKeyboardButton('strategies',
                                                          callback_data="user_strategies"),
                               types.InlineKeyboardButton('exchanges',
                                                          callback_data="user_exchanges"),
                               types.InlineKeyboardButton('trade history',
                                                          callback_data="user_history")
                               )

            self.bot.send_message(chat_id=message.chat.id, text=f'💳 Plan:\n🔹{plan}\n⏱ Valid date:  {valid}\n\n'
                                                                f'📊 Strategies: \t{strategies_dict}\n'
                                                                f'🏛 Exchanges: \t{accounts_dict}',
                                  reply_markup=profile_option)

        @self.bot.message_handler(commands=['help'])
        def help_me(message):
            try:
                self.bot.reply_to(message, 'Some help')

            except Exception as e:
                self.bot.reply_to(message, '⛔️ Try again')
                print(e)
