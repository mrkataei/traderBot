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

#statics
# API_KEY = os.getenv('API_KEY')
API_KEY = '1936293973:AAFLKY0TCP9qEMjqPDrewsdzGisNSQmB0ds'
bot = telebot.TeleBot(API_KEY)
connection = db.con_db()
user_dict = {}
reg_dict = {}

#need more develop on classes
class User:
    def __init__(self, name):
        self.username = name
        self.session = None

class Register:
    def __init__(self ,chat_id):
        self.chat_id = chat_id
        self.username:str
        self.password1:str
        self.password2:str
        self.security_question_id:int
        self.security_question:str
        self.security_answer:str

#/start command enter by user
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
        user = User(call.message.chat.first_name)
        user_dict[call.message.chat.id] = user
        bot.reply_to(call.message , "🔑Enter your username")
        #handle next step message user enter after login
        bot.register_next_step_handler(call.message, callback=process_login_username)
    if call.data == "reg":
        #create object from user and store in our dictionary with chat_id key value
        user = Register(call.message.chat.id)
        reg_dict[call.message.chat.id] = user
        bot.reply_to(call.message , "🔑Enter your username")
        #handle next step message user enter after sign up
        bot.register_next_step_handler(call.message, callback=process_reg_username)
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
        if q_id :
            user.security_question_id = q_id
            user.security_question = functions.get_security_questions(connection , q_id)
            msg = bot.reply_to(message, 'Enter your Answer')
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
        #after reset password and update database we dont need this object
        del reg_dict[message.chat.id]
    except Exception as e:
        bot.reply_to(message, 'Please /start bot again')
        del reg_dict[message.chat.id]


@bot.message_handler(commands=['new'])
def new_watchlist(message):
    if not message.chat.id in user_dict :
        bot.reply_to(message, 'Please /start bot again')
    elif not user_dict[message.chat.id].session:
        bot.reply_to(message, 'Please login /start')
    else:
        bot.register_next_step_handler(message, callback=process_new_watch_name)


# def process_new_watch_name(message):



"""
    logout command handler
"""
@bot.message_handler(commands=['logout'])
def logout(message):
    if not message.chat.id in user_dict:
        bot.reply_to(message, 'Please /start bot again')
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

#needs always run
bot.polling()