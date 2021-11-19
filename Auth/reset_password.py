"""
Mr.Kataei 8/4/2021
rest password needs connection to database which in Inc directory con_db() return it,
after all parameters satisfied then update database - methods check answer and set_password
is private and inner def in reset password for security
"""
from Inc import functions
from Libraries.definitions import *


def reset_password(username: str, answer: str, new_password: str, new_password2: str):
    """
    :param username:
    :param answer:
    :param new_password:
    :param new_password2:
    :return:
    """
    def check_answer():
        """
        :return:
        """
        query = "SELECT * FROM users WHERE username='{username}' AND question_answer='{answer}' " \
                "LIMIT 1".format(username=username, answer=answer)
        record = functions.execute_query(query=query)
        # if false wrong answer
        if record:
            return True
        else:
            return False

    def set_password():
        """
        :return:
        """
        # check 2 password input same and correct pattern
        result, error = functions.chek_password(password=new_password, password2=new_password2)
        if not result:
            print(error)
            return result
        else:
            # new pass hash with random salt return 2 elements password[pass][salt]
            key, salt = functions.hash_pass(password=new_password)
            query = "UPDATE users SET password='{password}', salt={salt} " \
                    "WHERE username='{username}'".format(password=key, salt=salt, username=username)
            functions.update_query(query=query)
            return True

    if not functions.check_username_exist(username):
        return 'username not exist'
    elif not check_answer():
        return trans('R_wrong_answer') + "\n" + trans('C_please_start')
    elif set_password():
        return trans('R_success') + "\n" + trans('C_please_start')
    else:
        return trans('R_try_again') + "\n" + trans('C_please_start')
