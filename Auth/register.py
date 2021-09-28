"""
Mr.Kataei 8/4/2021
rest password needs connection to database which in Inc directory con_db() return it,
need hash function for password - any registration in app for now needs username
 , password , chat_id , question_id and answer -(roles(admin-user))
"""

from Inc import functions
from Libraries.definitions import *
from Inc.db import con_db


def register(username: str, chat_id: str, password: str, password2: str, question_id: int, answer: str):
    connection = con_db()
    # check_password return tuple (bool,Error:str)
    chek_pass = functions.chek_password(password=password, password2=password2)
    # check_username function return True if username not exists
    if not functions.check_username(username):
        return trans('R_username_exist')
    elif not chek_pass[0]:
        return chek_pass[1]
    else:
        password = functions.hash_pass(password=password)
        try:
            sql = "INSERT INTO users (username, chat_id ,password , salt, role , question_id , question_answer ) " \
                  "VALUES (%s, %s , %s , %s , %s , %s , %s)"
            val = (username, chat_id, password[0], password[1], 'user', question_id, answer)
            cursor = connection.cursor()
            cursor.execute(sql, val)
            # insert into database
            connection.commit()
            return "🥳" + trans('R_welcome')
        except functions.Error as err:
            print("Something went wrong: {}".format(err))
