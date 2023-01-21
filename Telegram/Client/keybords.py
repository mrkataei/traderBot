from Libraries.definitions import *
from telebot import types


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

def exchange_keyboard():
    key_markup = types.ReplyKeyboardMarkup(row_width=1)
    key_binance = types.KeyboardButton("binance")
    key_kocoin = types.KeyboardButton("kocoin")
    key_bitfinex = types.KeyboardButton("bitfinex")
    key_markup.add(key_binance, key_kocoin, key_bitfinex)
    
    return key_markup
