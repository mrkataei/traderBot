"""
Mr.Kataei 8/4/2021
rest password needs connection to database which in Inc directory con_db() return it,
need hash function for password - any registration in app for now needs username
 , password , chat_id , question_id and answer -(roles(admin-user))
"""

from mysql.connector import MySQLConnection
from Inc.functions import chek_password , check_username ,hash_pass

def register(db_connection:MySQLConnection , username:str ,chat_id:str, password:str ,password2:str, question_id:int , answer:str ):
  cursor = db_connection.cursor()
  #check_password return tuple (bool,Error:str)
  chek_pass= chek_password(password=password , password2=password2)
  #check_username function return True if username not exists
  if not check_username(db_connection , username):
    return "username already exist"
  elif not chek_pass[0]:
    return chek_pass[1]
  else:
    password = hash_pass(password=password)
    sql = "INSERT INTO users (username, chat_id ,password , salt, role , question_id , question_answer ) VALUES (%s, %s , %s , %s , %s , %s , %s)"
    val = (username, chat_id ,password[0], password[1], 'user' ,  question_id, answer)
    cursor.execute(sql, val)
    #insert into database
    db_connection.commit()
    return "🥳welcome"