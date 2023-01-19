""""
Mr.Kataei 11/23/2021

"""
from datetime import datetime
from time import sleep
import os
from telebot import types
from telebot import apihelper
from Auth.register import register
from Inc import functions
from Account.clients import User, BitfinexClient, DemoClient, Nobitex
from Interfaces.telegram import Telegram
import numpy as np
from Conf import analysis_settings
from Analysis.emerald import Emerald
from Analysis.diamond import Diamond
from Analysis.ruby import Ruby
from Analysis.palladium import Palladium
from Libraries.data_collector import get_candle_binance as candles
from Test.strategy_tester import StrategyTaster
from Libraries.definitions import *

apihelper.ENABLE_MIDDLEWARE = True

# @testkourosh2bot -> address // use this bot for test your code
# API_KEY = '1978536410:AAE_RMk3-4r_cLnt_nRcEnZHaSp-vIk9oVo'

timeframe_binance_dictionary = {
    '30min': [(30, 'm'), 1],
    '1hour': [(1, 'h'), 2],
    '4hour': [(4, 'h'), 3],
    '1day': [(1, 'd'), 4],
    '1min': [(1, 'm'), 5],
    '15min': [(15, 'm'), 6]
}


def is_valid_username(s: str):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        if len(s) >= 4 and not s[0].isdigit() and s[0].isalpha() and s.find(' ') < 0:
            return True
        else:
            return False


def get_analysis_class(analysis: str, symbol: str, timeframe_id: int, number: int, unit: str):
    coin_id = functions.get_coin_id(symbol)
    data = candles(symbol=symbol, number=number, unit=unit, limit=1000)

    if not data[0]:
        return None
    else:
        data = data[1]
    if analysis == 'emerald':
        return Emerald(data=data, coin_id=coin_id, timeframe_id=timeframe_id, bot_ins=1).get_recommendations()
    if analysis == 'diamond':
        setting = analysis_settings.get_analysis_setting(coin_id=coin_id, timeframe_id=timeframe_id, analysis_id=3)
        if setting:
            return Diamond(data=data, coin_id=coin_id, timeframe_id=timeframe_id,
                           bot_ins=1, setting=setting, is_back_test=True).get_recommendations()
        else:
            return None
    if analysis == 'ruby':
        return Ruby(data=data, coin_id=coin_id, timeframe_id=timeframe_id,
                    bot_ins=1).get_recommendations()
    if analysis == "palladium":
        setting = analysis_settings.get_analysis_setting(coin_id=coin_id, timeframe_id=timeframe_id, analysis_id=4)
        if setting:
            return Palladium(data=data, coin_id=coin_id, timeframe_id=timeframe_id,
                             setting=setting, bot_ins=1).get_recommendations()
        else:
            return None
    else:
        return None


def get_exchange_class(exchange_id: int, public: str, secret: str, chat_id: str = None):
    if exchange_id == 1:
        return BitfinexClient(public=public, secret=secret)
    elif exchange_id == 2:
        return DemoClient(chat_id=chat_id)
    elif exchange_id == 3:
        return Nobitex(public=public, secret=secret)
    else:
        return None


def start_keyboard():
    key_markup = types.ReplyKeyboardMarkup(row_width=2)
    key_add_account = types.KeyboardButton(trans('C_add_exchange'))
    key_add_strategy = types.KeyboardButton(trans('C_add_strategy'))
    key_tutorials = types.KeyboardButton(trans('C_tutorials'))
    key_plans = types.KeyboardButton(trans('C_plans'))
    key_profile = types.KeyboardButton(trans('C_profile'))
    key_back_test = types.KeyboardButton(trans('C_back_test'))
    key_social = types.KeyboardButton(trans('C_social_medias'))
    key_help = types.KeyboardButton(trans('C_help'))
    key_language = types.KeyboardButton(trans('C_lang'))
    key_markup.add(key_profile, key_help, key_add_account, key_add_strategy, key_back_test, key_tutorials,
                   key_plans, key_language, key_social)
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


def tut_cat_keyboard():
    """
    :return:
    """
    categories = np.array(functions.get_tutorials_categories())
    key_markup = types.ReplyKeyboardMarkup(row_width=1)
    key_markup.add(*categories[:, 1])
    return key_markup


# def back_home_tut():
#     key_markup = types.ReplyKeyboardMarkup(row_width=1)
#     key_markup.add('categories', 'back home')
#     return key_markup


def tut_medias_keyboard(category: str):
    """
    :return:
    """
    medias = np.array(functions.get_tutorials_with_category(category=category))
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keys = []
    for media in medias:
        keys.append(types.InlineKeyboardButton(text=media[0], url=media[1]))
    keyboard.add(*keys)
    return keyboard


def social_keyboard():
    """
    :return:
    """
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.add(types.InlineKeyboardButton(text=trans("C_instagram"),
                                            url='https://instagram.com/aitrdbot?utm_medium=copy_link'),
                 types.InlineKeyboardButton(text=trans("C_telegram"),
                                            url='https://t.me/aitrdrbot'),
                 types.InlineKeyboardButton(text=trans("C_twitter"),
                                            url='https://twitter.com/aitrdbot?s=21'))
    return keyboard


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


def generate_profile_show_message(chat_id: str):
    """
    :param chat_id:
    :return:
    """
    plan, valid = functions.get_user_plan_profile(chat_id=chat_id)
    strategies = functions.get_user_exchanges_strategies_profile(chat_id=chat_id)
    accounts = functions.get_user_exchange(chat_id=chat_id)
    accounts_dict = "\n\n"
    strategies_dict = "\n\n"
    for i, strategy in enumerate(strategies, 1):
        strategies_dict += f"{i}-\n {trans('C_coin')} : {strategy[0]}\n{trans('C_analysis')}: {strategy[1]}\n" \
                           f"{trans('C_percent_usd')}: {strategy[2]}%\n{trans('C_exchange')}: {strategy[3]}\n\n"

    for account in accounts:
        accounts_dict += f"🔹 {account[0]}"

    return plan, valid, strategies_dict, accounts_dict


def dont_understand(message):
    commands = ['/lang', '/exchange', '/strategy', '/test', '/start', '/plans', '/profile', '/tutorial',
                '/help', trans('C_social_medias'),
                trans('C_plans'), trans('C_back_test'), trans('C_profile'), trans('C_tutorials'),
                trans('C_add_exchange'), trans('C_add_strategy'), trans('C_lang'), trans('C_help')]

    if message.text not in commands or message.content_type != 'text':
        return True
    else:
        return False


def get_exchanges():
    return np.array(functions.get_exchanges())


def get_coins():
    return np.array(functions.get_coins())


def get_analysis():
    return np.array(functions.get_analysis())


def get_timeframes():
    return np.array(functions.get_timeframes())


def get_tut_cat():
    return np.array(functions.get_tutorials_categories())


class ClientBot(Telegram):
    def __init__(self):
        Telegram.__init__(self)
        # self.tut_cat = np.array(functions.get_tutorials_categories())

    def is_valid_user(self, message):
        user = functions.get_user(message.chat.id)
        if not user:
            self.bot.send_message(message.chat.id, trans('C_sorry_signup'))
            return False
        else:
            result = functions.check_expire_plan(chat_id=message.chat.id)
            if result:
                self.bot.send_message(message.chat.id, trans('C_expire_plan'))
                return False
            else:
                return True

    def can_start_bot(self, message):
        if message.chat.id in self.user_dict:
            return False
        else:
            self.bot.send_message(message.chat.id, trans('C_please_start'))
            return True

    def is_valid_command(self, message):
        if not self.can_start_bot(message=message) and self.is_valid_user(message=message):
            return True
        else:
            return False

    def check_add_command(self, message):
        if message.text == trans('C_add_strategy') or message.text == '/strategy':
            if self.is_valid_command(message=message):
                user = self.user_dict[message.chat.id]
                user.update_user_plan_limit()
                if user.strategy > len(functions.get_user_watchlist(username=user.username)):
                    return True
                else:
                    self.bot.send_message(message.chat.id, trans('C_full_strategies'))
                    return False
            else:
                return False
        else:
            return False

    def check_setup_command(self, message):
        if message.text == trans('C_add_exchange') or message.text == '/exchange':
            if self.is_valid_command(message=message):
                user = self.user_dict[message.chat.id]
                user.update_user_plan_limit()
                if user.account > len(functions.get_user_exchange(chat_id=message.chat.id)):
                    return True
                else:
                    self.bot.send_message(message.chat.id, trans('C_full_exchanges'))
                    return False
            else:
                return False
        else:
            return False

    def tutorial_command(self, message):
        if message.text == trans('C_tutorials') or message.text == '/tutorial':
            if self.is_valid_command(message=message):
                return True
            else:
                return False
        else:
            return False

    def profile_command(self, message):
        if message.text == trans('C_profile') or message.text == '/profile':
            if self.is_valid_command(message=message):
                return True
            else:
                return False
        else:
            return False

    def back_test_command(self, message):
        if message.text == trans('C_back_test') or message.text == '/test':
            if self.is_valid_command(message=message):
                return True
            else:
                return False
        else:
            return False

    def plan_command(self, message):
        if message.text == trans('C_plans') or message.text == '/plans':
            if self.is_valid_command(message=message):
                return True
            else:
                return False
        else:
            return False

    def lang_command(self, message):
        if message.text == trans('C_lang') or message.text == '/lang':
            if self.is_valid_command(message=message):
                return True
            else:
                return False
        else:
            return False

    def bot_actions(self):
        @self.bot.middleware_handler(update_types=['message'])
        def activate_language(bot_instance, message):
            try:
                user_lang = self.user_dict[message.chat.id].lang
            except Exception as e:
                user_lang = message.from_user.language_code
            activate(user_lang)

        @self.bot.callback_query_handler(func=lambda call: self.is_valid_command(call.message))
        def query_handler(call):

            if call.data == "profile_edit_strategies":
                strategies = functions.get_user_exchanges_strategies_profile(chat_id=call.message.chat.id)
                if len(strategies) == 0:
                    self.bot.send_message(chat_id=call.message.chat.id, text=trans("C_any_strategies"))
                else:
                    for strategy in strategies:
                        strategies_option = types.InlineKeyboardMarkup(row_width=2)
                        strategies_option.add(types.InlineKeyboardButton(trans('C_edit'),
                                                                         callback_data=str(strategy[4]) +
                                                                                       "_edit_strategy"),
                                              types.InlineKeyboardButton(trans('C_delete'),
                                                                         callback_data=str(strategy[4]) +
                                                                                       "_delete_strategy")
                                              )
                        self.bot.send_message(chat_id=call.message.chat.id,
                                              text=f'{trans("C_coin")}: {strategy[0]}\n'
                                                   f'{trans("C_analysis")}: {strategy[1]}\n'
                                                   f'{trans("C_percent_usd")}: {strategy[2]}\n'
                                                   f'{trans("C_exchange")}: {strategy[3]}\n',
                                              reply_markup=strategies_option)

            elif call.data == "profile_edit_exchanges":
                accounts = functions.get_user_exchange(chat_id=call.message.chat.id)
                if len(accounts) == 0:
                    self.bot.send_message(chat_id=call.message.chat.id, text=trans("C_any_exchanges"))
                else:
                    for account in accounts:
                        # for show asset each exchange
                        public, secret = functions.get_user_api(int(account[1]))
                        exchange_client = get_exchange_class(exchange_id=int(account[2]), public=public, secret=secret,
                                                             chat_id=call.message.chat.id)
                        result_message = f'{trans("C_assets")}:\n'
                        if exchange_client is not None:
                            assets = exchange_client.get_assets()
                            if not assets[0]:
                                assets = assets[1]
                                for asset in assets:
                                    result_message += f'🪙 {asset[1]}\n 💎 {str(asset[2])}\n'
                            else:
                                result_message = trans("C_active")

                        accounts_option = types.InlineKeyboardMarkup(row_width=2)
                        accounts_option.add(types.InlineKeyboardButton(trans('C_edit'),
                                                                       callback_data=str(account[1]) +
                                                                                     "_edit_account"),
                                            types.InlineKeyboardButton(trans("C_invoke"),
                                                                       callback_data=str(account[1]) +
                                                                                     "_invoke_account")
                                            )
                        self.bot.send_message(chat_id=call.message.chat.id, text=f"🔹 {account[0]}\n{result_message}",
                                              reply_markup=accounts_option)

            elif call.data == "profile_show_history":
                histories = functions.get_user_trade_history(chat_id=call.message.chat.id)
                if len(histories) == 0:
                    self.bot.send_message(chat_id=call.message.chat.id, text=trans("C_any_trades"))
                else:
                    result_message = trans('C_trade_history')
                    for history in histories:
                        result_message += f'🔹{trans("C_date")}: {history[0]}\n {trans("C_exchange")}: {history[1]}\n ' \
                                          f'{trans("C_analysis")}: {history[2]}\n{trans("C_coin")}: {history[3]}\n' \
                                          f'{trans("C_price")}: {history[4]}\n' \
                                          f'{trans("C_position")}: {history[5]}\n' \
                                          f'{trans("C_order_status")}: {history[6]}\n' \
                                          f'{trans("C_status")}: {history[7]}\n' \
                                          f'{trans("C_percent_usd")}: {history[8]}% \n' \
                                          f'{trans("C_submit_order_time")}: {history[9]}\n' \
                                          f'{trans("C_receive_signal_time")}: {history[10]}\n\n'

                    self.bot.send_message(chat_id=call.message.chat.id, text=result_message,
                                          reply_markup=start_keyboard())

            elif "_delete_strategy" in call.data:
                query = str(call.data).split('_')
                functions.delete_strategy(strategy_id=int(query[0]))
                self.bot.send_message(chat_id=call.message.chat.id, text=trans("C_done"),
                                      reply_markup=start_keyboard())
                self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

            elif "_edit_strategy" in call.data:
                query = str(call.data).split('_')
                add_strategy(message=call.message, watchlist_id=int(query[0]))
                self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

            elif "_edit_account" in call.data:
                query = str(call.data).split('_')
                add_exchange(message=call.message, user_setting_id=int(query[0]))
                self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

            elif "_invoke_account" in call.data:
                query = str(call.data).split('_')
                functions.update_user_exchange(user_setting_id=int(query[0]), public='none', secret='none')
                self.bot.send_message(chat_id=call.message.chat.id, text=f'{trans("C_done")}\n',
                                      reply_markup=start_keyboard())
                self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

            elif "language" in call.data:
                query = str(call.data).split('_')
                if query[0] == 'english':
                    self.user_dict[call.message.chat.id].lang = 'en'
                    query[0] = 'English'
                elif query[0] == 'persian':
                    query[0] = 'فارسی'
                    self.user_dict[call.message.chat.id].lang = 'fa'
                activate_language('', call.message)
                self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
                self.bot.send_message(chat_id=call.message.chat.id, text=f'{trans("C_done")}\n'
                                                                         f' {query[0]} {trans("C_was_selected")}',
                                      reply_markup=start_keyboard())

            # self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        @self.bot.message_handler(commands=['start'], func=self.can_start_bot)
        def welcome(message):
            user = functions.get_user(message.chat.id)
            # activate_language('', message)
            markup = start_keyboard()
            self.user_dict[message.chat.id] = User(message=message)  # create object for register user session
            if not user:
                # is typing bot ..
                self.bot.send_chat_action(chat_id=message.chat.id, action="typing")
                sleep(1)

                self.bot.send_message(message.chat.id, trans('C_hey') + message.chat.first_name + "!\n" +
                                      trans('C_welcome'), reply_markup=markup)
                # if user deleted telegram account need develop
                keyboard = types.ReplyKeyboardMarkup()
                reg_button = types.KeyboardButton(text=trans("C_share_contact"), request_contact=True)
                keyboard.add(reg_button)
                self.bot.send_message(message.chat.id, trans("C_reg_with_phone"),
                                      reply_markup=keyboard)
            else:
                self.user_dict[message.chat.id].username = user[0][0]
                if self.is_valid_user(message=message):
                    functions.update_user_online(username=user[0][0], online=True)
                    self.bot.send_message(message.chat.id, trans("C_can_i_help"), reply_markup=markup)

        @self.bot.message_handler(content_types=['contact'],
                                  func=lambda message: functions.is_user_signup(message.chat.id))
        def register_handler(message):
            markup = types.ReplyKeyboardRemove(selective=False)
            self.bot.send_message(message.chat.id, trans("C_enter_username"), reply_markup=markup)
            self.bot.register_next_step_handler(message=message, callback=reg_step_1,
                                                phone=message.contact.phone_number)

        def reg_step_1(message, phone: str):
            user = self.user_dict[message.chat.id]
            username = str(message.text).lower()
            try:
                if functions.check_username_exist(username=username):
                    self.bot.send_message(message.chat.id, trans('C_exist_username'))
                    self.bot.register_next_step_handler(message=message, callback=reg_step_1,
                                                        phone=phone)
                elif message.content_type == 'text' and is_valid_username(username):
                    user.username = username
                    error, detail = register(username=username, chat_id=user.chat_id, phone=phone)
                    if error:
                        self.bot.reply_to(message, trans('C_try_again'))
                    else:
                        functions.update_user_online(username=user.username, online=True)
                        markup = start_keyboard()
                        self.bot.send_message(message.chat.id, trans('C_account_created'), reply_markup=markup)
                else:
                    self.bot.send_message(message.chat.id, trans('C_invalid_username'))
                    self.bot.register_next_step_handler(message=message, callback=reg_step_1,
                                                        phone=phone)

            except Exception as e:
                self.bot.reply_to(message, trans('C_try_again'))

        @self.bot.message_handler(func=self.check_setup_command)
        def add_exchange(message, user_setting_id: int = 0):
            try:
                key_markup = exchanges_keyboard()
                self.bot.send_message(message.chat.id, trans("C_choose_exchange"),
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_1,
                                                    user_setting_id=user_setting_id)

            except Exception as e:
                self.bot.reply_to(message, trans("C_error"), reply_markup=start_keyboard())

        def add_exchange_step_1(message, user_setting_id: int):
            if message.text == 'demo':
                user = self.user_dict[message.chat.id]
                markup = start_keyboard()
                if user_setting_id == 0:
                    error, result = functions.set_user_setting(username=str(user.username),
                                                               exchange_id=2,
                                                               public='public', secret='secret')
                    functions.create_demo_account(str(user.username))
                    if error:
                        self.bot.send_message(message.chat.id, trans("C_demo_exist"), reply_markup=markup)
                    else:
                        self.bot.send_message(message.chat.id, trans('C_demo_created'), reply_markup=markup)
                else:
                    if functions.get_demo_account_assets(chat_id=message.chat.id) is not None:
                        functions.create_demo_account(str(user.username))
                    result = functions.update_user_exchange(user_setting_id=int(user_setting_id),
                                                            exchange_id=2,
                                                            public='public', secret='secret')

                    self.bot.delete_message(message.chat.id, message.message_id)
                    if result is None:
                        self.bot.send_message(message.chat.id, trans("C_demo_created"), reply_markup=markup)
                    else:
                        self.bot.send_message(message.chat.id, trans("C_same_exchange"), markup)

            else:
                try:
                    exchanges = get_exchanges()
                    exchanges_id = np.where(exchanges[:, 1] == message.text)[0][0]
                    key_markup = types.ReplyKeyboardRemove(selective=False)
                    exchanges_id = int(exchanges[exchanges_id][0])
                    if exchanges_id == 3:
                        self.bot.send_message(message.chat.id, trans("C_enter_token"), reply_markup=key_markup)
                    else:
                        self.bot.send_message(message.chat.id, trans("C_enter_public_key"), reply_markup=key_markup)
                    self.bot.register_next_step_handler(message=message, callback=add_exchange_step_2,
                                                        exchange_id=exchanges_id,
                                                        user_setting_id=user_setting_id)
                except IndexError:
                    self.bot.send_message(message.chat.id, trans("C_wrong_exchange"), reply_markup=exchanges_keyboard())
                    self.bot.register_next_step_handler(message=message, callback=add_exchange_step_1,
                                                        user_setting_id=user_setting_id)

        def add_exchange_step_2(message, exchange_id: int, user_setting_id: int):
            if message.content_type == 'text':
                if exchange_id == 3:
                    add_exchange_step_3(message=message, exchange_id=3, public=message.text,
                                        user_setting_id=user_setting_id)

                else:
                    self.bot.send_message(message.chat.id, trans("C_enter_secret_key"))
                    self.bot.register_next_step_handler(message=message, callback=add_exchange_step_3,
                                                        exchange_id=exchange_id, public=message.text,
                                                        user_setting_id=user_setting_id)
                    self.bot.delete_message(message.chat.id, message.message_id)
            else:
                self.bot.send_message(message.chat.id, trans("C_wrong_API"))
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_2,
                                                    exchange_id=exchange_id,
                                                    user_setting_id=user_setting_id)

        def add_exchange_step_3(message, exchange_id: int, public: str, user_setting_id: int):
            if message.content_type == 'text':
                exchange_client = get_exchange_class(exchange_id=int(exchange_id), public=public, secret=message.text,
                                                     chat_id=message.chat.id)
                markup = start_keyboard()
                if exchange_client is not None:
                    assets = exchange_client.get_assets()
                    if assets[0]:
                        self.bot.send_message(message.chat.id, trans("C_wrong_API"), reply_markup=markup)
                    else:
                        assets = assets[1]
                        result_message = f'{trans("C_assets")}:\n'
                        for asset in assets:
                            result_message += f'🪙 {asset[1]}\n 💎 {str(asset[2])}\n\n'
                        self.bot.send_message(message.chat.id, result_message)
                        user = self.user_dict[message.chat.id]
                        # insert database
                        if user_setting_id == 0:
                            error, result = functions.set_user_setting(username=str(user.username),
                                                                       exchange_id=int(exchange_id),
                                                                       public=str(public), secret=str(message.text))
                            self.bot.delete_message(message.chat.id, message.message_id)
                            if error:
                                self.bot.send_message(message.chat.id, trans("C_something_wrong"), reply_markup=markup)
                            else:
                                self.bot.send_message(message.chat.id, trans("C_success"), reply_markup=markup)
                        else:
                            result = functions.update_user_exchange(user_setting_id=int(user_setting_id),
                                                                    exchange_id=int(exchange_id),
                                                                    public=str(public), secret=str(message.text))
                            self.bot.delete_message(message.chat.id, message.message_id)
                            if result is None:
                                self.bot.send_message(message.chat.id, trans("C_success"), reply_markup=markup)
                            else:
                                self.bot.send_message(message.chat.id, trans("C_same_exchange"),
                                                      reply_markup=markup)
                else:
                    self.bot.send_message(message.chat.id, trans("C_unsupported_exchange"),
                                          reply_markup=start_keyboard())
            else:
                self.bot.send_message(message.chat.id, trans("C_wrong_API"))
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_3,
                                                    exchange_id=exchange_id, public=public,
                                                    user_setting_id=user_setting_id)

        @self.bot.message_handler(func=self.back_test_command)
        def back_test(message):
            try:
                key_markup = analysis_keyboard()
                self.bot.send_message(message.chat.id, trans("C_choose_analysis"), reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=back_test_step_1)

            except Exception:
                self.bot.reply_to(message, trans("C_error"), reply_markup=start_keyboard())

        def back_test_step_1(message):
            try:
                analysis = get_analysis()
                analysis_id = np.where(analysis[:, 1] == message.text)[0][0]
                description = functions.get_analysis(analysis_id=int(analysis[analysis_id][0]))[0][2]
                self.bot.send_message(message.chat.id, description)
                key_markup = coins_keyboard()
                self.bot.send_message(message.chat.id, trans("C_choose_coin"), reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=back_test_step_2,
                                                    analysis=analysis[analysis_id][1])
            except IndexError:
                self.bot.send_message(message.chat.id, trans("C_wrong_analysis"), reply_markup=analysis_keyboard())
                self.bot.register_next_step_handler(message=message, callback=back_test_step_1)

        def back_test_step_2(message, analysis: str):
            try:
                coins = get_coins()
                coin_id = np.where(coins[:, 1] == message.text)[0][0]
                key_markup = timeframe_keyboard()
                self.bot.send_message(message.chat.id, trans("C_choose_timeframe"), reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=back_test_step_3,
                                                    analysis=analysis, coin=coins[coin_id][1])

            except IndexError:
                self.bot.send_message(message.chat.id, trans("C_wrong_coin"), reply_markup=coins_keyboard())
                self.bot.register_next_step_handler(message=message, callback=back_test_step_2,
                                                    analysis=analysis)

        def back_test_step_3(message, analysis: str, coin: str):
            try:
                timeframes = get_timeframes()
                timeframe_id = np.where(timeframes[:, 1] == message.text)[0][0]
                key_markup = types.ReplyKeyboardRemove(selective=False)
                self.bot.send_message(message.chat.id, trans("C_initial_value_back_test"), reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=back_test_step_4,
                                                    analysis=analysis, coin=coin,
                                                    timeframe=timeframes[timeframe_id][1])
            except IndexError:
                self.bot.send_message(message.chat.id, trans("C_wrong_timeframe"), reply_markup=timeframe_keyboard())
                self.bot.register_next_step_handler(message=message, callback=back_test_step_3,
                                                    analysis=analysis, coin=coin)

        def back_test_step_4(message, analysis: str, coin: str, timeframe: str):
            try:
                amount = float(message.text)
                if not 0 < amount:
                    self.bot.send_message(message.chat.id, trans("C_warning_amount_back_test"))
                    self.bot.register_next_step_handler(message=message, callback=back_test_step_4,
                                                        analysis=analysis, coin=coin,
                                                        timeframe=timeframe)
                else:
                    timeframe_data = timeframe_binance_dictionary[timeframe]
                    timeframe_id = timeframe_data[1]
                    number, unit = timeframe_data[0]
                    self.bot.send_message(message.chat.id, trans("C_processing"))
                    try:
                        recommendation = get_analysis_class(analysis=analysis, symbol=coin,
                                                            timeframe_id=timeframe_id, number=number, unit=unit)
                    except Exception as e:
                        recommendation = None
                    markup = start_keyboard()
                    if recommendation is None:
                        result = trans("C_wrong_setting_back_test")
                    else:
                        try:
                            result = StrategyTaster(name='telegram', symbol=coin, timeframe=timeframe,
                                                    dataframe=recommendation, initial_value=int(amount))
                            user = self.user_dict[message.chat.id]
                            user = user.username
                            file_name = f'trades-{analysis}-{timeframe}' \
                                        f'-{coin}-{user}-{datetime.now()}.csv'
                            result.trades_list.to_csv(file_name)
                            path = os.getcwd()  # get path now directory
                            doc = open(path + '/' + file_name, 'rb')
                            self.bot.send_document(message.chat.id, doc)
                            os.remove(path + '/' + file_name)
                            result = result.result.values[0]
                            result = f'🪙 *{result[1]}*\n⏰ *{result[2]}*\n{trans("C_start_time")}: *{result[3]}*\n' \
                                     f'{trans("C_end_time")}: *{result[4]}*\n' \
                                     f'{trans("C_positive")}: *{result[5]}*\n' \
                                     f'{trans("C_total_trades")}: *{result[6]}*\n' \
                                     f'{trans("C_total_trade_accuracy")}: *{result[7]}*%\n' \
                                     f'{trans("C_net_profit_percent")}: *{result[8]}*%\n' \
                                     f'{trans("C_average_trade_profit")}: *{result[9]}*%\n' \
                                     f'{trans("C_profit_per_coin")}: *{result[10]}*%\n ' \
                                     f'{trans("C_final_amount")}: *{result[11]}*$'
                        except Exception as e:
                            result = trans("C_something_wrong")
                    self.bot.send_message(message.chat.id, result, reply_markup=markup, parse_mode='Markdown')

            except (ValueError, TypeError):
                self.bot.send_message(message.chat.id, trans("C_warning_amount_back_test"))
                self.bot.register_next_step_handler(message=message, callback=back_test_step_4,
                                                    analysis=analysis, coin=coin,
                                                    timeframe=timeframe)

        @self.bot.message_handler(func=self.check_add_command)
        def add_strategy(message, watchlist_id: int = 0):
            try:
                key_markup = user_exchanges_account_keyboard(message=message)
                if key_markup:
                    self.bot.send_message(message.chat.id, trans("C_choose_exchange"),
                                          reply_markup=key_markup)
                    self.bot.register_next_step_handler(message=message, callback=add_strategy_step_1,
                                                        watchlist_id=watchlist_id)
                else:
                    self.bot.send_message(message.chat.id, trans("C_warning_set_exchange_first"),
                                          reply_markup=start_keyboard())

            except Exception as e:
                self.bot.reply_to(message, trans("C_error"), reply_markup=start_keyboard())

        def add_strategy_step_1(message, watchlist_id: int = 0):
            try:
                exchanges = get_exchanges()
                exchanges_id = np.where(exchanges[:, 1] == message.text)[0][0]

                key_markup = analysis_keyboard()
                self.bot.send_message(message.chat.id, trans("C_choose_analysis"),
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_2,
                                                    exchange_id=exchanges[exchanges_id][0],
                                                    watchlist_id=watchlist_id)
            except IndexError:
                self.bot.send_message(message.chat.id, trans("C_wrong_exchange"), reply_markup=exchanges_keyboard())
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_1,
                                                    watchlist_id=watchlist_id)

        def add_strategy_step_2(message, exchange_id: int, watchlist_id: int = 0):
            try:
                analysis = get_analysis()
                analysis_id = np.where(analysis[:, 1] == message.text)[0][0]
                key_markup = coins_keyboard()
                self.bot.send_message(message.chat.id, trans("C_choose_coin"),
                                      reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_3,
                                                    exchange_id=exchange_id, analysis_id=analysis[analysis_id][0],
                                                    watchlist_id=watchlist_id)
            except IndexError:
                self.bot.send_message(message.chat.id, trans("C_wrong_analysis"), reply_markup=analysis_keyboard())

                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_2,
                                                    exchange_id=exchange_id, watchlist_id=watchlist_id)

        def add_strategy_step_3(message, exchange_id: int, analysis_id: int, watchlist_id: int = 0):
            try:
                coins = get_coins()
                coin_id = np.where(coins[:, 1] == message.text)[0][0]
                key_markup = types.ReplyKeyboardRemove(selective=False)
                self.bot.send_message(message.chat.id, trans("C_enter_percent_usd"), reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_4,
                                                    exchange_id=exchange_id, analysis_id=analysis_id,
                                                    coin_id=coins[coin_id][0],
                                                    watchlist_id=watchlist_id)
            except IndexError:
                self.bot.send_message(message.chat.id, trans("C_wrong_coin"), reply_markup=coins_keyboard())
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_3,
                                                    exchange_id=exchange_id, analysis_id=analysis_id,
                                                    watchlist_id=watchlist_id)

        def add_strategy_step_4(message, exchange_id: int, coin_id: int, analysis_id: int, watchlist_id: int = 0):
            user = self.user_dict[message.chat.id]
            try:
                percent = float(message.text)
                if not 0 < percent <= 100:
                    self.bot.send_message(message.chat.id, trans("C_warning_percent_usd"))
                    self.bot.register_next_step_handler(message=message, callback=add_strategy_step_4,
                                                        exchange_id=exchange_id, coin_id=coin_id,
                                                        analysis_id=analysis_id, watchlist_id=watchlist_id)
                else:
                    markup = start_keyboard()
                    setting_id = functions.get_user_settings_id(chat_id=message.chat.id,
                                                                exchange_id=exchange_id)[0][0]
                    if watchlist_id == 0:
                        error, result = functions.set_watchlist(user_setting_id=int(setting_id), coin_id=int(coin_id),
                                                                username=user.username, analysis_id=int(analysis_id),
                                                                amount=percent)
                        if error:
                            self.bot.send_message(message.chat.id, trans("C_exist_strategy"), reply_markup=markup)
                        else:
                            self.bot.send_message(message.chat.id, trans("C_success"), reply_markup=markup)
                    else:
                        result = functions.update_user_strategy(user_setting_id=int(setting_id), coin_id=int(coin_id),
                                                                analysis_id=int(analysis_id), amount=percent,
                                                                watchlist_id=watchlist_id)
                        if result is None:
                            self.bot.send_message(message.chat.id, trans("C_success"), reply_markup=markup)
                        else:
                            self.bot.send_message(message.chat.id, trans("C_exist_strategy"), reply_markup=markup)
            except (ValueError, TypeError):
                self.bot.send_message(message.chat.id, trans("C_warning_percent_usd"))
                self.bot.register_next_step_handler(message=message, callback=add_strategy_step_4,
                                                    exchange_id=exchange_id, coin_id=coin_id,
                                                    analysis_id=analysis_id, watchlist_id=watchlist_id)

        @self.bot.message_handler(func=self.profile_command)
        def profile(message):
            profile_option = types.InlineKeyboardMarkup(row_width=2)
            plan, valid, strategies_dict, accounts_dict = generate_profile_show_message(chat_id=message.chat.id)
            profile_option.add(types.InlineKeyboardButton(trans("C_strategies"),
                                                          callback_data="profile_edit_strategies"),
                               types.InlineKeyboardButton(trans('C_assets_exchange'),
                                                          callback_data="profile_edit_exchanges"),
                               types.InlineKeyboardButton(trans("C_trades_history"),
                                                          callback_data="profile_show_history")
                               )
            self.bot.send_message(chat_id=message.chat.id, text=f'{trans("C_plan")}:\n🔹{plan}\n'
                                                                f'{trans("C_valid_date")}:  {valid}\n\n'
                                                                f'{trans("C_strategies")}: \t{strategies_dict}\n'
                                                                f'{trans("C_exchanges")}: \t{accounts_dict}',
                                  reply_markup=profile_option)

        @self.bot.message_handler(func=self.tutorial_command)
        def tutorials(message):
            try:
                self.bot.send_message(message.chat.id, trans('C_coming_soon'), reply_markup=start_keyboard())

                # key_markup = tut_cat_keyboard()
                # self.bot.send_message(message.chat.id, '📚  Please Select tutorial category',
                #                       reply_markup=key_markup)
                # self.bot.register_next_step_handler(message=message, callback=show_tutorial_step_1)

            except Exception as e:
                self.bot.send_message(message, trans("C_error"), reply_markup=start_keyboard())

        # def show_tutorial_step_1(message):
        #     try:
        #         category_id = np.where(self.tut_cat[:, 1] == message.text)[0][0]
        #         key_markup = tut_medias_keyboard(category=self.tut_cat[category_id][1])
        #         self.bot.send_message(message.chat.id, '📼  Download any tutorial you want',
        #                               reply_markup=key_markup)
        #         back_tut_keyboard = back_home_tut()
        #         self.bot.send_message(message.chat.id, '🤓  Enjoy',
        #                               reply_markup=back_tut_keyboard)
        #         self.bot.register_next_step_handler(message=message, callback=back_tut)
        #
        #     except IndexError:
        #         self.bot.send_message(message.chat.id, '⛔️ wrong category')
        #         self.bot.register_next_step_handler(message=message, callback=show_tutorial_step_1)
        #
        # def back_tut(message):
        #     if message.text == 'back home':
        #         welcome(message=message)
        #     elif message.text == 'categories':
        #         self.bot.register_next_step_handler(message=message, callback=tutorials)
        #
        #     else:
        #         self.bot.register_next_step_handler(message=message, callback=back_tut)

        @self.bot.message_handler(func=lambda message: message.text == trans('C_social_medias'))
        def social_media(message):
            try:
                key_markup = social_keyboard()
                self.bot.send_message(message.chat.id, trans("C_follow_us"),
                                      reply_markup=key_markup)

            except Exception as e:
                self.bot.reply_to(message, trans("C_try_again"), reply_markup=start_keyboard())

        @self.bot.message_handler(func=lambda message: message.text == trans('C_help') or message.text == '/help')
        def help_me(message):
            try:
                self.bot.reply_to(message, trans("C_help_message"), parse_mode='Markdown')

            except Exception as e:
                self.bot.reply_to(message, trans("C_try_again"), reply_markup=start_keyboard())

        @self.bot.message_handler(func=self.plan_command)
        def plan_charge(message):
            try:
                self.bot.reply_to(message, trans("C_charge_plan"))

            except Exception as e:
                self.bot.reply_to(message, trans("C_try_again"), reply_markup=start_keyboard())

        @self.bot.message_handler(func=self.lang_command)
        def plan_charge(message):
            try:
                lang_option = types.InlineKeyboardMarkup(row_width=2)
                lang_option.add(types.InlineKeyboardButton('English',
                                                           callback_data="english_language"),
                                types.InlineKeyboardButton('فارسی',
                                                           callback_data="persian_language")
                                )
                self.bot.send_message(chat_id=message.chat.id, text=trans("C_choose_language"),
                                      reply_markup=lang_option)
            except Exception as e:
                self.bot.reply_to(message, trans("C_try_again"), reply_markup=start_keyboard())

        @self.bot.message_handler(func=dont_understand)
        def excuse(message):
            self.bot.send_message(message.chat.id, trans("C_dont_understand"), reply_markup=start_keyboard())
