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
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_chat_action(chat_id=message.chat.id ,  action="typing")
    users.append(message.chat.username)
    sleep(1)
    bot.reply_to(message, "Hey " + message.chat.first_name + "!\n"+
                 "I am Aran , your trade assistance \n"
                 "/help show commands" )
    #send notif to admin
    print(users)
    if message.chat.username:
        bot.send_message(chat_id=1210507821 , text="Hi Admin!\n" + "@"+message.chat.username + " just join now" )
    else:
        bot.send_message(chat_id=1210507821 , text="Hi Admin!\n" +message.chat.first_name + " just join now" )

@bot.message_handler(commands=['help'])
def help_me(message):
    bot.send_chat_action(chat_id=message.chat.id ,  action="typing")
    sleep(1)
    bot.reply_to(message, "price <symbol> show last price of symbol\n"
                          "candle <symbol> show last 1min candle of symbol" )
# @bot.message_handler(commands=['test'])
# def start_message(message):
#     markup = telebot.types.InlineKeyboardMarkup()
#     markup.add(telebot.types.InlineKeyboardButton(text='Three', callback_data=3))
#     markup.add(telebot.types.InlineKeyboardButton(text='Four', callback_data=4))
#     markup.add(telebot.types.InlineKeyboardButton(text='Five', callback_data=5))
#     bot.send_message(message.chat.id, text="How much is 2 plus 2?", reply_markup=markup)
#
# @bot.callback_query_handler(func=lambda call: True)
# def query_handler(call):
#
#     bot.answer_callback_query(callback_query_id=call.id, text='Answer accepted!')
#     answer = 'You made a mistake'
#     if call.data == '4':
#         answer = 'You answered correctly!'
#
#     bot.send_message(call.message.chat.id, answer)
#     bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
def stock_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in "price" :
        return False
    else:
        return True

@bot.message_handler(func=stock_request)
def send_price(message):
    request = str(message.text.split()[1]).upper()
    try:
        data  = client.get_symbol_ticker(symbol=request)["price"]
        if data:
            bot.send_message(message.chat.id, data)
        else:
            bot.send_message(message.chat.id, "No data!?")
    except:
        bot.send_message(message.chat.id, "invalid symbol please try again ")


def candle_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in "candle" :
        return False
    else:
        return True

@bot.message_handler(func=candle_request)
def send_candle(message):
    request = str(message.text.split()[1]).upper()

    try:
        data = pd.DataFrame(client.get_klines(symbol=request , interval=client.KLINE_INTERVAL_1MINUTE , limit= 1 )).values
        time = pd.to_datetime(data[0,0] ,unit='ms' ,yearfirst=True).tz_localize('UTC').tz_convert('Asia/Tehran')
        if data[0,1] <= data[0,4]:
            percent  = (float(data[0,4]) - float(data[0,1]) ) * 100 / float(data[0,1])
            percent  = round(percent, 3)
            text = "🤑" +request + "    1min"+"\n🟢" +  str(percent) +"%\n"+"Open time : " + str(time) + "\n" + "Open : " + str(data[0,1]) + \
                   "\n" + "High : " + str(data[0,2]) + "\n"+ "Low : " + str(data[0,3]) + "\n" + "Close : " + str(data[0,4]) + \
                   "\n" + "Volume : " + str(data[0,5]) + "\n" + "Number of trades : " + str(data[0,8])
        else:
            percent  = (float(data[0,4]) - float(data[0,1]) ) * 100 / float(data[0,1])
            percent  = round(percent, 3)
            text = "😰" +request + "    1min"+"\n🔴" +  str(percent) +"%\n" "Open time : " + str(time) + "\n" + "Open : " + str(data[0,1]) + \
                   "\n" + "High : " + str(data[0,2]) + "\n"+ "Low : " + str(data[0,3]) + "\n" + "Close : " + str(data[0,4]) + \
                   "\n" + "Volume : " + str(data[0,5]) + "\n" + "Number of trades : " + str(data[0,8])
        bot.send_message(message.chat.id, text)
    except:
        bot.send_message(message.chat.id, "invalid symbol or something wrong \n"
                                          "please try again ")


@bot.message_handler(commands=['add'])
def add_symbol(message):
    try:
        symbol.append(message.text.split()[1])
        bot.send_message(message.chat.id, message.text.split()[1] + " added to the coin list")
    except:
        bot.reply_to(message , "no coin entered")

@bot.message_handler(commands=['coins'])
def show_coins(message):
    coins = ""
    for coin in symbol:
        coins += str(coin) + "  "
    bot.send_message(message.chat.id, "coins already watchlist : " + coins)

@bot.message_handler(commands=['remove'])
def remove_coins(message):
    try:
        coin = message.text.split()[1]
        try:
            symbol.remove(coin)
            bot.reply_to(message, "coin has been removed")
        except:
            bot.reply_to(message, message.text.split()[1] +  " not in list")
    except:
        bot.reply_to(message, "no coin entered")



bot.polling()