"""Mr.Kataei 8/4/2021
login needs connection to database which in Inc directory con_db() return it,
after this get 2 parameters username and password both of them string
return string  : if success login return "you are logged in" else "your username or password is incorrect"
login function need hash function already define in Auth.register to hash string plan text and sum with salt
and compare to database row
"""
from Libraries.definitions import *
from Inc import functions


def login(username: str, password: str):
    (connection, cursor) = functions.get_connection_and_cursor()
    try:
        query = "SELECT * from users WHERE username='{username}' LIMIT 1".format(username=username)
        cursor.execute(query)
        record = cursor.fetchall()
        if record and record[0][2] == functions.hash_pass(password=password, salt=record[0][3])[0]:
            return True, trans('L_successful_login')
        else:
            return False, trans('L_invalid_login') + "\n" + trans("C_please_start")
    # exception must be complete
    except functions.Error as err:
        return False, "Something went wrong: {}".format(err)
