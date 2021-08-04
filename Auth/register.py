"""
Mr.Kataei 8/4/2021
rest password needs connection to database which in Inc directory con_db() return it,
need hash function for password - any registration in app for now needs username
 , password , chat_id , question_id and answer -(roles(admin-user))
"""
import hashlib
import random
import mysql.connector
from mysql.connector import MySQLConnection
import re

def hash_pass(password:str , salt:int=random.randrange(124 , 92452 , 2)):
  #salt is optional and default is random number (124-92452) - take non-optional when login
  password = password + str(salt)
  key = hashlib.sha512(password.encode('utf-8')).hexdigest()
  result = [key , salt]
  return result

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
#check password format
def chek_password(password:str , password2:str):
  if len(password) < 8 :
    result = (False, "password is too short" )
  elif password != password2 :
    result = (False, "passwords not match")
  elif not re.fullmatch("^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$" , password):
    result = (False, "password must be content 0-9 digit and capital and lower char and include one of {@#$%^&+=} ")
  else:
    result = (True, "Success")
  return result

def check_username(db_connection:MySQLConnection , username:str):
  cursor = db_connection.cursor()
  try:
    query = 'SELECT * from users WHERE username="{username}" LIMIT 1'.format(username=username)
    cursor.execute(query)
    record = cursor.fetchall()
    if record:
      return False
    else:
      return True
  except mysql.connector.Error as err:
    return "Something went wrong: {}".format(err)

#this is for telebot no for register
def get_security_questions(db_connection:MySQLConnection , question_id:int=-1):
  cursor = db_connection.cursor()
  try:
    #question_id is optional by default is negative and return all questions
    #else return specific question
    if question_id>0:
      query = 'SELECT * from secrity_question WHERE id="{id}" LIMIT 1'.format(id=question_id)
    else:
      query = 'SELECT * from secrity_question '
    cursor.execute(query)
    record = cursor.fetchall()
    return record
  except mysql.connector.Error as err:
    return "Something went wrong: {}".format(err)

#return question_id from users table
def get_user_security_id(db_connection:MySQLConnection , username:str):
  cursor = db_connection.cursor()
  try:
    #check user exist
    if not check_username(db_connection , username):
      query = 'SELECT question_id from users WHERE username="{username}" LIMIT 1'.format(username=username)
      cursor.execute(query)
      record = cursor.fetchall()
      return record[0][0]
    else:
      return False
  except mysql.connector.Error as err:
    return "Something went wrong: {}".format(err)