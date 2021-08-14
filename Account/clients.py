"""
Mr.Kataei 8/4/2021
use for telegram bot to register and login and logout
"""
class User:
    def __init__(self):
        self.username = None
        self.session = None
        self.watchlist = []
        self.temp_watch = None
        self.coin = None
        self.analysis =None

class Register:
    def __init__(self ,chat_id):
        self.chat_id = chat_id
        self.username:str
        self.password1:str
        self.password2:str
        self.security_question_id:int
        self.security_question:str
        self.security_answer:str
