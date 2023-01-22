"""
    Mr.Kataei 11/12/2021
"""
import telebot
from telebot import types
from time import sleep
from crud.user import user as crudUser
from crud.watchlist import watchlist as crudWatchlist
from crud.sterategy import strategy as crudStrategy
from db.session import SessionLocal
from libraries.definitions import *
from .keybords import start_keyboard, social_keyboard
from schema.watchlist import WatchlistUpdate
from util.module import get_exchange

session = SessionLocal()

def dont_understand(message) -> bool:
    commands = ['/lang', '/exchange', '/strategy', '/test', '/start', '/plans', '/profile', '/tutorial',
                '/help', trans('C_social_medias'),
                trans('C_plans'), trans('C_back_test'), trans('C_profile'), trans('C_tutorials'),
                trans('C_add_exchange'), trans('C_add_strategy'), trans('C_lang'), trans('C_help')]

    if message.text not in commands or message.content_type != 'text':
        return True
    else:
        return False


def update_watchlist():
    pass

class Telegram:
    def __init__(self, API_KEY: str = '5987702945:AAHjEwnwW8NaHAxv2C-lEUIJXFacNnkQIUk'):
        self.API_KEY = API_KEY
        self.bot = None
        self.user_dict = {}

    def bot_polling(self):
        print("Starting bot polling now")
        while True:
            try:
                print("New bot instance started")
                self.bot = telebot.TeleBot(self.API_KEY)  # Generate new bot instance
                self.bot_actions()  # If bot is used as a global variable, remove bot as an input param
                self.bot.polling(none_stop=True, interval=2, timeout=30)
            except Exception as ex:  # Error in polling
                print("Bot polling failed, restarting in {}sec. Error:\n{}".format(30, ex))
                self.bot.stop_polling()
                sleep(2)
            else:  # Clean exit
                self.bot.stop_polling()
            print("Bot polling loop finished")
            break  # End loop

    def is_valid_user(self, message) -> bool:
        user = crudUser.get_by_chat_id(db=session, chat_id=message.chat.id)
        if not user:
            self.bot.send_message(message.chat.id, trans('C_sorry_signup'))
            return False
        else:
            result = crudUser.check_expire(db=session, chat_id=message.chat.id)
            if result:
                return result
            else:
                self.bot.send_message(message.chat.id, trans('C_expire_plan'))
                return False

    def profile_command(self, message) -> bool:
        if message.text == trans('C_profile') or message.text == '/profile':
            return True
        else:
            return False

    def tutorial_command(self, message) -> bool:
        if message.text == trans('C_tutorials') or message.text == '/tutorial':
            return True
        else:
            return False

    def plan_command(self, message) -> bool:
        if message.text == trans('C_plans') or message.text == '/plans':
            return True
        else:
            return False

    def lang_command(self, message) -> bool:
        if message.text == trans('C_lang') or message.text == '/lang':
            return True
        else:
            return False

    def bot_actions(self):

        @self.bot.message_handler(func=self.profile_command)
        def profile(message):
            profile_option = types.InlineKeyboardMarkup(row_width=2)
            profile_option.add(
                types.InlineKeyboardButton(trans("C_edit_watchlists"),
                                           callback_data="profile_edit_strategies"),
                types.InlineKeyboardButton(trans('C_assets_exchange'),
                                           callback_data="profile_show_assets"),
                types.InlineKeyboardButton(trans("C_trades_history"),
                                           callback_data="profile_show_history")
            )

            plan = crudUser.get_plan_by_chat_id(db=session, chat_id=message.chat.id)
            plan_text = trans('C_plans') + '\n' + plan['name'] + '\n' + plan['valid_date'] + '\n\n'
            watchlists = crudWatchlist.get_by_chat_id(db=session, chat_id=message.chat.id)
            watchlist_text = trans('C_watchlists') + '\n'
            for watchlist in watchlists:
                sterategy = crudStrategy.get(db=session, id=watchlist.strategy_id)
                watchlist_text +=  watchlist.name + "\n" + trans('C_coin') + "\t"+ \
                                   watchlist.asset + '\n' + trans('C_exchange') + "\t" + watchlist.exchange + '\n' + \
                                   trans('C_strategy')+ "\t" + sterategy.name +  '\n' +trans('c_created_at') + "\t"+ str(watchlist.created)

            self.bot.send_message(chat_id=message.chat.id, text=plan_text + watchlist_text,
                                  reply_markup=profile_option)

        @self.bot.message_handler(func=lambda message: message.text == trans('C_help') or message.text == '/help')
        def help_me(message):
            try:
                self.bot.reply_to(message, trans("C_help_message"), parse_mode='Markdown')

            except Exception as e:
                self.bot.reply_to(message, trans("C_try_again"), reply_markup=start_keyboard())

        @self.bot.message_handler(func=dont_understand)
        def excuse(message):
            self.bot.send_message(message.chat.id, trans("C_dont_understand"), reply_markup=start_keyboard())

        @self.bot.message_handler(func=lambda message: message.text == trans('C_social_medias'))
        def social_media(message):
            try:
                key_markup = social_keyboard()
                self.bot.send_message(message.chat.id, trans("C_follow_us"),
                                      reply_markup=key_markup)

            except Exception as e:
                self.bot.reply_to(message, trans("C_try_again"), reply_markup=start_keyboard())

        @self.bot.message_handler(func=self.tutorial_command)
        def tutorials(message):
            try:
                self.bot.send_message(message.chat.id, trans('C_coming_soon'), reply_markup=start_keyboard())
            except Exception as e:
                self.bot.send_message(message, trans("C_error"), reply_markup=start_keyboard())


        @self.bot.message_handler(func=self.plan_command)
        def plan_charge(message):
            try:
                self.bot.reply_to(message, trans("C_charge_plan"))

            except Exception as e:
                self.bot.reply_to(message, trans("C_try_again"), reply_markup=start_keyboard())

        @self.bot.message_handler(func=self.lang_command)
        def lang_change(message):
            try:
                lang_option = types.InlineKeyboardMarkup(row_width=2)
                lang_option.add(types.InlineKeyboardButton('English',
                                                           callback_data="english"),
                                types.InlineKeyboardButton('فارسی',
                                                           callback_data="فارسی")
                                )
                self.bot.send_message(chat_id=message.chat.id, text=trans("C_choose_language"),
                                      reply_markup=lang_option)
            except Exception as e:
                self.bot.reply_to(message, trans("C_try_again"), reply_markup=start_keyboard())

        @self.bot.callback_query_handler(func=lambda call: call.data == 'english' or call.data == 'فارسی')
        def language_handler(call):
            if call.data == 'english':
                activate('en')
            else:
                activate('fa')
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            self.bot.send_message(chat_id=call.message.chat.id, text=f'{trans("C_done")}\n'
                                                                     f' {call.data} {trans("C_was_selected")}',
                                  reply_markup=start_keyboard())

        @self.bot.callback_query_handler(func=lambda call: 'profile_edit' in call.data)
        def profile_edit_handler(call):
            watchlists = crudWatchlist.get_by_chat_id(db=session, chat_id=call.message.chat.id)
            for watchlist in watchlists:
                strategy = crudStrategy.get(db=session, id=watchlist.strategy_id)
                strategies_option = types.InlineKeyboardMarkup(row_width=2)
                strategies_option.add(types.InlineKeyboardButton(trans('C_edit'),
                                                                 callback_data=str(watchlist.id) +
                                                                               "_edit_watchlist"),
                                      types.InlineKeyboardButton(trans('C_delete'),
                                                                 callback_data=str(watchlist.id) +
                                                                               "_delete_watchlist")
                                      )
                self.bot.send_message(chat_id=call.message.chat.id,
                                      text=f'{trans("C_coin")}: {watchlist.asset}\n'
                                           f'{trans("C_strategy")}: {strategy.name}\n'
                                           f'{trans("C_exchange")}: {watchlist.exchange}\n',
                                      reply_markup=strategies_option)

        @self.bot.callback_query_handler(func=lambda call: '_delete_watchlist' in call.data)
        def delete_watchlist_handler(call):
            query = str(call.data).split('_')
            crudWatchlist.remove(db=session, id=query[0])
            self.bot.send_message(chat_id=call.message.chat.id, text=trans("C_done"),
                                  reply_markup=start_keyboard())
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        @self.bot.callback_query_handler(func=lambda call: '_edit_watchlist' in call.data)
        def edit_watchlist_handler(call):
            query = str(call.data).split('_')
            watchlist = crudWatchlist.get(db=session, id=query[0])
            watchlist_update = WatchlistUpdate(name='new_name', exchange='new_exchange',
                                               public_key='public_key', secrete_key='new_secrete_key', asset='new_asset', chat_id=watchlist.chat_id,
                                               strategy_id=1)
            crudWatchlist.update(db=session, db_obj=watchlist, obj_in=watchlist_update)
            self.bot.send_message(chat_id=call.message.chat.id, text=trans("C_done"),
                                  reply_markup=start_keyboard())
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

        @self.bot.callback_query_handler(func=lambda call: 'profile_show_assets' == call.data)
        def show_assets_handler(call):
            watchlists = crudWatchlist.get_by_chat_id(db=session, chat_id=call.message.chat.id)
            for watchlist in watchlists:
                exchange = get_exchange(exchange=watchlist.exchange)
                if exchange:
                    exchange = exchange(public=watchlist.public_key, secret=watchlist.secrete_key)
                    assets = exchange.get_assets()
                    if not assets:
                        self.bot.send_message(chat_id=call.message.chat.id,text=watchlist.name + 'dont have valid API Keys or valid exchange update this wallet')
                    else:
                        self.bot.send_message(chat_id=call.message.chat.id,text=assets)
                else:
                    self.bot.send_message(chat_id=call.message.chat.id,text=watchlist.name + 'dont have valid API Keys or valid exchange update this wallet')
        
        @self.bot.callback_query_handler(func=lambda call: 'profile_show_history' == call.data)
        def show_assets_handler(call):
            self.bot.send_message(chat_id=call.message.chat.id,text='need to develop trade table')
            
            