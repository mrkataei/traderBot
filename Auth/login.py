import mysql.connector
from mysql.connector import MySQLConnection
from Auth.register import hash_pass


def login(db_connection:MySQLConnection , username:str , password:str):
  cursor = db_connection.cursor()
  try:
    query = 'SELECT * from users WHERE username="{username}" LIMIT 1'.format(username=username)
    cursor.execute(query)
    record = cursor.fetchall()
    if record and record[0][1] == hash_pass(password=password, salt=record[0][2])[0] :
      print("you are logged in")
    else:
      print("your username or password is incorrect")
  except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))