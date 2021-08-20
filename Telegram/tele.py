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
from time import sleep
from Auth import login , register , reset_password
from Inc import db , functions
import numpy as np
from binance.client import Client
from Telegram import candle
from Account.clients import User , Register
from decouple import config
#    test
#statics
API_KEY = config('API_KEY')
# API_KEY = '1936293973:AAFLKY0TCP9qEMjqPDrewsdzGisNSQmB0ds'
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

#need more develop on classes

def bot_actions():
    # /start command enter by user
    @bot.message_handler(commands=['start'])
    def welcome(message):
        #some action with delay to typing bot
        bot.send_chat_action(chat_id=message.chat.id, action="typing")
        sleep(1)
        #welcome message and instructions
        bot.reply_to(message, "Hey " + message.chat.first_name + "!\n" +
                     "I am Aran , your trade assistance \n"
                     "/help show commands")
        #the markup help us we have call back with inlinekeyboard when yours tap one of those
        #some callback data send and we receive with @bot.callback_query_handler
        step_kb = telebot.types.InlineKeyboardMarkup()
        step_kb.add(telebot.types.InlineKeyboardButton('🔑Login', callback_data='login'))
        step_kb.add(telebot.types.InlineKeyboardButton('🤩Sign up', callback_data='reg'))
        step_kb.add(telebot.types.InlineKeyboardButton('🔏Forget password', callback_data='forget'))
        bot.send_message(chat_id=message.chat.id,text='Have not any account?\nSign up now!',reply_markup=step_kb)
    #after callback @bot.callback_query_handler get function parameter ,this always true
    #and w8 to one case login and reg and .. happened . need to develop func in parameter
    @bot.callback_query_handler(func=lambda call: True)
    def query_handler(call):
        if call.data == "login":
            #create object from user and store in our dictionary with chat_id key value
            user = User()
            user_dict[call.message.chat.id] = user
            bot.reply_to(call.message , "🔑Enter your username")
            #handle next step message user enter after login
            bot.register_next_step_handler(call.message, callback=process_login_username)
        if call.data == "reg":
            if functions.check_chat_id(connection ,call.message.chat.id ):
                #create object from user and store in our dictionary with chat_id key value
                user = Register(call.message.chat.id)
                reg_dict[call.message.chat.id] = user
                bot.reply_to(call.message , "🔑Enter your username")
                #handle next step message user enter after sign up
                bot.register_next_step_handler(call.message, callback=process_reg_username)
            else:
                username = functions.get_user_with_chat_id(connection ,call.message.chat.id)
                bot.reply_to(call.message, f"You already have an account : {username} \nPlease /start to login ")
        if call.data == "1" or call.data == "2":
            #in other keyboard we need calls back from user choose which one question
            user = reg_dict[call.message.chat.id]
            #store in our object
            user.security_question_id = int(call.data)
            bot.reply_to(call.message, "Enter your answer")
            # handle next step message user enter after choose question
            bot.register_next_step_handler(call.message, callback=process_reg_answer)
        if call.data == "forget":
            #create object from user and store in our dictionary with chat_id key value
            user = Register(call.message.chat.id)
            reg_dict[call.message.chat.id] = user
            bot.reply_to(call.message, "🔑Enter your username")
            #handle next step message user enter after forget password
            bot.register_next_step_handler(call.message, callback=process_forget_username)
        if call.data == "watchlist":
            coin_keyboard = telebot.types.InlineKeyboardMarkup()
            for index , coin in coins_list:
                coin_keyboard.add(telebot.types.InlineKeyboardButton(coin, callback_data=coin))
            bot.send_message(chat_id=call.message.chat.id, text='Select your coin', reply_markup=coin_keyboard)

        #need more develop
        if call.data in coins_list[:,1] :
            coin = coins_list[np.where(coins_list[:, 1] == call.data)][0][0]
            # for coins in coins[:1]:
            user = user_dict[call.message.chat.id]
            if not functions.set_coin(connection, user.username, coin, user.watchlist[0][2])[0]:
                bot.reply_to(call.message, "Coin already in watchlist /add")
            else:
                bot.reply_to(call.message, "Done! /show to show your watchlist \n"
                                           "Default time frame is 30min!\n"
                                           "For change /frame")

        if call.data in timeframes_list[:,1] :
            time_id = timeframes_list[np.where(timeframes_list[:, 1] == call.data)][0][0]
            time= timeframes_list[np.where(timeframes_list[:, 1] == call.data)][0][1]
            # for coins in coins[:1]:
            user = user_dict[call.message.chat.id]
            functions.update_timeframe(connection , user.username , time_id)
            bot.reply_to(call.message, f"Done! timeframe change to {time}")

        if call.data in analysis_list[:,1]:
            user = user_dict[call.message.chat.id]
            analysis_id = analysis_list[np.where(analysis_list[:, 1] == call.data)][0][0]
            functions.set_user_analysis(connection, user.username , int(analysis_id))
            bot.reply_to(call.message, f"Done!\n"
                                       f"Now {call.data} is working for you")
        if call.data == "remove_watchlist":
            user = user_dict[call.message.chat.id]
            user.watchlist = functions.get_user_watchlist(connection, user.username)
            if user.watchlist:
                watchlist_remove = telebot.types.InlineKeyboardMarkup()
                # for watch in user.watchlist :
                user.temp_watch = user.watchlist[0][2]
                watchlist_remove.add(telebot.types.InlineKeyboardButton(user.watchlist[0][2], callback_data='watchlist_remove_step2'))
                bot.send_message(chat_id=call.message.chat.id, text='Select your watchlist', reply_markup=watchlist_remove)
            else:
                bot.reply_to(call.message, 'You don\'t have any watchlist! /new' )
        if call.data == "watchlist_remove_step2":
            user = user_dict[call.message.chat.id]
            functions.delete_watchlist(connection , user.username , user.temp_watch)
            bot.reply_to(call.message, 'Done!\nFor create /new')

        if call.data == "remove_coins":
            user = user_dict[call.message.chat.id]
            user.watchlist = functions.get_user_watchlist(connection, user.username)
            if user.watchlist:
                if functions.get_empty_coins_remain(connection, user.username, user.watchlist[0][2]) == 2 :
                    bot.reply_to(call.message, 'No coins in your watchlist!/add😓')
                else:
                    watchlist_remove = telebot.types.InlineKeyboardMarkup()
                    # for watch in user.watchlist :
                    user.temp_watch = user.watchlist[0][2]
                    watchlist_remove.add(telebot.types.InlineKeyboardButton(user.watchlist[0][2],
                                                                            callback_data='coins_remove_step2'))
                    bot.send_message(chat_id=call.message.chat.id, text='Select your watchlist',
                                     reply_markup=watchlist_remove)
            else:
                bot.reply_to(call.message, 'Create watchlist first! /new')
        if call.data == "coins_remove_step2":
            user = user_dict[call.message.chat.id]
            user.watchlist = functions.get_user_watchlist(connection, user.username)
            coin_keyboard = telebot.types.InlineKeyboardMarkup()
            user_coins = functions.get_user_coins(connection, user.username, user.watchlist[0][2])
            for coin in user_coins:
                coin_keyboard.add(telebot.types.InlineKeyboardButton(coin, callback_data=coin + " delete"))
            bot.send_message(chat_id=call.message.chat.id, text='Select your coin', reply_markup=coin_keyboard)

        if "delete" in call.data :
            user = user_dict[call.message.chat.id]
            temp = str(call.data).split(" ")
            coin = coins_list[np.where(coins_list[:, 1] == temp[0])][0][0]
            functions.set_null_coin_user(connection , user.username , coin)
            bot.reply_to(call.message, 'Done!\n /add coins now!')

        #after call back done keyboard delete
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


    """
        login handler
    """
    #get username and store in user dictionary (key:chat_id)
    def process_login_username(message):
        try:
            user = user_dict[message.chat.id]
            user.username = message.text
            #get password with process_password and register_next_step_handler
            # to handle next enter user's message
            msg = bot.reply_to(message, '🔒Enter your password')
            bot.register_next_step_handler(msg, process_password)
        #some exception need develop
        except Exception as e:
            bot.reply_to(message, 'Please /start bot again')
            del user_dict[message.chat.id]

    #if session assign True user login ,if any exception happened -
    # start again with /start and object user removed
    def process_password(message):
        try:
            user = user_dict[message.chat.id]
            res = login.login(db_connection=connection , username=user.username , password=message.text)
            bot.delete_message(message.chat.id , message.message_id)
            bot.send_message(message.chat.id , res)
            user.session = True
            print(user_dict)
        except Exception as e:
            bot.reply_to(message, 'Please /start bot again')
            del user_dict[message.chat.id]

    """
        register handler
    """
    def process_reg_username(message):
        try:
            #fetch object
            user = reg_dict[message.chat.id]
            user.username = message.text
            msg = bot.reply_to(message, '👮🏻‍♂️Enter your password\n'
                                        '\n🔹your password must be at least 8 characters\n'
                                        '🔹And a number and special character(@#$%^&+=)\n'
                                        '🔹and lower/upper case at least')
            bot.register_next_step_handler(msg, process_reg_password)
        except Exception as e:
            bot.reply_to(message, 'Please /start bot again')
            del reg_dict[message.chat.id]

    def process_reg_password(message):
        try:
            user = reg_dict[message.chat.id]
            user.password1 = message.text
            msg = bot.reply_to(message, '🔒Enter your password again')
            bot.register_next_step_handler(msg, process_reg_password_again)
            #delete password for privacy
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            bot.reply_to(message, 'Please /start bot again')
            del reg_dict[message.chat.id]

    def process_reg_password_again(message):
        try:
            user = reg_dict[message.chat.id]
            user.password2 = message.text
            question_dict = functions.get_security_questions(connection)
            bot.delete_message(message.chat.id, message.message_id)
            #select question
            questions = telebot.types.InlineKeyboardMarkup()
            questions.add(telebot.types.InlineKeyboardButton(question_dict[0][1], callback_data="1"))
            questions.add(telebot.types.InlineKeyboardButton(question_dict[1][1], callback_data="2"))
            bot.send_message(chat_id=message.chat.id, text='⚠️Select your security question', reply_markup=questions)
        except Exception as e:
            bot.reply_to(message, 'Please /start bot again ')
            del reg_dict[message.chat.id]

    def process_reg_answer(message):
        try:
            user = reg_dict[message.chat.id]
            user.answer = message.text
            #insert to database
            res = register.register(db_connection=connection ,username=user.username ,chat_id=user.chat_id,
                                    password=user.password1 , password2=user.password1 ,question_id=user.security_question_id , answer=user.answer)
            #initial default timeframe 1min
            functions.set_timeframe(connection,user.username , 1)
            #init first amount bank
            functions.set_amount_bank_user(connection , user.username , 10)
            bot.reply_to(message, res+"\nplease /start to login")
            del reg_dict[message.chat.id]
        except Exception as e:
            bot.reply_to(message, 'Please /start bot again')
            del reg_dict[message.chat.id]

    """
        forget message  handler
    """
    def process_forget_username(message):
        try:
            user = reg_dict[message.chat.id]
            user.username = message.text
            #check user exists if dont handle this next step crashed ->get_user_security_id handled this
            q_id = functions.get_user_security_id(connection, user.username)
            question = functions.get_security_questions(connection , q_id)
            if q_id :
                user.security_question_id = q_id
                user.security_question = functions.get_security_questions(connection , q_id)
                msg = bot.reply_to(message, question[0][1])
                bot.register_next_step_handler(msg, process_forget_answer)
            else:
                bot.send_message(chat_id=message.chat.id , text="😞Username not exists\nTry again /start")
                del reg_dict[message.chat.id]

        except Exception as e:
            bot.reply_to(message, 'Please /start bot again')
            del reg_dict[message.chat.id]

    def process_forget_answer(message):
        try:
            user = reg_dict[message.chat.id]
            user.answer = message.text
            msg = bot.reply_to(message, '🔓Enter your new password')
            bot.register_next_step_handler(msg, process_forget_new_pass)
        except Exception as e:
            bot.reply_to(message, 'Please /start bot again')
            del reg_dict[message.chat.id]

    def process_forget_new_pass(message):
        try:
            user = reg_dict[message.chat.id]
            user.password1 = message.text
            msg = bot.reply_to(message, '🔒Enter your new password again')
            bot.delete_message(message.chat.id, message.message_id)
            bot.register_next_step_handler(msg, process_forget_new_pass_again)
        except Exception as e:
            bot.reply_to(message, 'Please /start bot again')
            del reg_dict[message.chat.id]

    def process_forget_new_pass_again(message):
        try:
            user = reg_dict[message.chat.id]
            user.password2 = message.text
            #reset_password function handle all error about passwords and wrong answer
            res = reset_password.reset_password(db_connection=connection ,username=user.username , answer=user.answer ,
                                                new_password=user.password1 ,new_password2=user.password2)
            bot.reply_to(message, res)
            bot.delete_message(message.chat.id, message.message_id)
            #after reset password and update database we dont need this object
            del reg_dict[message.chat.id]
        except Exception as e:
            bot.reply_to(message, 'Please /start bot again')
            del reg_dict[message.chat.id]

    """
        new command handler / for new watchlist
    """
    @bot.message_handler(commands=['new'])
    def new_watchlist(message):
        if not message.chat.id in user_dict :
            bot.reply_to(message, 'Please login /start')
        elif not user_dict[message.chat.id].session:
            bot.reply_to(message, 'Please login /start')
        else:
            user = user_dict[message.chat.id]
            # if len(functions.get_user_watchlist(connection , user.username)) < 1:
            if not functions.get_user_watchlist(connection , user.username):
                bot.reply_to(message, "Enter your watchlist name")
                bot.register_next_step_handler(message, process_new_watch)
            else:
                bot.reply_to(message, "😅 You have already one watchlist /show")

    def process_new_watch(message):
        try:
            #fetch object
            user = user_dict[message.chat.id]
            for create in range(0,2):
                functions.create_watchlist(connection , user.username , message.text)
            user.watchlist = message.text
            bot.reply_to(message, "Good!👀\n/add to add coin in your watchlist")
        except Exception as e:
            bot.reply_to(message, 'Please /start bot again')

    @bot.message_handler(commands=['add'])
    def add_coin(message):
        if not message.chat.id in user_dict :
            bot.reply_to(message, 'Please login /start')
        elif not user_dict[message.chat.id].session:
            bot.reply_to(message, 'Please login /start')
        else:
            user = user_dict[message.chat.id]
            user.watchlist = functions.get_user_watchlist(connection, user.username)
            if user.watchlist:
                if functions.get_empty_coins_remain(connection ,user.username , user.watchlist[0][2])!=0:
                    watchlist = telebot.types.InlineKeyboardMarkup()
                    watchlist.add(telebot.types.InlineKeyboardButton(user.watchlist[0][2], callback_data='watchlist'))
                    bot.send_message(chat_id=message.chat.id, text='Select your watchlist', reply_markup=watchlist)
                else:
                    bot.reply_to(message, 'your watchlist is full!😓')
            else:
                bot.reply_to(message, 'Create watchlist first! /new')

    """
        timeframe command handler update 
    """
    @bot.message_handler(commands=['frame'])
    def update_timeframe(message):
        if not message.chat.id in user_dict:
            bot.reply_to(message, '😪Please /start to login')
        #check user login
        elif user_dict[message.chat.id] and not user_dict[message.chat.id].session :
            bot.reply_to(message, '😪You are logged out')
        else:
            time_keyboard = telebot.types.InlineKeyboardMarkup()
            for index, time in timeframes_list:
                time_keyboard.add(telebot.types.InlineKeyboardButton(time, callback_data=time))
            bot.send_message(chat_id=message.chat.id, text='Select your timeframe', reply_markup=time_keyboard)


    """
        show command handler
    """
    @bot.message_handler(commands=['show'])
    def update_timeframe(message):
        if not message.chat.id in user_dict:
            bot.reply_to(message, '😪Please /start to login')
        #check user login
        elif user_dict[message.chat.id] and not user_dict[message.chat.id].session :
            bot.reply_to(message, '😪You are logged out')
        else:
            user = user_dict[message.chat.id]
            user.watchlist = functions.get_user_watchlist(connection, user.username)
            if user.watchlist:
                amount = functions.get_amount_bank_user(connection, user.username)
                timeframe = functions.get_user_timeframe(connection, user.username)
                coins = ""
                for watchlist in user.watchlist:
                    if watchlist[1]:
                        coin = str(functions.get_coin_name(connection , int(watchlist[1])))
                        percent = candle.get_percent_candle(coin, timeframe)
                        percent = str(percent) + " 🔴" if percent<0 else str(percent)+ " 🟢"
                        coins += coin + " %"+ percent +"\n"
                # amount = 0
                res ="💰 Assets\n" + str(amount) + "$\n\n" \
                                                   "👀 Watchlists\n"+ user.watchlist[0][2] + "\n\n💎 Coins\n" + coins + "\n⏱ Timeframe\n" \
                     + timeframe
                bot.reply_to(message, res)
            else:
                bot.reply_to(message, 'Create watchlist first! /new')
    @bot.message_handler(commands=['analysis'])
    def update_timeframe(message):
        if not message.chat.id in user_dict:
            bot.reply_to(message, '😪Please /start to login')
        #check user login
        elif user_dict[message.chat.id] and not user_dict[message.chat.id].session :
            bot.reply_to(message, '😪You are logged out')
        else:
            #if user dont have an analysis
            user = user_dict[message.chat.id]
            analysis = functions.get_user_analysis(connection ,user.username)
            if not analysis:
                analysis_keyboard = telebot.types.InlineKeyboardMarkup()
                for index , analy in analysis_list:
                    analysis_keyboard.add(telebot.types.InlineKeyboardButton(analy, callback_data=analy))
                bot.send_message(chat_id=message.chat.id, text='📊️Select your analysis', reply_markup=analysis_keyboard)
            else:
                bot.reply_to(message, f'😏You already have {analysis} analysis \n'
                                      f'/show to remove or see details')

    """
            removes command handler
    """

    @bot.message_handler(commands=['remove'])
    def remove(message):
        if not message.chat.id in user_dict:
            bot.reply_to(message, '😪Please /start to login')
        #check user login
        elif not user_dict[message.chat.id].session :
            bot.reply_to(message, '😪Please /start to login')
        else:
            try:
                remove_keyboard = telebot.types.InlineKeyboardMarkup()
                remove_keyboard.add(telebot.types.InlineKeyboardButton("Watchlist", callback_data="remove_watchlist"))
                remove_keyboard.add(telebot.types.InlineKeyboardButton("Coins", callback_data="remove_coins"))
                bot.send_message(chat_id=message.chat.id, text='select option you want to delete',
                                 reply_markup=remove_keyboard)

            except Exception as e:
                bot.reply_to(message, 'logout unsuccessful')
    """
        logout command handler
    """
    @bot.message_handler(commands=['logout'])
    def logout(message):
        if not message.chat.id in user_dict:
            bot.reply_to(message, '😪Please /start to login')
        #check user login
        elif user_dict[message.chat.id] and not user_dict[message.chat.id].session :
            bot.reply_to(message, '😪You are logged out')
        else:
            try:
                user_dict[message.chat.id].session = False
                bot.reply_to(message, '👋🏼Goodbye!\nFor login /start bot ')
                del user_dict[message.chat.id]
                print(user_dict)
            except Exception as e:
                bot.reply_to(message, 'logout unsuccessful')




