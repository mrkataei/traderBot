from Interfaces.telegram import Telegram

# master bot already run on vps dont use this @aitrdbot -> address
API_KEY = '2123917023:AAFPy9xoaJLt0BxqQJgC3J3F9km8F7ozdn8'
# @testkourosh2bot -> address // use this bot for test your code
# API_KEY = '1978536410:AAE_RMk3-4r_cLnt_nRcEnZHaSp-vIk9oVo'


class TempBot(Telegram):
    def __init__(self):
        Telegram.__init__(self, API_KEY=API_KEY)

    def bot_actions(self):
        @self.bot.message_handler(func=lambda message: True)
        def excuse(message):
            self.bot.send_message(message.chat.id, ' 👷🏼‍♂️ ربات در حال تعمیر و بروزرسانی است.\n'
                                                   'از صبر و شکیبایی شما متشکریم! ')

