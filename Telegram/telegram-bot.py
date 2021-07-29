import os
import telebot
from time import sleep
from binance.client import Client
import pandas as pd

client = Client()
symbol = []
# API_KEY = os.getenv('API_KEY')
API_KEY = '1936293973:AAFLKY0TCP9qEMjqPDrewsdzGisNSQmB0ds'
bot = telebot.TeleBot(API_KEY)
users = []

class Var:
    def __init__(self):
        self.timeframe = client.KLINE_INTERVAL_1MINUTE
    def get_timeframe(self):
        return self.timeframe
    def set_timeframe(self , timeframe:str):
        self.timeframe = timeframe

timefr = Var()
def check_users(username: str):
    if users:  # first init
        for user in users:
            if user == username:
                return False
            else:
                return True
    else:
        return True

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")
    sleep(1)
    bot.reply_to(message, "Hey " + message.chat.first_name + "!\n" +
                 "I am Aran , your trade assistance \n"
                 "/help show commands")
    # send notif to admin
    try:
        if message.chat.username:
            users.append(message.chat.username) if check_users(message.chat.username) else print("user already exist")
            bot.send_message(chat_id=1210507821, text="Hi Admin!\n" + "@" + message.chat.username + " just join now")
        else:
            users.append("N.U." + message.chat.first_name) if check_users(message.chat.first_name) else print(
                "user already exist")
            bot.send_message(chat_id=1210507821, text="Hi Admin!\n" + message.chat.first_name + " just join now")
        print(users)
    except:
        print("Unblock Bot Admin 😐")


@bot.message_handler(commands=['help'])
def help_me(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")
    sleep(1)
    bot.reply_to(message, "price <symbol> show last \n"
                          "candle <symbol> show last candle")


@bot.message_handler(commands=['frame'])
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='1min', callback_data=client.KLINE_INTERVAL_1MINUTE))
    markup.add(telebot.types.InlineKeyboardButton(text='3min', callback_data=client.KLINE_INTERVAL_3MINUTE))
    markup.add(telebot.types.InlineKeyboardButton(text='5min', callback_data=client.KLINE_INTERVAL_5MINUTE))
    markup.add(telebot.types.InlineKeyboardButton(text='15min', callback_data=client.KLINE_INTERVAL_15MINUTE))
    markup.add(telebot.types.InlineKeyboardButton(text='30min', callback_data=client.KLINE_INTERVAL_30MINUTE))
    markup.add(telebot.types.InlineKeyboardButton(text='1hour', callback_data=client.KLINE_INTERVAL_1HOUR))
    markup.add(telebot.types.InlineKeyboardButton(text='2hour', callback_data=client.KLINE_INTERVAL_2HOUR))
    markup.add(telebot.types.InlineKeyboardButton(text='4hour', callback_data=client.KLINE_INTERVAL_4HOUR))
    markup.add(telebot.types.InlineKeyboardButton(text='6hour', callback_data=client.KLINE_INTERVAL_6HOUR))
    markup.add(telebot.types.InlineKeyboardButton(text='8hour', callback_data=client.KLINE_INTERVAL_8HOUR))
    markup.add(telebot.types.InlineKeyboardButton(text='12hour', callback_data=client.KLINE_INTERVAL_12HOUR))
    markup.add(telebot.types.InlineKeyboardButton(text='daily', callback_data=client.KLINE_INTERVAL_1DAY))
    markup.add(telebot.types.InlineKeyboardButton(text='3day', callback_data=client.KLINE_INTERVAL_3DAY))
    markup.add(telebot.types.InlineKeyboardButton(text='weekly', callback_data=client.KLINE_INTERVAL_1WEEK))
    markup.add(telebot.types.InlineKeyboardButton(text='monthly', callback_data=client.KLINE_INTERVAL_1MONTH))
    bot.send_message(message.chat.id, text="Choose your timeframe !", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='Timeframe has been set!')
    timefr.set_timeframe(call.data)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

def stock_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in "price":
        return False
    else:
        return True


@bot.message_handler(func=stock_request)
def send_price(message):
    request = str(message.text.split()[1]).upper()
    try:
        data = client.get_symbol_ticker(symbol=request)["price"]
        if data:
            bot.send_message(message.chat.id, data)
        else:
            bot.send_message(message.chat.id, "No data!?")
    except:
        bot.send_message(message.chat.id, "Invalid symbol please try again ")


def candle_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in "candle":
        return False
    else:
        return True


@bot.message_handler(func=candle_request)
def send_candle(message):
    timeframe = timefr.get_timeframe()
    request = str(message.text.split()[1]).upper()
    try:
        data = pd.DataFrame(client.get_klines(symbol=request, interval= timeframe, limit=1)).values
        time = pd.to_datetime(data[0, 0], unit='ms', yearfirst=True).tz_localize('UTC').tz_convert('Asia/Tehran')
        if data[0, 1] <= data[0, 4]:
            percent = (float(data[0, 4]) - float(data[0, 1])) * 100 / float(data[0, 1])
            percent = round(percent, 3)
            text = "🤑" + request + "\n🟢" + str(percent) + "%\n" + "⏱Timeframe: "+timeframe +"\n"+ "Open time : " + str(
                time) + "\n" + "Open : " + str(data[0, 1]) + \
                   "\n" + "High : " + str(data[0, 2]) + "\n" + "Low : " + str(data[0, 3]) + "\n" + "Close : " + str(
                data[0, 4]) + \
                   "\n" + "Volume : " + str(data[0, 5]) + "\n" + "Number of trades : " + str(data[0, 8])
        else:
            percent = (float(data[0, 4]) - float(data[0, 1])) * 100 / float(data[0, 1])
            percent = round(percent, 3)
            text = "😰" + request + "\n🔴" + str(percent) + "%\n" + "⏱Timeframe: "+timeframe +"Open time : " + str(
                time) + "\n" + "Open : " + str(data[0, 1]) + \
                   "\n" + "High : " + str(data[0, 2]) + "\n" + "Low : " + str(data[0, 3]) + "\n" + "Close : " + str(
                data[0, 4]) + \
                   "\n" + "Volume : " + str(data[0, 5]) + "\n" + "Number of trades : " + str(data[0, 8])
        bot.send_message(message.chat.id, text)
    except:
        bot.send_message(message.chat.id, "Invalid symbol or something wrong \n"
                                          "Please try again ")


@bot.message_handler(commands=['add'])
def add_symbol(message):
    try:
        symbol.append(message.text.split()[1])
        bot.send_message(message.chat.id, message.text.split()[1] + " Added to the watchlist")
    except:
        bot.reply_to(message, "No coin entered")


@bot.message_handler(commands=['coins'])
def show_coins(message):
    coins = ""
    for coin in symbol:
        coins += str(coin) + "  "
    bot.send_message(message.chat.id, "Watchlist : " + coins)


@bot.message_handler(commands=['remove'])
def remove_coins(message):
    try:
        coin = message.text.split()[1]
        try:
            symbol.remove(coin)
            bot.reply_to(message, "Coin has been removed")
        except:
            bot.reply_to(message, message.text.split()[1] + " Not in list")
    except:
        bot.reply_to(message, "No coin entered")


bot.polling()