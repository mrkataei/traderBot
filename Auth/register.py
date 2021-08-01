import hashlib
import random
import mysql.connector
from mysql.connector import MySQLConnection
import re

def hash_pass(password:str , salt:int=random.randrange(124 , 92452 , 2)):
  password = password + str(salt)
  key = hashlib.sha512(password.encode('utf-8')).hexdigest()
  result = [key , salt]
  return result

def register(db_connection:MySQLConnection , username:str , password:str , question_id:int , answer:str ):
  cursor = db_connection.cursor()
  chek_pass= chek_password(password=password , password2=password)
  if not check_username(db_connection , username):
    print("username already exist")
  elif not chek_pass[0]:
    print(chek_pass[1])
  else:
    password = hash_pass(password=password)
    sql = "INSERT INTO users (username, password , salt, role , question_id , question_answer ) VALUES (%s, %s , %s , %s , %s , %s)"
    val = (username, password[0], password[1], 'user' ,  question_id, answer)
    cursor.execute(sql, val)
    db_connection.commit()

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
    print("Something went wrong: {}".format(err))