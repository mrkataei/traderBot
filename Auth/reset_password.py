"""
Mr.Kataei 8/4/2021
rest password needs connection to database which in Inc directory con_db() return it,
after all parameters satisfied then update database - methods check answer and set_password
is private and inner def in reset password for security
"""
import mysql.connector
from mysql.connector import MySQLConnection
from Inc.functions import chek_password ,check_username ,hash_pass

def reset_password(db_connection:MySQLConnection , username:str ,  answer:str , new_password:str , new_password2:str):
    cursor = db_connection.cursor()
    def check_answer():
        try:
            query = 'SELECT * FROM users WHERE username="{username}" AND question_answer="{answer}" LIMIT 1'.format(username=username , answer=answer)
            cursor.execute(query)
            record = cursor.fetchall()
            #if false wrong answer
            if record:
                return True
            else:
                return False
        except mysql.connector.Error as err:
            return "Something went wrong: {}".format(err)
    def set_password():
        #check 2 password input same and correct pattern
        chek_pass = chek_password(password=new_password, password2=new_password2)
        if not chek_pass[0]:
            print(chek_pass[1])
            return False
        else:
            try:
                cur = db_connection.cursor()
                #new pass hash with random salt return 2 elements password[pass][salt]
                password = hash_pass(password=new_password)
                sql = 'UPDATE users SET password="{password}" , salt="{salt}" WHERE username="{username}"'.format(password=password[0] ,salt=password[1] , username=username)
                cur.execute(sql)
                db_connection.commit()
                return True
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
                return False
    if check_username(db_connection , username):
        return  "user not exist"
    elif not check_answer():
        return "answer is wrong /start bot again"
    elif set_password():
        return "success /start to login"
    else:
        return "try again /start bot again"



