"""
Mr.Kataei 8/4/2021
rest password needs connection to database which in Inc directory con_db() return it,
need hash function for password - any registration in app for now needs username
 , password , chat_id , question_id and answer -(roles(admin-user))
"""

from Inc import functions
from Libraries.definitions import *
from datetime import timedelta, datetime


def register(username: str, chat_id: str, password: str, password2: str, plan_id: int,  question_id: int, answer: str):
    # check_password return tuple (bool,Error:str)
    result, error = functions.chek_password(password=password, password2=password2)
    # check_username function return True if username not exists
    if functions.check_username_exist(username):
        return trans('R_username_exist')
    elif not result:
        return error
    else:
        key, salt = functions.hash_pass(password=password)
        duration_days = functions.get_duration_plan(plan_id=plan_id)
        today_time = datetime.now()
        valid_time_plan = today_time + timedelta(days=duration_days)
        query = "INSERT INTO users (username, chat_id , password, salt, plan_id," \
                " valid_time_plan, question_id , answer) " \
                "VALUES (%s, %s , %s , %s , %s , %s , %s, %s)"
        val = (username, chat_id, key, salt, plan_id, valid_time_plan, question_id, answer)
        functions.insert_query(query=query, values=val)
        return True, trans('R_welcome')
