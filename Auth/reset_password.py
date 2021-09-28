"""
Mr.Kataei 8/4/2021
rest password needs connection to database which in Inc directory con_db() return it,
after all parameters satisfied then update database - methods check answer and set_password
is private and inner def in reset password for security
"""
from Inc import functions
from Libraries.definitions import *


def reset_password(username: str, answer: str, new_password: str, new_password2: str):
    (connection, cursor) = functions.get_connection_and_cursor()

    def check_answer():
        try:
            query = "SELECT * FROM users WHERE username='{username}' AND question_answer='{answer}' " \
                    "LIMIT 1".format(username=username, answer=answer)
            cursor.execute(query)
            record = cursor.fetchall()
            # if false wrong answer
            if record:
                return True
            else:
                return False
        except functions.Error as err:
            return "Something went wrong: {}".format(err)

    def set_password():
        # check 2 password input same and correct pattern
        chek_pass = functions.chek_password(password=new_password, password2=new_password2)
        if not chek_pass[0]:
            print(chek_pass[1])
            return False
        else:
            try:
                # new pass hash with random salt return 2 elements password[pass][salt]
                password = functions.hash_pass(password=new_password)
                sql = "UPDATE users SET password='{password}', salt='{salt}' " \
                      "WHERE username='{username}'".format(password=password[0], salt=password[1], username=username)
                cursor.execute(sql)
                connection.commit()
                return True
            except functions.Error as err:
                print("Something went wrong: {}".format(err))
                return False

    if functions.check_username(username):
        return trans('C_username_exist')
    elif not check_answer():
        return trans('R_wrong_answer') + "\n" + trans('C_please_start')
    elif set_password():
        return trans('R_success') + "\n" + trans('C_please_start')
    else:
        return trans('R_try_again') + "\n" + trans('C_please_start')
