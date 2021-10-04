""""
Mr.Kataei 8/7/2021
all functions about queries from database define here, for now
soon this file must be cluster and to be multiple files
"""

from mysql.connector import Error
# import re
import hashlib
import random
from Inc.db import con_db


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


def check_username(username: str):
    try:
        query = "SELECT * from users WHERE username= '{username}' LIMIT 1".format(username=username)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        if record:
            return False
        else:
            return True
    except Error as err:
        return "Something went wrong: {}".format(err)


def check_chat_id(chat_id: str):
    try:
        query = "SELECT * from users WHERE chat_id= '{chat_id}' ".format(chat_id=chat_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        if record:
            return record[0][0]
        else:
            return False
    except Error as err:
        return "Something went wrong: {}".format(err)


def update_chat_id(username: str, chat_id: str):
    try:
        sql = "UPDATE users SET chat_id = '{chat_id}' WHERE username= '{username}'".format(chat_id=chat_id,
                                                                                           username=username)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_user_with_chat_id(chat_id: str):
    try:
        query = "SELECT username from users WHERE chat_id='{chat_id}' ".format(chat_id=chat_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record[0][0]
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_security_questions(question_id: int = -1):
    try:
        # question_id is optional by default is negative and return all questions
        # else return specific question
        if question_id > 0:
            query = "SELECT * from secrity_question WHERE id= {question_id}".format(question_id=question_id)
        else:
            query = "SELECT * from secrity_question"
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()

        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


# return question_id from users table
def get_user_security_id(username: str):
    try:
        query = "SELECT question_id from users WHERE username= '{username}'".format(username=username)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()

        return record[0][0]
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_user_watchlist(username: str, name: str = None):
    try:
        if not name:
            query = "SELECT * from watchlist WHERE user= '{username}' ".format(username=username)
        else:
            query = "SELECT * from watchlist WHERE user= '{username}'  " \
                    "AND name= '{name}' ".format(username=username, name=name)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_user_coins(username: str, watchlist: str = None):
    coins = []
    try:
        if watchlist:
            query = "SELECT coin_id from watchlist WHERE user= '{username}'  " \
                    "AND name= '{watchlist}' ".format(username=username, watchlist=watchlist)

        else:
            query = "SELECT coin_id from watchlist WHERE user= '{username}' ".format(username=username)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        for coin in record:
            if coin[0]:
                coins.append(get_coin_name(coin[0]))
        return coins

    except Error as err:
        return "Something went wrong: {}".format(err)


def create_watchlist(username: str, name: str):
    try:
        sql = "INSERT INTO watchlist (user ,name ) VALUES (%s, %s )"
        val = (username, name)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def set_coin(username: str, coin_id: int, watchlist_name: str):
    try:
        sql = "UPDATE watchlist SET coin_id ='{coin_id}' WHERE user='{username}' AND name='{watchlist_name}' AND  " \
              "coin_id IS NULL LIMIT 1".format(username=username, coin_id=coin_id, watchlist_name=watchlist_name)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return True, ""
    except Error as err:
        return False, "Something went wrong: {}".format(err)


def get_empty_coins_remain(username: str, watchlist_name: str):
    try:
        sql = "SELECT coin_id FROM watchlist WHERE user= '{username}' AND name= '{watchlist_name}' AND " \
              "coin_id IS NULL ".format(username=username, watchlist_name=watchlist_name)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        record = cursor.fetchall()

        return len(record)
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_coins():
    try:
        query = 'SELECT * from coins'
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_coin_name(coin_id: int):
    try:
        sql = "SELECT coin FROM coins WHERE id={coin_id}".format(coin_id=coin_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        record = cursor.fetchall()
        return record[0][0]
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_coin_id(coin_name: str):
    try:
        sql = "SELECT id FROM coins WHERE coin='{coin_name}'".format(coin_name=coin_name)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        record = cursor.fetchall()
        return record[0][0]
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_timeframe(timeframe_id: int = -1):
    try:
        if timeframe_id < 0:
            query = 'SELECT * from timeframes'
        else:
            query = "SELECT timeframe from timeframes WHERE id={timeframe_id}".format(timeframe_id=timeframe_id)

        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record

    except Error as err:
        return "Something went wrong: {}".format(err)


def update_timeframe(username: str, timeframe_id: int):
    try:
        sql = "UPDATE user_timeframe SET timeframe_id ={timeframe_id} WHERE " \
              "user='{username}' LIMIT 1".format(username=username, timeframe_id=timeframe_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def set_timeframe(username: str, timeframe_id: int):
    try:
        sql = "INSERT INTO user_timeframe (user ,timeframe_id ) VALUES (%s, %s )"
        val = (username, timeframe_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_user_timeframe(username: str):
    try:
        sql = "SELECT timeframe_id FROM user_timeframe WHERE user='{username}'".format(username=username)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        record = cursor.fetchall()
        record = get_timeframe(record[0][0])
        return record[0][0]
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_analysis(analysis_id: int = -1):
    try:
        if analysis_id < 0:
            query = "SELECT id , name from analysis"
        else:
            query = "SELECT name from analysis WHERE id={analysis_id}".format(analysis_id=analysis_id)

        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_user_chat_id(username: str):
    try:
        sql = "SELECT chat_id FROM users WHERE username='{username}'".format(username=username)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        record = cursor.fetchall()
        return record[0][0]
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_users_analysis_with_analysis_id(analysis_id: int):
    try:
        sql = "SELECT user FROM user_analysis WHERE analysis_id={analysis_id}".format(analysis_id=analysis_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_chat_id_with_analysis_id(analysis_id: int):
    chat_id = []
    try:
        sql = "SELECT user FROM user_analysis WHERE analysis_id={analysis_id}".format(analysis_id=analysis_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        record = cursor.fetchall()
        for user in record:
            chat_id.append(int(get_user_chat_id(user[0])))
        return chat_id
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_user_analysis_name(username: str):
    try:
        sql = "SELECT analysis_id FROM user_analysis WHERE user='{username}'".format(username=username)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        record = cursor.fetchall()
        if record:
            record = get_analysis(record[0][0])[0][0]
        else:
            record = False
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_user_analysis(username: str):
    try:
        sql = "SELECT * FROM user_analysis WHERE user='{username}'".format(username=username)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def set_user_analysis(username: str, analysis_id: int):
    try:
        sql = "INSERT INTO user_analysis (user ,analysis_id ) VALUES (%s, %s )"
        val = (username, analysis_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def set_amount_bank_user(username: str, amount: float):
    try:
        sql = "INSERT INTO bank (user ,amount ) VALUES (%s, %s )"
        val = (username, amount)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def update_amount_user(username: str, amount: float):
    try:
        sql = "UPDATE bank SET amount='{amount}' WHERE user='{username}'".format(amount=amount, username=username)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_amount_bank_user(username: str):
    try:
        sql = "SELECT amount FROM bank WHERE user='{username}'".format(username=username)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        record = cursor.fetchall()
        return record[0][0]
    except Error as err:
        return "Something went wrong: {}".format(err)


# get last signal inserted in database
def get_recommendations(analysis_id: int = None, timeframe_id: int = None, coin_id: int = None):
    try:
        if analysis_id and timeframe_id and coin_id:
            sql = "SELECT * FROM recommendations WHERE coin_id={coin_id} AND  analysis_id={analysis_id} AND " \
                  "timeframe_id={timeframe_id} order by timestmp DESC LIMIT 1".format(coin_id=coin_id,
                                                                                      analysis_id=analysis_id,
                                                                                      timeframe_id=timeframe_id)
        else:
            sql = "SELECT * FROM recommendations order by timestmp DESC LIMIT 1"
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def set_recommendation(analysis_id: int, coin_id: int, timeframe_id: int, position: str, target_price: float,
                       current_price: float, cost_price: float, risk: str):
    try:
        sql = "INSERT INTO recommendations (coin_id, analysis_id, position, target_price," \
              " current_price, timeframe_id, cost_price, risk) VALUES (%s, %s , %s ,%s, %s , %s ,%s ,%s)"
        val = (coin_id, analysis_id, position, target_price, current_price, timeframe_id, cost_price, risk)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def set_score(username: str, score: int, recom_id=int, is_used: int = 0):
    try:
        sql = "INSERT INTO score_analysis (recom_id, score, user, is_used) VALUES (%s, %s , %s ,%s)"
        val = (recom_id, score, username, is_used)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def set_null_coin_user(username: str, coin_id: int):
    try:
        sql = "UPDATE watchlist SET coin_id=NULL WHERE user='{username}' " \
              "AND coin_id={coin_id}".format(username=username, coin_id=coin_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_description_analysis(analysis_id: int):
    try:
        sql = "SELECT description FROM analysis WHERE id={analysis_id}".format(analysis_id=analysis_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        record = cursor.fetchall()
        return record[0][0]
    except Error as err:
        return "Something went wrong: {}".format(err)


def delete_watchlist(username: str, name: str):
    try:
        sql = "DELETE from watchlist WHERE user='{username}' AND name='{name}'".format(username=username, name=name)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def delete_analysis(username: str, analysis_id: int):
    try:
        sql = "DELETE from user_analysis WHERE user='{username}' " \
              "AND analysis_id={analysis_id}".format(username=username, analysis_id=analysis_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def pay_transaction(cost_price: float, username: str, detail: str = "some signal send"):
    try:
        amount = float(get_amount_bank_user(username)) - cost_price
        if float(amount) >= 0:
            update_amount_user(username, amount)
            sql = "INSERT INTO transactions (user, operation, amount, detail) VALUES (%s, %s ,%s ,%s )"
            val = (username, "deposit", cost_price, detail)
            connection = con_db()
            cursor = connection.cursor()
            cursor.execute(sql, val)
            connection.commit()
        else:
            return False
    except Error as err:
        return "Something went wrong: {}".format(err)


def charge_account(amount: float, username: str, detail: str = "charge account"):
    try:
        amount = float(get_amount_bank_user(username)) + amount
        update_amount_user(username, amount)
        sql = "INSERT INTO transactions (user, operation, amount, detail) VALUES (%s, %s ,%s ,%s )"
        val = (username, "withdrawal", amount, detail)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.execute(sql, val)
        connection.commit()

    except Error as err:
        return "Something went wrong: {}".format(err)


def get_all_user_watchlist():
    try:
        query = "SELECT * from watchlist"
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_all_user_analysis():
    try:
        query = "SELECT * from watchlist"
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_all_user_timeframe():
    try:
        query = "SELECT * from watchlist"
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_user_recommendation(coin_id: int = None, analysis_id: int = None, timeframe_id: int = None):
    try:
        if coin_id and analysis_id and timeframe_id:
            query = "SELECT watchlist.user , watchlist.coin_id , user_timeframe.timeframe_id ," \
                    "user_analysis.analysis_id  FROM watchlist INNER JOIN user_timeframe " \
                    "ON watchlist.user = user_timeframe.user INNER JOIN user_analysis " \
                    "ON user_timeframe.user = user_analysis.user " \
                    "WHERE coin_id ={coin_id} AND analysis_id={analysis_id} " \
                    "AND timeframe_id={timeframe_id}".format(coin_id=coin_id, analysis_id=analysis_id,
                                                             timeframe_id=timeframe_id)
        else:
            query = "SELECT watchlist.user , watchlist.coin_id , user_timeframe.timeframe_id ," \
                    "user_analysis.analysis_id  FROM watchlist INNER JOIN user_timeframe " \
                    "ON watchlist.user = user_timeframe.user INNER JOIN user_analysis " \
                    "ON user_timeframe.user = user_analysis.user "
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_admins():
    try:
        query = "SELECT username from users WHERE role='admin'"
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_usernames():
    try:
        query = "SELECT username from users"
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_user_details(username: str):
    try:
        query = "SELECT users.username , users.timestamp , users.role , bank.amount , user_timeframe.timeframe_id ," \
                "user_analysis.analysis_id FROM users LEFT JOIN bank ON users.username = bank.user " \
                "LEFT JOIN user_timeframe ON users.username = user_timeframe.user LEFT JOIN user_analysis " \
                "ON user_timeframe.user = user_analysis.user WHERE username='{username}'".format(username=username)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_chat_ids():
    try:
        query = "SELECT chat_id from users"
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_indicator_setting(indicator_setting_id: int):
    try:
        query = "SELECT settings from indicators_settings " \
                "WHERE id = {indicator_setting_id}".format(indicator_setting_id=indicator_setting_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        if record:
            parameters = record[0][0].split(',')
            record = dict()
            for parameter in parameters:
                parameter = parameter.split(':')
                try:
                    record[parameter[0]] = int(parameter[1])
                except Exception:
                    record[parameter[0]] = parameter[1]
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_analysis_setting(coin_id: int, timeframe_id: int, analysis_id: int):
    try:
        query = "SELECT analysis_setting , indicator_setting_id from analysis_setting WHERE coin_id = {coin_id} " \
                "AND timeframe_id = {timeframe_id} and analysis_id ={analysis_id}".format(coin_id=coin_id,
                                                                                          timeframe_id=timeframe_id,
                                                                                          analysis_id=analysis_id)
        connection = con_db()
        cursor = connection.cursor()
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
                        record['analysis_setting'][arg[0]] = int(arg[1])
                    except Exception:
                        record['analysis_setting'][arg[0]] = arg[1]
            record['indicators_setting'] = {}
            indicators = settings[1].split(',')
            for indicator in indicators:
                record['indicators_setting'][get_indicator_name_from_indicators_settings(indicator)] = \
                    get_indicator_setting(indicator)
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_indicator_id(indicator_name: str):
    try:
        query = "SELECT id from indicators " \
                "WHERE name ='{indicator_name}'".format(indicator_name=indicator_name)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()[0][0]
        return record

    except Error as err:
        return "Something went wrong: {}".format(err)


def get_indicator_name_from_indicators_settings(indicator_setting_id: int):
    try:
        query = "SELECT indicator_id from indicators_settings " \
                "WHERE id = {indicator_setting_id}".format(indicator_setting_id=indicator_setting_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        record = int(record[0][0])
        record = get_indicator_name(record)
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_all_indicator_settings():
    try:
        query = "SELECT settings,id FROM indicators_settings"
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_indicator_name(indicator_id: int):
    try:
        query = "SELECT name from indicators WHERE id = {indicator_id}".format(indicator_id=indicator_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        record = record[0][0]
        return record
    except Error as err:
        return "Something went wrong: {}".format(err)


def update_analysis_setting_string(coin_id: int, timeframe_id: int, analysis_id: int, analysis_setting: str):
    try:
        query = "UPDATE analysis_setting SET analysis_setting='{analysis_setting}' WHERE coin_id={coin_id} " \
                "AND timeframe_id={timeframe_id} " \
                "AND analysis_setting={analysis_id}".format(analysis_setting=analysis_setting,
                                                            coin_id=coin_id, timeframe_id=timeframe_id,
                                                            analysis_id=analysis_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def check_indicator_setting_exist(indicator_setting: str):
    records = get_all_indicator_settings()
    for record in records:
        if indicator_setting in record[0]:
            return True, int(record[1])


def set_indicator_setting(indicator_id: int, indicator_setting: str):
    try:
        sql = "INSERT INTO indicators_settings (indicator_id ,settings ) VALUES (%s, %s )"
        val = (indicator_id, indicator_setting)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def get_indicator_setting_id(setting: str):
    try:
        query = "SELECT id from indicators_settings WHERE settings = '{setting}'".format(setting=setting)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        if record:
            return record[0][0]
        else:
            return None
    except Error as err:
        return "Something went wrong: {}".format(err)


def update_analysis_setting_indicator_id(coin_id: int, timeframe_id: int, analysis_id: int, settings: dict):
    indicators_id_exist = ''
    for indicator in settings:
        res = check_indicator_setting_exist(settings[indicator])
        if res:
            indicators_id_exist += str(res[1]) + ','
        else:
            indicator_id = get_indicator_id(indicator)
            set_indicator_setting(indicator_id=indicator_id, indicator_setting=settings[indicator])
            indicators_id_exist += str(get_indicator_setting_id(settings[indicator])) + ','
    try:

        indicators_id_exist = indicators_id_exist.rstrip(indicators_id_exist[-1])
        query = "UPDATE analysis_setting SET indicator_setting_id='{indicator_setting_id}' WHERE coin_id={coin_id} " \
                "AND timeframe_id={timeframe_id} " \
                "AND analysis_id={analysis_id}".format(indicator_setting_id=indicators_id_exist,
                                                            coin_id=coin_id, timeframe_id=timeframe_id,
                                                            analysis_id=analysis_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)
