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
from telegram.base import Telegram
import numpy as np
from Conf import analysis_settings
from Analysis.emerald import Emerald
from Analysis.diamond import Diamond
from Analysis.ruby import Ruby
from Analysis.palladium import Palladium
from libraries.data_collector import get_candle_binance as candles
from test.strategy_tester import StrategyTaster
from libraries.definitions import *


from crud.user import CRUDUser

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


class ClientBot(Telegram):
    def __init__(self):
        Telegram.__init__(self)

    def bot_actions(self):

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
