from Telegram.base import Telegram
from telebot import types
from crud.user import user as crud
from db.session import SessionLocal
from schema.user import UserCreate
from Libraries.definitions import *
from .keybords import start_keyboard, social_keyboard
from util.module import get_exchanges, get_exchange
from time import sleep

session = SessionLocal()

class TempBot(Telegram):
    def __init__(self):
        Telegram.__init__(self)
    
    def bot_actions(self):
        super().bot_actions()
        @self.bot.message_handler(commands=['start'])
        def welcome(message):
            user = crud.get_by_chat_id(db=session, chat_id=message.chat.id)
            user_lang = message.from_user.language_code
            activate(user_lang)
            if not user:
                # is typing bot ..
                self.bot.send_chat_action(chat_id=message.chat.id, action="typing")
                sleep(1)

                self.bot.send_message(message.chat.id, trans('C_hey') + message.chat.first_name + "!\n" +
                                      trans('C_welcome'), reply_markup=start_keyboard())
                keyboard = types.ReplyKeyboardMarkup()
                reg_button = types.KeyboardButton(text=trans("C_share_contact"), request_contact=True)
                keyboard.add(reg_button)
                self.bot.send_message(message.chat.id, trans("C_reg_with_phone"),
                                      reply_markup=keyboard)
            else:
                self.bot.send_message(message.chat.id, trans("C_can_i_help"), reply_markup=start_keyboard())
            
        @self.bot.message_handler(content_types=['contact'])
        def register_handler(message):
            markup = types.ReplyKeyboardRemove(selective=False)
            self.bot.send_message(message.chat.id, trans("C_enter_username"), reply_markup=markup)
            self.bot.register_next_step_handler(message=message, callback=reg_step_1,
                                                phone=message.contact.phone_number)
        def reg_step_1(message, phone: str):
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

        


        
