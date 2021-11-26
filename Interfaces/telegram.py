"""
    Mr.Kataei 11/12/2021
"""
import telebot
from time import sleep


class Telegram:
    def __init__(self, API_KEY: str = '1987308624:AAHEYHcAYaeqiii2REcHMrSefohBSedWIxA'):
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

    def bot_actions(self):
        raise Exception("NotImplementedException")

