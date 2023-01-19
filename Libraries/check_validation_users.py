from datetime import datetime, timedelta
from time import sleep
import telebot
from Inc import functions

# master bot already run on vps dont use this @aitrdbot -> address
API_KEY = '2123917023:AAFPy9xoaJLt0BxqQJgC3J3F9km8F7ozdn8'
# @testkourosh2bot -> address // use this bot for test your code
# API_KEY = '1978536410:AAE_RMk3-4r_cLnt_nRcEnZHaSp-vIk9oVo'

_bot_ins = telebot.TeleBot(API_KEY)


def delete_user_strategy(bot_ins):
    users = functions.get_users_validation_date()
    today = datetime.now()
    try:
        for user in users:
            valid_day = (user[1] - today).days
            if user[1] < today:
                functions.delete_all_user_strategies(username=user[0])
                bot_ins.send_message(chat_id=int(user[2]), text='your plan was expired!🥵\n'
                                                                'charge your /plan immediately')
                print(functions.set_is_valid_user(username=user[0]))
            elif user[1] < timedelta(days=1) + today:
                bot_ins.send_message(chat_id=int(user[2]), text=f'your plan will expired in {valid_day} day!🥵\n'
                                                                'charge your /plan immediately')
            elif user[1] < timedelta(days=2) + today:

                bot_ins.send_message(chat_id=int(user[2]), text=f'your plan will expired in {valid_day} days!🥵\n'
                                                                'charge your /plan immediately')
            elif user[1] < timedelta(days=3) + today:
                bot_ins.send_message(chat_id=int(user[2]), text=f'your plan will expired in {valid_day} days!🥵\n'
                                                                'charge your /plan immediately')
            elif user[1] < timedelta(days=4) + today:
                bot_ins.send_message(chat_id=int(user[2]), text=f'your plan will expired in {valid_day} days!🥵\n'
                                                                'charge your /plan immediately')
    except Exception as e:
        print(e)


def check_validate_stream():
    while True:
        delete_user_strategy(bot_ins=_bot_ins)
        sleep(28800)
