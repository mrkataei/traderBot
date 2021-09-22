""""
Mr.Kataei 8/7/2021
all functions about queries from database define here, for now
soon this file must be cluster and to be multiple files
"""

import mysql.connector
from mysql.connector import MySQLConnection
# import re
import hashlib
import random


def hash_pass(password: str, salt: int = random.randrange(124, 92452, 2)):
    # salt is optional and default is random number (124-92452) - take non-optional when login
    password = password + str(salt)
    key = hashlib.sha512(password.encode('utf-8')).hexdigest()
    result = [key, salt]
    return result


# check password format
def chek_password(password: str, password2: str):
    if len(password) < 8:
        result = (False, "password is too short")
    elif password != password2:
        result = (False, "passwords not match")
    # elif not re.fullmatch("^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$", password):
    # result = (False, "password must be content 0-9 digit and capital and lower char and include one of {@#$%^&+=} ")
    else:
        result = (True, "Success")
    return result


def check_username(db_connection: MySQLConnection, username: str):
    cursor = db_connection.cursor()
    try:
        query = f'SELECT * from users WHERE username="{username}" LIMIT 1'
        cursor.execute(query)
        record = cursor.fetchall()
        if record:
            return False
        else:
            return True
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def check_chat_id(db_connection: MySQLConnection, chat_id: str):
    cursor = db_connection.cursor()
    try:
        query = f'SELECT * from users WHERE chat_id="{chat_id}"'
        cursor.execute(query)
        record = cursor.fetchall()
        if record:
            return record[0][0]
        else:
            return False
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def update_chat_id(db_connection: MySQLConnection, username: str, chat_id: str):
    cursor = db_connection.cursor()
    try:
        sql = f'UPDATE users SET chat_id ="{chat_id}" WHERE username="{username}" LIMIT 1'
        cursor.execute(sql)
        db_connection.commit()
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_user_with_chat_id(db_connection: MySQLConnection, chat_id: str):
    cursor = db_connection.cursor()
    try:
        # check user exist
        query = f'SELECT username from users WHERE chat_id="{chat_id}" LIMIT 1'
        cursor.execute(query)
        record = cursor.fetchall()
        return record[0][0]
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


# this is for telebot no for register
def get_security_questions(db_connection: MySQLConnection, question_id: int = -1):
    cursor = db_connection.cursor()
    try:
        # question_id is optional by default is negative and return all questions
        # else return specific question
        if question_id > 0:
            query = f'SELECT * from secrity_question WHERE id="{question_id}" LIMIT 1'
        else:
            query = 'SELECT * from secrity_question '
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


# return question_id from users table
def get_user_security_id(db_connection: MySQLConnection, username: str):
    cursor = db_connection.cursor()
    try:
        # check user exist
        if not check_username(db_connection, username):
            query = f'SELECT question_id from users WHERE username="{username}" LIMIT 1'
            cursor.execute(query)
            record = cursor.fetchall()
            return record[0][0]
        else:
            return False
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_user_watchlist(db_connection: MySQLConnection, username: str, name: str = None):
    cursor = db_connection.cursor()
    try:
        # check user exist
        if not check_username(db_connection, username):
            if not name:
                query = f'SELECT * from watchlist WHERE user="{username}"'
            else:
                query = f'SELECT * from watchlist WHERE user="{username}"  AND name="{name}"'
            cursor.execute(query)
            record = cursor.fetchall()
            return record
        else:
            return False
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_user_coins(db_connection: MySQLConnection, username: str, watchlist: str = None):
    cursor = db_connection.cursor()
    coins = []
    try:
        if watchlist:
            query = f'SELECT coin_id from watchlist WHERE user="{username}"  AND name="{watchlist}"'

        else:
            query = f'SELECT coin_id from watchlist WHERE user="{username}"'

        cursor.execute(query)
        record = cursor.fetchall()
        for coin in record:
            if coin[0]:
                coins.append(get_coin_name(db_connection, coin[0]))
        return coins

    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def create_watchlist(db_connection: MySQLConnection, username: str, name: str):
    cursor = db_connection.cursor()
    try:
        # check user exist
        if not check_username(db_connection, username):
            sql = "INSERT INTO watchlist (user ,name ) VALUES (%s, %s )"
            val = (username, name)
            cursor.execute(sql, val)
            db_connection.commit()
        else:
            return False
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def set_coin(db_connection: MySQLConnection, username: str, coin_id: int, watchlist_name: str):
    cursor = db_connection.cursor()
    try:
        # check user exist
        if not check_username(db_connection, username):
            sql = f'UPDATE watchlist SET coin_id ="{coin_id}" WHERE user="{username}" AND name="{watchlist_name}" ' \
                  'AND  coin_id IS NULL LIMIT 1'
            cursor.execute(sql)
            db_connection.commit()
            return True, ""
        else:
            return False, ""
    except mysql.connector.Error as err:
        return False, "Something went wrong: {}".format(err)


def get_empty_coins_remain(db_connection: MySQLConnection, username: str, watchlist_name: str):
    cursor = db_connection.cursor()
    try:
        # check user exist
        if not check_username(db_connection, username):
            sql = f'SELECT coin_id FROM watchlist WHERE user="{username}" ' \
                  f'AND name="{watchlist_name}"  AND coin_id IS NULL '
            cursor.execute(sql)
            record = cursor.fetchall()
            return len(record)
        else:
            return False
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_coins(db_connection: MySQLConnection):
    cursor = db_connection.cursor()
    try:
        query = 'SELECT * from coins'
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_coin_name(db_connection: MySQLConnection, coin_id: int):
    cursor = db_connection.cursor()
    try:
        # check user exist
        sql = f'SELECT coin FROM coins WHERE id="{coin_id}" '
        cursor.execute(sql)
        record = cursor.fetchall()
        return record[0][0]
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_coin_id(db_connection: MySQLConnection, coin_name: str):
    cursor = db_connection.cursor()
    try:
        # check user exist
        sql = f'SELECT id FROM coins WHERE coin="{coin_name}" '
        cursor.execute(sql)
        record = cursor.fetchall()
        return record[0][0]
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_timeframe(db_connection: MySQLConnection, timeframe_id: int = -1):
    cursor = db_connection.cursor()
    try:
        if timeframe_id < 0:
            query = 'SELECT * from timeframes'
        else:
            query = f'SELECT timeframe from timeframes WHERE id="{timeframe_id}"'

        cursor.execute(query)
        record = cursor.fetchall()
        return record

    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def update_timeframe(db_connection: MySQLConnection, username: str, timeframe_id: int):
    cursor = db_connection.cursor()
    try:
        # check user exist
        if not check_username(db_connection, username):
            sql = f'UPDATE user_timeframe SET timeframe_id ="{timeframe_id}"' \
                  f' WHERE user="{username}" LIMIT 1'
            cursor.execute(sql)
            db_connection.commit()
        else:
            return False
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def set_timeframe(db_connection: MySQLConnection, username: str, timeframe_id: int):
    cursor = db_connection.cursor()
    try:
        # check user exist
        if not check_username(db_connection, username):
            sql = "INSERT INTO user_timeframe (user ,timeframe_id ) VALUES (%s, %s )"
            val = (username, timeframe_id)
            cursor.execute(sql, val)
            db_connection.commit()
        else:
            return False
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_user_timeframe(db_connection: MySQLConnection, username: str):
    cursor = db_connection.cursor()
    try:
        sql = f'SELECT timeframe_id FROM user_timeframe WHERE user="{username}"'
        cursor.execute(sql)
        record = cursor.fetchall()
        record = get_timeframe(db_connection, record[0][0])
        return record[0][0]
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_analysis(db_connection: MySQLConnection, analysis_id: int = -1):
    cursor = db_connection.cursor()
    try:
        # check user exist
        if analysis_id < 0:
            query = 'SELECT * from analysis'
        else:
            query = f'SELECT name from analysis WHERE id="{analysis_id}"'

        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_user_chat_id(db_connection: MySQLConnection, username: str):
    cursor = db_connection.cursor()
    try:
        # check user exist
        if not check_username(db_connection, username):
            sql = f'SELECT chat_id FROM users WHERE username="{username}"'
            cursor.execute(sql)
            record = cursor.fetchall()
            return record[0][0]
        else:
            return False
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_users_analysis_with_analysis_id(db_connection: MySQLConnection, analysis_id: int):
    cursor = db_connection.cursor()
    try:
        sql = f'SELECT user FROM user_analysis WHERE analysis_id="{analysis_id}"'
        cursor.execute(sql)
        record = cursor.fetchall()
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_chat_id_with_analysis_id(db_connection: MySQLConnection, analysis_id: int):
    cursor = db_connection.cursor()
    chat_id = []
    try:
        sql = f'SELECT user FROM user_analysis WHERE analysis_id="{analysis_id}"'
        cursor.execute(sql)
        record = cursor.fetchall()
        for user in record:
            chat_id.append(int(get_user_chat_id(db_connection, user[0])))
        return chat_id
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_user_analysis_name(db_connection: MySQLConnection, username: str):
    cursor = db_connection.cursor()
    try:
        # check user exist
        if not check_username(db_connection, username):
            sql = f'SELECT analysis_id FROM user_analysis WHERE user="{username}"'
            cursor.execute(sql)
            record = cursor.fetchall()
            if record:
                record = get_analysis(db_connection, record[0][0])[0][0]
            else:
                record = False
            return record
        else:
            return False
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_user_analysis(db_connection: MySQLConnection, username: str):
    cursor = db_connection.cursor()
    try:
        # check user exist
        if not check_username(db_connection, username):
            sql = f'SELECT * FROM user_analysis WHERE user="{username}"'
            cursor.execute(sql)
            record = cursor.fetchall()
            return record
        else:
            return False
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def set_user_analysis(db_connection: MySQLConnection, username: str, analysis_id: int):
    cursor = db_connection.cursor()
    try:
        # check user exist
        if not check_username(db_connection, username):
            sql = "INSERT INTO user_analysis (user ,analysis_id ) VALUES (%s, %s )"
            val = (username, analysis_id)
            cursor.execute(sql, val)
            db_connection.commit()
        else:
            return False
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def set_amount_bank_user(db_connection: MySQLConnection, username: str, amount: float):
    cursor = db_connection.cursor()
    try:
        # check user exist
        if not check_username(db_connection, username):
            sql = "INSERT INTO bank (user ,amount ) VALUES (%s, %s )"
            val = (username, amount)
            cursor.execute(sql, val)
            db_connection.commit()
        else:
            return False
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def update_amount_user(db_connection: MySQLConnection, username: str, amount: float):
    cursor = db_connection.cursor()
    try:
        sql = f'UPDATE bank SET amount="{amount}" WHERE user="{username}" '
        cursor.execute(sql)
        db_connection.commit()
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_amount_bank_user(db_connection: MySQLConnection, username: str):
    cursor = db_connection.cursor()
    try:
        # check user exist
        if not check_username(db_connection, username):
            sql = f'SELECT amount FROM bank WHERE user="{username}"'
            cursor.execute(sql)
            record = cursor.fetchall()
            return record[0][0]
        else:
            return False
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


# get last signal inserted in database
def get_recommendations(db_connection: MySQLConnection, analysis_id: int = None, timeframe: id = None,
                        coin_id: int = None):
    cursor = db_connection.cursor()
    try:
        if analysis_id and timeframe and coin_id:
            sql = f'SELECT * FROM recommendations WHERE coin_id="{coin_id}" ' \
                  f'AND  analysis_id="{analysis_id}" AND timeframe_id={timeframe} order by timestmp DESC LIMIT 1'
        else:
            sql = f'SELECT * FROM recommendations order by timestmp DESC LIMIT 1'
        cursor.execute(sql)
        record = cursor.fetchall()
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def set_recommendation(db_connection: MySQLConnection, analysis_id: int
                       , coin_id: int, timeframe_id: int, position: str,
                       target_price: float, current_price: float, cost_price: float, risk: str):
    cursor = db_connection.cursor()
    try:
        sql = "INSERT INTO recommendations (coin_id, analysis_id, position, target_price," \
              " current_price, timeframe_id, cost_price, risk) VALUES (%s, %s , %s ,%s, %s , %s ,%s ,%s)"
        val = (coin_id, analysis_id, position, target_price, current_price, timeframe_id, cost_price, risk)
        cursor.execute(sql, val)
        db_connection.commit()
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def set_score(db_connection: MySQLConnection, username: str, score: int, recom_id=int, is_used: int = 0):
    cursor = db_connection.cursor()
    try:
        sql = "INSERT INTO score_analysis (recom_id, score, user, is_used) VALUES (%s, %s , %s ,%s)"
        val = (recom_id, score, username, is_used)
        cursor.execute(sql, val)
        db_connection.commit()
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def set_null_coin_user(db_connection: MySQLConnection, username: str, coin_id: int):
    cursor = db_connection.cursor()
    try:
        sql = f'UPDATE watchlist SET coin_id=NULL WHERE user="{username}" AND coin_id="{coin_id}"'
        cursor.execute(sql)
        db_connection.commit()
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def delete_watchlist(db_connection: MySQLConnection, username: str, name: str):
    cursor = db_connection.cursor()
    try:
        sql = f'DELETE from watchlist WHERE user="{username}" AND name="{name}"'
        cursor.execute(sql)
        db_connection.commit()
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def delete_analysis(db_connection: MySQLConnection, username: str, analysis_id: int):
    cursor = db_connection.cursor()
    try:
        sql = f'DELETE from user_analysis WHERE user="{username}" AND analysis_id="{analysis_id}"'
        cursor.execute(sql)
        db_connection.commit()
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def pay_transaction(db_connection: MySQLConnection, cost_price: float, username: str, detail: str = "some signal send"):
    cursor = db_connection.cursor()
    try:
        amount = float(get_amount_bank_user(db_connection, username)) - cost_price
        if float(amount) >= 0:
            update_amount_user(db_connection, username, amount)
            sql = "INSERT INTO transactions (user, operation, amount, detail) VALUES (%s, %s ,%s ,%s )"
            val = (username, "deposit", cost_price, detail)
            cursor.execute(sql, val)
            db_connection.commit()
        else:
            return False
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def charge_account(db_connection: MySQLConnection, amount: float, username: str, detail: str = "charge account"):
    cursor = db_connection.cursor()
    try:
        amount = float(get_amount_bank_user(db_connection, username)) + amount
        update_amount_user(db_connection, username, amount)
        sql = "INSERT INTO transactions (user, operation, amount, detail) VALUES (%s, %s ,%s ,%s )"
        val = (username, "withdrawal", amount, detail)
        cursor.execute(sql, val)
        db_connection.commit()

    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_all_user_watchlist(db_connection: MySQLConnection):
    cursor = db_connection.cursor()
    try:
        query = f'SELECT * from watchlist'
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_all_user_analysis(db_connection: MySQLConnection):
    cursor = db_connection.cursor()
    try:
        query = f'SELECT * from watchlist'
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_all_user_timeframe(db_connection: MySQLConnection):
    cursor = db_connection.cursor()
    try:
        query = f'SELECT * from watchlist'
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_user_recommendation(db_connection: MySQLConnection, coin_id: int = None, analysis_id: int = None,
                            timeframe_id: int = None):
    cursor = db_connection.cursor()
    try:
        if coin_id and analysis_id and timeframe_id:
            query = f'SELECT watchlist.user , watchlist.coin_id , user_timeframe.timeframe_id ,' \
                    f'user_analysis.analysis_id  FROM watchlist ' \
                    f'INNER JOIN user_timeframe ON watchlist.user = user_timeframe.user ' \
                    f'INNER JOIN user_analysis ON user_timeframe.user = user_analysis.user ' \
                    f'WHERE coin_id ="{coin_id}" AND analysis_id="{analysis_id}" AND timeframe_id="{timeframe_id}"'
        else:
            query = f'SELECT watchlist.user , watchlist.coin_id , user_timeframe.timeframe_id ,' \
                    f'user_analysis.analysis_id  FROM watchlist ' \
                    f'INNER JOIN user_timeframe ON watchlist.user = user_timeframe.user ' \
                    f'INNER JOIN user_analysis ON user_timeframe.user = user_analysis.user '
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_admins(db_connection: MySQLConnection):
    cursor = db_connection.cursor()
    admin = 'admin'
    try:
        query = f'SELECT username from users WHERE role="{admin}"'
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_usernames(db_connection: MySQLConnection):
    cursor = db_connection.cursor()
    try:
        query = f'SELECT username from users'
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_user_details(db_connection: MySQLConnection, username: str):
    cursor = db_connection.cursor()
    try:

        query = f'SELECT users.username , users.timestamp , users.role , bank.amount , user_timeframe.timeframe_id ,' \
                f'user_analysis.analysis_id FROM users ' \
                f'LEFT JOIN bank ON users.username = bank.user ' \
                f'LEFT JOIN user_timeframe ON users.username = user_timeframe.user  ' \
                f'LEFT JOIN user_analysis ON user_timeframe.user = user_analysis.user ' \
                f'WHERE username="{username}"'
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def set_accuracy(db_connection: MySQLConnection, recom_id: int, validity: int):
    cursor = db_connection.cursor()
    try:
        sql = "INSERT INTO accuracy (recom_id, validity) VALUES (%s, %s )"
        val = (recom_id, validity)
        cursor.execute(sql, val)
        db_connection.commit()
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_chat_ids(db_connection: MySQLConnection):
    cursor = db_connection.cursor()
    try:
        query = f'SELECT chat_id from users'
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_indicator_setting(db_connection: MySQLConnection, indicator_setting_id: int):
    cursor = db_connection.cursor()
    try:
        query = f'SELECT settings from indicators_settings WHERE id = "{indicator_setting_id}"'
        cursor.execute(query)
        record = cursor.fetchall()
        if record:
            parameters = record[0][0].split(',')
            record = dict()
            for parameter in parameters:
                parameter = parameter.split(':')
                try:
                    record[parameter[0]] = float(parameter[1])
                except Exception as e:
                    record[parameter[0]] = parameter[1]
                    print(e)
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_analysis_setting(db_connection: MySQLConnection, coin_id: int, timeframe_id: int, analysis_id: int):
    cursor = db_connection.cursor()
    try:
        query = f'SELECT analysis_setting , indicator_setting_id from analysis_setting WHERE coin_id = "{coin_id}" and ' \
                f'timeframe_id = "{timeframe_id}" and analysis_id = "{analysis_id}"'
        cursor.execute(query)
        record = cursor.fetchall()
        if record:
            settings = record[0]
            record = dict()
            record['analysis_setting'] = {}
            if settings[0]:
                args = settings[0].split(',')
                for arg in args:
                    arg = arg.split(':')
                    try:
                        record['analysis_setting'][arg[0]] = float(arg[1])
                    except Exception as e:
                        record['analysis_setting'][arg[0]] = arg[1]
                        print(e)
            record['indicators_setting'] = {}
            indicators = settings[1].split(',')
            for indicator in indicators:
                record['indicators_setting'][get_indicator_name_from_indicators_settings(db_connection, indicator)] = \
                    get_indicator_setting(db_connection, indicator)
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_indicator_name_from_indicators_settings(db_connection: MySQLConnection, indicator_setting_id: int):
    cursor = db_connection.cursor()
    try:
        query = f'SELECT indicator_id from indicators_settings WHERE id = "{indicator_setting_id}"'
        cursor.execute(query)
        record = int(cursor.fetchall()[0][0])
        record = get_indicator_name(db_connection, record)
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)


def get_indicator_name(db_connection: MySQLConnection, indicator_id: int):
    cursor = db_connection.cursor()
    try:
        query = f'SELECT name from indicators WHERE id = "{indicator_id}"'
        cursor.execute(query)
        record = cursor.fetchall()[0][0]
        return record
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)