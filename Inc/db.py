import mysql.connector
from Auth import login , register ,reset_password

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
db = con_db()
# for row in records:
#   print(row)
#
# print(mycursor.rowcount, "record inserted.")
# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#   print(x)

# mycursor.execute("SHOW TABLES")