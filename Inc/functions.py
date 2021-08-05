import mysql.connector
from mysql.connector import MySQLConnection
import re
import hashlib
import random


def hash_pass(password:str , salt:int=random.randrange(124 , 92452 , 2)):
  #salt is optional and default is random number (124-92452) - take non-optional when login
  password = password + str(salt)
  key = hashlib.sha512(password.encode('utf-8')).hexdigest()
  result = [key , salt]
  return result

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

def get_user_watchlist(db_connection:MySQLConnection , username:str , name:str=None):
  cursor = db_connection.cursor()
  try:
    # check user exist
    if not check_username(db_connection, username):
      if not name:
        query = 'SELECT * from watchlist WHERE user="{username}"'.format(username=username )
      else:
        query = 'SELECT * from watchlist WHERE user="{username}"  AND name="{name}"'.format(username=username , name=name)
      cursor.execute(query)
      record = cursor.fetchall()
      return record
    else:
      return False
  except mysql.connector.Error as err:
    return "Something went wrong: {}".format(err)

def create_watchlist(db_connection:MySQLConnection , username:str , name:str):
  cursor = db_connection.cursor()
  try:
    # check user exist
    if not check_username(db_connection, username):
      sql = "INSERT INTO watchlist (user ,name ) VALUES (%s, %s )"
      val = (username,name)
      cursor.execute(sql, val)
      db_connection.commit()
    else:
      return False
  except mysql.connector.Error as err:
    return "Something went wrong: {}".format(err)