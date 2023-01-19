"""
Mr.Kataei 8/4/2021
rest password needs connection to database which in Inc directory con_db() return it,
need hash function for password - any registration in app for now needs username
 , password , chat_id , question_id and answer -(roles(admin-user))
"""
import hashlib
import random
from Inc import functions
from datetime import timedelta, datetime


def hash_pass(password: str, salt: int = random.randrange(124, 92452, 2)):
    # salt is optional and default is random number (124-92452) - take non-optional when login
    password = password + str(salt)
    key = hashlib.sha512(password.encode('utf-8')).hexdigest()
    return key, salt


def register(username: str, chat_id: str, phone: str):
    # free account plan id is 1
    duration_days = functions.get_duration_plan(plan_id=1)
    today_time = datetime.now()
    valid_time_plan = today_time + timedelta(days=duration_days)
    passwd, salt = hash_pass(password=phone)  # save hash phone for password - use for website future
    query = "INSERT INTO users (username, chat_id, phone, valid_time_plan, password, salt) " \
            "VALUES (%s, %s , %s, %s, %s, %s )"
    val = (username, chat_id, phone, valid_time_plan, passwd, salt)
    error, detail = functions.insert_query(query=query, values=val)
    return error, detail
