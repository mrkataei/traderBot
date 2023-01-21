from Telegram.base import Telegram
from telebot import types
from crud.user import user as crud
from db.session import SessionLocal
from schema.user import UserCreate
from Libraries.definitions import *
from .keybords import start_keyboard, exchange_keyboard
from util.module import get_exchanges, get_exchange
from time import sleep

session = SessionLocal()

class TempBot(Telegram):
    def __init__(self):
        Telegram.__init__(self)
    
    def bot_actions(self):
        
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

        @self.bot.message_handler(func=self.is_valid_user)
        def add_watchlist(message):
            try:
                self.bot.send_message(message.chat.id, trans("C_choose_exchange"),
                                      reply_markup=exchange_keyboard())
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_1)

            except Exception as e:
                self.bot.reply_to(message, trans("C_error"), reply_markup=start_keyboard())

        def add_exchange_step_1(message):
            try:
                exchanges = get_exchanges()
                exchanges_id = np.where(exchanges[:, 1] == message.text)[0][0]
                key_markup = types.ReplyKeyboardRemove(selective=False)
                exchanges_id = int(exchanges[exchanges_id][0])
                if exchanges_id == 3:
                    self.bot.send_message(message.chat.id, trans("C_enter_token"), reply_markup=key_markup)
                else:
                    self.bot.send_message(message.chat.id, trans("C_enter_public_key"), reply_markup=key_markup)
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_2,
                                                        exchange_id=exchanges_id,
                                                        user_setting_id=user_setting_id)
            except IndexError:
                self.bot.send_message(message.chat.id, trans("C_wrong_exchange"), reply_markup=exchanges_keyboard())
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_1,
                                                        user_setting_id=user_setting_id)

        def add_exchange_step_2(message, exchange_id: int, user_setting_id: int):
            if message.content_type == 'text':
                if exchange_id == 3:
                    add_exchange_step_3(message=message, exchange_id=3, public=message.text,
                                        user_setting_id=user_setting_id)

                else:
                    self.bot.send_message(message.chat.id, trans("C_enter_secret_key"))
                    self.bot.register_next_step_handler(message=message, callback=add_exchange_step_3,
                                                        exchange_id=exchange_id, public=message.text,
                                                        user_setting_id=user_setting_id)
                    self.bot.delete_message(message.chat.id, message.message_id)
            else:
                self.bot.send_message(message.chat.id, trans("C_wrong_API"))
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_2,
                                                    exchange_id=exchange_id,
                                                    user_setting_id=user_setting_id)

        def add_exchange_step_3(message, exchange_id: int, public: str, user_setting_id: int):
            if message.content_type == 'text':
                exchange_client = get_exchange_class(exchange_id=int(exchange_id), public=public, secret=message.text,
                                                     chat_id=message.chat.id)
                markup = start_keyboard()
                if exchange_client is not None:
                    assets = exchange_client.get_assets()
                    if assets[0]:
                        self.bot.send_message(message.chat.id, trans("C_wrong_API"), reply_markup=markup)
                    else:
                        assets = assets[1]
                        result_message = f'{trans("C_assets")}:\n'
                        for asset in assets:
                            result_message += f'🪙 {asset[1]}\n 💎 {str(asset[2])}\n\n'
                        self.bot.send_message(message.chat.id, result_message)
                        user = self.user_dict[message.chat.id]
                        # insert database
                        if user_setting_id == 0:
                            error, result = functions.set_user_setting(username=str(user.username),
                                                                       exchange_id=int(exchange_id),
                                                                       public=str(public), secret=str(message.text))
                            self.bot.delete_message(message.chat.id, message.message_id)
                            if error:
                                self.bot.send_message(message.chat.id, trans("C_something_wrong"), reply_markup=markup)
                            else:
                                self.bot.send_message(message.chat.id, trans("C_success"), reply_markup=markup)
                        else:
                            result = functions.update_user_exchange(user_setting_id=int(user_setting_id),
                                                                    exchange_id=int(exchange_id),
                                                                    public=str(public), secret=str(message.text))
                            self.bot.delete_message(message.chat.id, message.message_id)
                            if result is None:
                                self.bot.send_message(message.chat.id, trans("C_success"), reply_markup=markup)
                            else:
                                self.bot.send_message(message.chat.id, trans("C_same_exchange"),
                                                      reply_markup=markup)
                else:
                    self.bot.send_message(message.chat.id, trans("C_unsupported_exchange"),
                                          reply_markup=start_keyboard())
            else:
                self.bot.send_message(message.chat.id, trans("C_wrong_API"))
                self.bot.register_next_step_handler(message=message, callback=add_exchange_step_3,
                                                    exchange_id=exchange_id, public=public,
                                                    user_setting_id=user_setting_id)
