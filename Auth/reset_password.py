import mysql.connector
from mysql.connector import MySQLConnection
from Auth.register import check_username , hash_pass ,chek_password

def reset_password(db_connection:MySQLConnection , username:str ,  answer:str , new_password:str , new_password2:str):
    cursor = db_connection.cursor()
    def check_answer():
        try:
            query = 'SELECT * FROM users WHERE username="{username}" AND question_answer="{answer}" LIMIT 1'.format(username=username , answer=answer)
            cursor.execute(query)
            record = cursor.fetchall()
            if record:
                return True
            else:
                return False
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
    def set_password():
        chek_pass = chek_password(password=new_password, password2=new_password2)
        if not chek_pass[0]:
            print(chek_pass[1])
            return False
        else:
            try:
                cur = db_connection.cursor()
                password = hash_pass(password=new_password)
                sql = 'UPDATE users SET password="{password}" , salt="{salt}" WHERE username="{username}"'.format(password=password[0] ,salt=password[1] , username=username)
                cur.execute(sql)
                db_connection.commit()
                return True
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
                return False
    if check_username(db_connection , username):
        print("user not exist")
    elif not check_answer():
        print("answer is wrong")
    elif set_password():
        print("success")
    else:
        print("try agin")



