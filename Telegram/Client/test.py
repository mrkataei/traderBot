from crud.user import CRUDUser
from db.session import SessionLocal
from schema.user import UserCreate
session = SessionLocal()
c_user = UserCreate(username='dasfs', password='sdsd', chat_id='sdfdsf')

user = CRUDUser.create(db=session, obj_in=c_user)

from Interfaces.telegram import Telegram

class TempBot(Telegram):
    def __init__(self):
        Telegram.__init__(self)

    def bot_actions(self):
        @self.bot.message_handler(func=lambda message: True)
        def start(message):
            self.bot.send_message(message.chat.id, ' 👷🏼‍♂️ ربات در حال تعمیر و بروزرسانی است.\n'
                                                   'از صبر و شکیبایی شما متشکریم! ')
