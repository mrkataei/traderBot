import mysql.connector
from mysql.connector import MySQLConnection
import os
import hashlib
import random

#mrkataei.mysql.pythonanywhere-services.com -> hostname
#username -> mrkataei
#password
# DB_HOST = os.getenv('DB_HOST')
DB_HOST = "localhost"
DB_NAME = "algowatch"
DB_USERNAME = "root"
DB_PASSWORD = ""
def con_db():
  try:
    database = mysql.connector.connect(
      host=DB_HOST,
      user=DB_USERNAME,
      password=DB_PASSWORD,
      database=DB_NAME
    )
    return database
  except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))

def hash_pass(password:str , salt:int=random.randrange(124 , 92452 , 2)):
  password = password + str(salt)
  key = hashlib.sha512(password.encode('utf-8')).hexdigest()
  result = [key , salt]
  return result

def login(db_connection:MySQLConnection , username:str , password:str):
  cursor = db_connection.cursor()
  try:
    query = 'SELECT * from users WHERE username="{username}" LIMIT 1'.format(username=username)
    cursor.execute(query)
    record = cursor.fetchall()
    if record[0][1] == hash_pass(password=password, salt=record[0][2])[0]:
      print("you are logged in")
    else:
      print("your username or password is incorrect")
  except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))

def register(db_connection:MySQLConnection , username:str , password:str , question_id:int , answer:str ):
  cursor = db_connection.cursor()
  password = hash_pass(password=password)
  sql = "INSERT INTO users (username, password , role , question_id , question_answer ) VALUES (%s, %s , %s , %s , %s)"
  val = (username, password[0], password[1], question_id, answer)
  cursor.execute(sql, val)
  db.commit()

db = con_db()
# register(db , "kami2021" , "123456789" , 1 , "qoli")
# login(db , "kami2021" , "123456789")


# for row in records:
#   print(row)
#
# print(mycursor.rowcount, "record inserted.")
# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#   print(x)

# mycursor.execute("SHOW TABLES")