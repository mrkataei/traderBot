"""Mr.Kataei 8/4/2021
login needs connection to database which in Inc directory con_db() return it,
after this get 2 parameters username and password both of them string
return string  : if success login return "you are logged in" else "your username or password is incorrect"
login function need hash function already define in Auth.register to hash string plan text and sum with salt
and compare to database row
"""
import mysql.connector
from mysql.connector import MySQLConnection
from Inc.functions import hash_pass


def login(db_connection:MySQLConnection , username:str , password:str):
  cursor = db_connection.cursor()
  try:
    query = 'SELECT * from users WHERE username="{username}" LIMIT 1'.format(username=username)
    cursor.execute(query)
    record = cursor.fetchall()
    if record and record[0][2] == hash_pass(password=password, salt=record[0][3])[0] :
      return "You are logged in🤩"
    else:
      return "Your username or password is incorrect🥵\n" \
             "Try again /start"
  #exception must be complete
  except mysql.connector.Error as err:
    return "Something went wrong: {}".format(err)
    #kourosh