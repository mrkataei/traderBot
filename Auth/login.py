"""Mr.Kataei 8/4/2021
login needs connection to database which in Inc directory con_db() return it,
after this get 2 parameters username and password both of them string
return string  : if success login return "you are logged in" else "your username or password is incorrect"
login function need hash function already define in Auth.register to hash string plan text and sum with salt
and compare to database row
"""
import datetime

from Libraries.definitions import *
from Inc import functions
from datetime import datetime


def login(username: str, password: str):
    """
    :param username:
    :param password:
    :return:
    """
    query = "SELECT * from users WHERE username='{username}' LIMIT 1".format(username=username)
    record = functions.execute_query(query=query)
    if record:
        record = functions.record_dictionary(record=record[0], table='users')
        if record['password'] == functions.hash_pass(password=password, salt=record['salt'])[0]:
            if check_expire_plan(record['valid_time_plan']):
                update_user_online(username=username, online=True)
                return True, trans('L_successful_login')
            else:
                return False, 'your plan expire'
    else:
        return False, trans('L_invalid_login') + "\n" + trans("C_please_start")


def check_expire_plan(valid_date: datetime):
    """
    :param valid_date:
    :return:
    """
    now_time = datetime.now()
    if now_time <= valid_date:
        return True
    else:
        return False


def update_user_online(username: str, online: bool):
    """
    :param username:
    :param online:
    :return:
    """
    online = 1 if online else 0
    query = "UPDATE users SET is_online={online} WHERE username='{username}'".format(online=online, username=username)
    functions.update_query(query)
