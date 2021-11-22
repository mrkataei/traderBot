"""
Mr.Kataei 8/4/2021
rest password needs connection to database which in Inc directory con_db() return it,
need hash function for password - any registration in app for now needs username
 , password , chat_id , question_id and answer -(roles(admin-user))
"""

from Inc import functions
from datetime import timedelta, datetime


def register(username: str, chat_id: str, phone: str):
    # free account plan id is 1
    duration_days = functions.get_duration_plan(plan_id=1)
    today_time = datetime.now()
    valid_time_plan = today_time + timedelta(days=duration_days)
    query = "INSERT INTO users (username, chat_id, phone, valid_time_plan) VALUES (%s, %s , %s, %s)"
    val = (username, chat_id, phone, valid_time_plan)
    error, detail = functions.insert_query(query=query, values=val)
    return error, detail

