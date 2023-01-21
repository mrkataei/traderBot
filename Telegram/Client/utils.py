from Telegram.base import Telegram
from telebot import types
from crud.user import user as crud
from db.session import SessionLocal
from schema.user import UserCreate
from Libraries.definitions import *
from .keybords import start_keyboard
from time import sleep


session = SessionLocal()

def is_valid_user(self, message) -> bool:
    user = crud.get_by_chat_id(chat_id=message.chat.id)
    # user = functions.get_user(message.chat.id)
    if not user:
        self.bot.send_message(message.chat.id, trans('C_sorry_signup'))
        return False
    else:
        result = crud.check_expire(db=session, chat_id=message.chat.id)
        if result:
            self.bot.send_message(message.chat.id, trans('C_expire_plan'))
            return False
        else:
            return result
