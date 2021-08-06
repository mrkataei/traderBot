""""
Mr.Kataei 8/4/2021
there is 2way to connect database 1-use local static variable
2- set in environment on linux - first in local without any customers use local
in future use .env
for test your queries use here or import file like login,.. from Auth directory
"""
import mysql.connector
from Inc import functions
import numpy as np
#DB_HOST = os.getenv('DB_HOST')

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
    return "Something went wrong: {}".format(err)

# db = con_db()
# functions.set_amount_bank_user(db , "kouroshataei" , 1323545.6565)
# print(functions.get_amount_bank_user(db , "kouroshataei"))
# functions.set_user_analysis(db , "kouroshataei" , 1)
# print(functions.get_user_analysis(db , "kouroshataei"))
