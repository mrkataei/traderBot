""""
Mr.Kataei 8/7/2021
all functions about queries from database define here, for now
soon this file must be cluster and to be multiple files
"""

from mysql.connector import Error

from Inc.db import con_db
from datetime import datetime


# queries function : update , insert , delete , fetch
def update_query(query: str):
    """
    :param query:
    :return:
    """
    try:
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except Error as err:
        return f'Something went wrong: {err}'


def execute_query(query: str):
    """
    :param query:
    :return:
    """
    try:
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        return record
    except Error as err:
        return f'Something went wrong: {err}'
    except Exception as e:
        return f'Something went wrong: {e}'


def insert_query(query: str, values: tuple):
    """
    :param query:
    :param values:
    :return:
    """
    try:
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        return False, 'success'
    except Error as err:
        return True, f'Something went wrong: {err}'


# get columns database to ignore indexes
def record_dictionary(record, table: str):
    """
    :param record:
    :param table:
    :return:
    """
    if table == 'users':
        return {'username': record[0], 'chat_id': record[1],
                'roll': record[2], 'phone': record[3], 'email': record[4], 'signup_time': record[5], 'last_login': record[6],
                'is_online': record[7], 'is_use_freemium': record[8], 'valid_time_plan': record[9],
                'plan_id': record[10], 'timeframe_id': record[11]}

    elif table == 'analysis':
        return {'id': record[0], 'name': record[1], 'description': record[2]}

    elif table == 'analysis_settings':
        return {'coin_id': record[0], 'timeframe_id': record[1], 'analysis_id': record[2],
                'indicator_settings_id': record[3], 'settings': record[4]}

    elif table == 'coins':
        return {'id': record[0], 'coin': record[1]}

    elif table == 'exchanges':
        return {'id': record[0], 'exchange': record[1]}

    elif table == 'indicators':
        return {'id': record[0], 'indicator': record[1]}

    elif table == 'indicator_settings':
        return {'id': record[0], 'indicator_id': record[1], 'settings': record[2]}

    elif table == 'plans':
        return {'id': record[0], 'plan': record[1], 'cost': record[2], 'duration': record[3], 'description': record[4],
                'coin_number': record[5], 'account_number': record[6], 'analysis_number': record[7]}

    elif table == 'recommendations':
        return {'id': record[0], 'analysis_id': record[1], 'coin_id': record[2], 'timeframe_id': record[3],
                'position': record[4], 'price': record[5], 'risk': record[6], 'timestamp': record[7]}

    elif table == 'timeframes':
        return {'id': record[0], 'timeframe': record[1]}

    elif table == 'transactions':
        return {'username': record[0], 'watchlist_id': record[1], 'recommendation_id_open': record[2],
                'recommendation_id_close': record[3], 'amount': record[4], 'is_open': record[5]}

    elif table == 'user_settings':
        return {'id': record[0], 'username': record[1], 'public': record[2], 'secret': record[3],
                'exchange_id': record[4]}

    elif table == 'watchlists':
        return {'id': record[0], 'coin_id': record[1], 'username': record[2], 'analysis_id': record[3],
                'amount': record[4]}

    elif table == 'plan_payments':
        return {'username': record[0], 'plan_id': record[1], 'timestamp': record[2], 'cost': record[3],
                'is_pay': record[4]}


# # hash passwords with salt use default salt for generate password use salt to define password already set db
# def hash_pass(password: str, salt: int = random.randrange(124, 92452, 2)):
#     """
#     :param password:
#     :param salt:
#     :return:
#     """
#     # salt is optional and default is random number (124-92452) - take non-optional when login
#     password = password + str(salt)
#     key = hashlib.sha512(password.encode('utf-8')).hexdigest()
#     return key, salt
#
#
# # check password format
# def chek_password(password: str, password2: str):
#     """
#     :param password:
#     :param password2:
#     :return:
#     """
#     if len(password) < 8:
#         result = False, "password is too short"
#     elif password != password2:
#         result = False, "passwords not match"
#     # elif not re.fullmatch("^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$", password):
#     # result = (False, "password must be content 0-9 digit and capital and lower char and include one of {@#$%^&+=} ")
#     else:
#         result = True, "Success"
#     return result


# check username exist
def check_username_exist(username: str):
    """
    :param username:
    :return:
    """
    query = "SELECT username from users WHERE username='{username}' LIMIT 1".format(username=username)
    record = execute_query(query=query)
    if record:
        return True
    else:
        return False


def get_duration_plan(plan_id: int):
    """
    :param plan_id:
    :return:
    """
    query = "SELECT duration from plans WHERE id='{plan_id}' LIMIT 1".format(plan_id=plan_id)
    record = execute_query(query=query)
    return record[0][0]


# get user row with chat_id
def get_user(chat_id: str):
    """
    :param chat_id:
    :return:
    """
    query = "SELECT * from users WHERE chat_id='{chat_id}'".format(chat_id=chat_id)
    record = execute_query(query=query)
    if record:
        return record
    else:
        return False


# check expire plan
def check_expire_plan(chat_id: str):
    """
    :param chat_id:
    :return:
    """
    user = record_dictionary(record=get_user(chat_id=chat_id)[0], table='users')
    now_time = datetime.now()
    if now_time <= user['valid_time_plan']:
        return False
    else:
        return True


def update_user_online(username: str, online: bool):
    """
    :param username:
    :param online:
    :return:
    """
    if online:
        now_time = datetime.now()
        query = "UPDATE users SET last_login='{now_time}' WHERE username='{username}'".format(now_time=now_time,
                                                                                              username=username)
        update_query(query)
    online = 1 if online else 0
    query = "UPDATE users SET is_online={online} WHERE username='{username}'".format(online=online, username=username)
    update_query(query)


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




# get functions
def get_coins(coin_id: int = -1):
    """
    :param coin_id: coin_id in already set in database
    :return: all coins if coin_id equal -1
    :return: coin name if coin_id
    :rtype: List of coins
    """
    if coin_id < 0:
        query = 'SELECT * from coins'
    else:
        query = "SELECT coin from coins WHERE id={coin_id}".format(coin_id=coin_id)
    return execute_query(query=query)


def get_timeframes(timeframe_id: int = -1):
    """
    :param timeframe_id: coin_id in already set in database
    :return: all timeframes if timeframe_id equal -1
    :return: timeframe name if timeframe_id
    :rtype: List of timeframes
    """
    if timeframe_id < 0:
        query = 'SELECT * from timeframes'
    else:
        query = "SELECT timeframe from timeframes WHERE id={timeframe_id}".format(timeframe_id=timeframe_id)
    return execute_query(query=query)


def get_analysis(analysis_id: int = -1):
    """
    :param analysis_id: analysis in already set in database
    :return: all analysis if analysis_id equal -1
    :return: analysis name if analysis_id
    :rtype: List of analysis
    """
    if analysis_id < 0:
        query = "SELECT * from analysis"
    else:
        query = "SELECT * from analysis WHERE id={analysis_id}".format(analysis_id=analysis_id)
    return execute_query(query=query)


def get_coin_name(coin_id: int):
    query = "SELECT coin FROM coins WHERE id={coin_id}".format(coin_id=coin_id)
    return execute_query(query=query)


def get_plans(plan_id: int = -1):
    """
    :param plan_id: plans in already set in database
    :return: all plans if plan_id equal -1
    :return: plans name if plan_id
    :rtype: List of plans
    """
    if plan_id < 0:
        query = "SELECT * from plans"
    else:
        query = "SELECT * from plans WHERE id={plan_id}".format(plan_id=plan_id)
    return execute_query(query=query)


# get last signal inserted in database
def get_recommendations(analysis_id: int = None, timeframe_id: int = None, coin_id: int = None):
    try:
        if analysis_id and timeframe_id and coin_id:
            sql = "SELECT * FROM recommendations WHERE coin_id={coin_id} AND  analysis_id={analysis_id} AND " \
                  "timeframe_id={timeframe_id} order by timestmp DESC LIMIT 1".format(coin_id=coin_id,
                                                                                      analysis_id=analysis_id,
                                                                                      timeframe_id=timeframe_id)
        elif timeframe_id is None and analysis_id and coin_id:
            sql = "SELECT * FROM recommendations WHERE coin_id={coin_id} AND  analysis_id={analysis_id}" \
                  " order by timestmp DESC LIMIT 1".format(coin_id=coin_id, analysis_id=analysis_id)
        elif timeframe_id is None and coin_id is None and analysis_id is None:
            sql = "SELECT * FROM recommendations order by timestmp DESC LIMIT 1"
        else:
            return None
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        record = cursor.fetchall()
        return record
    except Error as err:
        print("Something went wrong: {}".format(err))
        return None


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



def get_user_recommendation(coin_id: int = None, analysis_id: int = None):
    try:
        if coin_id and analysis_id:
            query = "SELECT watchlist.user , watchlist.coin_id ," \
                    "user_analysis.analysis_id  FROM watchlist INNER JOIN user_analysis " \
                    "ON watchlist.user = user_analysis.user " \
                    "WHERE coin_id ={coin_id} AND analysis_id={analysis_id} ".format(coin_id=coin_id,
                                                                                     analysis_id=analysis_id)
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


def get_indicators_setting_with_indicator_id(indicator_id: int):
    try:
        query = "SELECT settings, id from indicators_settings WHERE indicator_id = {indicator_id}".format(
            indicator_id=indicator_id)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        if record:
            return record
        else:
            return None
    except Error as err:
        return "Something went wrong: {}".format(err)


def update_indicator_setting_with_id(indicator_setting_id: int, settings: str):
    try:
        sql = "UPDATE indicators_settings SET settings ='{settings}' WHERE " \
              "id={indicator_setting_id} LIMIT 1".format(indicator_setting_id=indicator_setting_id, settings=settings)
        connection = con_db()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except Error as err:
        return "Something went wrong: {}".format(err)


def add_new_settings_to_indicator_setting(indicator_id: int, additional_setting: str):
    settings = get_indicators_setting_with_indicator_id(indicator_id)
    for setting in settings:
        update_indicator_setting_with_id(indicator_setting_id=int(setting[1]), settings=setting[0] + additional_setting)
