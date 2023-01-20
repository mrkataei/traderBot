from Interfaces.telegram import Telegram
from telebot import types
from crud.user import user as crud
from db.session import SessionLocal
from schema.user import UserCreate
from Libraries.definitions import *

from time import sleep





session = SessionLocal()




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
# master bot already run on vps dont use this @aitrdbot -> address
# API_KEY = '2123917023:AAFPy9xoaJLt0BxqQJgC3J3F9km8F7ozdn8'
# @testkourosh2bot -> address // use this bot for test your code
# API_KEY = '1978536410:AAE_RMk3-4r_cLnt_nRcEnZHaSp-vIk9oVo'


class TempBot(Telegram):
    def __init__(self):
        Telegram.__init__(self)

    def bot_actions(self):
        @self.bot.message_handler(commands=['start'])
        def welcome(message):
            user = crud.get_by_chat_id(db=session, chat_id=message.chat.id)
            # activate_language('', message)
            # markup = start_keyboard()
            # self.user_dict[message.chat.id] = User(message=message)  # create object for register user session
            if not user:
                # is typing bot ..
                self.bot.send_chat_action(chat_id=message.chat.id, action="typing")
                sleep(1)

                self.bot.send_message(message.chat.id, "please register", reply_markup=start_keyboard())
                # if user deleted telegram account need develop
                keyboard = types.ReplyKeyboardMarkup()
                reg_button = types.KeyboardButton(text=trans("C_share_contact"), request_contact=True)
                keyboard.add(reg_button)
                self.bot.send_message(message.chat.id, trans("C_reg_with_phone"),
                                      reply_markup=keyboard)
            
        @self.bot.message_handler(content_types=['contact'])
        def register_handler(message):
            markup = types.ReplyKeyboardRemove(selective=False)
            self.bot.send_message(message.chat.id, trans("C_enter_username"), reply_markup=markup)
            self.bot.register_next_step_handler(message=message, callback=reg_step_1,
                                                phone=message.contact.phone_number)

        def reg_step_1(message, phone: str):
            # user = self.user_dict[message.chat.id]
            username = str(message.text).lower()
            try:
                if crud.get_by_username(db=session, username=username):
                    self.bot.send_message(message.chat.id, trans('C_exist_username'))
                    self.bot.register_next_step_handler(message=message, callback=reg_step_1,
                                                        phone=phone)
                elif message.content_type == 'text':
                    c_user = UserCreate(username=username, password=phone, chat_id=message.chat.id ,email='dsfdfs@dfdf.com', phone=phone)
                    crud.create(db=session, obj_in=c_user)
                    # functions.update_user_online(username=user.username, online=True)
                    markup = start_keyboard()
                    self.bot.send_message(message.chat.id, trans('C_account_created'), reply_markup=markup)
                else:
                    self.bot.send_message(message.chat.id, trans('C_invalid_username'))
                    self.bot.register_next_step_handler(message=message, callback=reg_step_1,
                                                        phone=phone)

            except Exception as e:
                self.bot.reply_to(message, e)
