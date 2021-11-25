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
                'role': record[2], 'email': record[3], 'phone': record[4], 'signup_time': record[5],
                'last_login': record[6], 'is_online': record[7], 'is_use_freemium': record[8],
                'valid_time_plan': record[9], 'plan_id': record[10], 'timeframe_id': record[11]}

    elif table == 'analysis':
        return {'id': record[0], 'name': record[1], 'description': record[2]}

    elif table == 'coins':
        return {'id': record[0], 'coin': record[1]}

    elif table == 'exchanges':
        return {'id': record[0], 'exchange': record[1]}

    elif table == 'plans':
        return {'id': record[0], 'plan': record[1], 'cost': record[2], 'duration': record[3], 'description': record[4],
                'strategy_number': record[5], 'account_number': record[6]}

    elif table == 'recommendations':
        return {'id': record[0], 'analysis_id': record[1], 'coin_id': record[2], 'timeframe_id': record[3],
                'position': record[4], 'price': record[5], 'risk': record[6], 'timestamp': record[7]}

    elif table == 'timeframes':
        return {'id': record[0], 'timeframe': record[1]}

    elif table == 'transactions':
        return {'username': record[0], 'watchlist_id': record[1], 'recommendation_id_open': record[2],
                'recommendation_id_close': record[3], 'amount': record[4], 'is_open': record[5]}

    elif table == 'user_settings':
        return {'username': record[0], 'public': record[1], 'secret': record[2],
                'exchange_id': record[3]}

    elif table == 'watchlist':
        return {'id': record[0], 'user_setting_id': [1], 'coin_id': record[2], 'username': record[3],
                'analysis_id': record[4], 'amount': record[5]}

    elif table == 'plan_payments':
        return {'username': record[0], 'plan_id': record[1], 'timestamp': record[2], 'cost': record[3],
                'is_pay': record[4]}


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


def is_user_signup(chat_id: str):
    """
    :param chat_id:
    :return:
    """
    if not get_user(chat_id=chat_id):
        return True
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


def get_tutorials_categories():
    """
    :return:
    """
    query = "SELECT * from tutorials_category"
    return execute_query(query=query)


def get_tutorials_with_category(category: str):
    """
    :param category:
    :return:
    """
    query = "SELECT tutorials.name, tutorials.media from tutorials, tutorials_category " \
            "where tutorials_category.name='{category}' " \
            "and tutorials.category = tutorials_category.id".format(category=category)
    return execute_query(query=query)


def get_user_plan(username: str):
    """
    :param username:
    :return:
    """
    query = "SELECT plan_id from users WHERE username='{username}'".format(username=username)
    record = execute_query(query=query)
    if record:
        return record[0][0]
    else:
        return False


def get_user_exchange(chat_id: str):
    """
    :param chat_id:
    :return:
    """
    query = "SELECT exchanges.exchange from user_settings, users, exchanges WHERE chat_id='{chat_id}' " \
            "and users.username = user_settings.username " \
            "and exchanges.id = user_settings.exchange_id".format(chat_id=chat_id)
    return execute_query(query=query)


def get_user_settings_id(chat_id: str, exchange_id: int):
    """
    :param chat_id:
    :param exchange_id:
    :return:
    """
    query = "SELECT user_settings.id FROM users, user_settings, exchanges " \
            "WHERE users.username = user_settings.username and exchanges.id = user_settings.exchange_id " \
            "and users.chat_id = '{chat_id}' " \
            "and user_settings.exchange_id = {exchange_id}".format(chat_id=chat_id, exchange_id=exchange_id)
    return execute_query(query=query)


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


def set_user_setting(username: str, public: str, secret: str, exchange_id: int):
    """
    :param username:
    :param public:
    :param secret:
    :param exchange_id:
    :return:
    """
    query = "INSERT INTO user_settings (username, public, secret, exchange_id) VALUES (%s, %s , %s ,%s)"
    val = (username, public, secret, exchange_id)
    error, result = insert_query(query=query, values=val)
    return error, result


def get_user_exchanges(chat_id: str):
    """
    :param chat_id:
    :return:
    """
    query = "SELECT exchanges.exchange FROM users, user_settings, exchanges " \
            "WHERE users.username = user_settings.username and exchanges.id = user_settings.exchange_id " \
            "and users.chat_id = '{chat_id}'".format(chat_id=chat_id)
    return execute_query(query=query)


def set_watchlist(user_setting_id: int, coin_id: int, username: str, analysis_id: int, amount: float):
    """
    :param user_setting_id:
    :param coin_id:
    :param username:
    :param analysis_id:
    :param amount:
    :return:
    """
    query = "INSERT INTO watchlist(user_setting_id, coin_id, username, analysis_id, amount) " \
            "VALUES (%s, %s, %s , %s ,%s)"
    val = (user_setting_id, coin_id, username, analysis_id, amount)
    error, result = insert_query(query=query, values=val)
    return error, result


def get_exchanges(exchange_id: int = -1):
    """
    :param exchange_id:
    :return:
    """
    if exchange_id < 0:
        query = "SELECT * from exchanges"
    else:
        query = "SELECT * from exchanges WHERE id={exchange_id}".format(exchange_id=exchange_id)
    return execute_query(query=query)


def get_user_watchlist(username: str):
    """
    :param username:
    :return:
    """
    query = "SELECT * from watchlist WHERE username='{username}'".format(username=username)
    return execute_query(query=query)


def get_user_strategy(coin_id: int = None, analysis_id: int = None):
    """
    :param coin_id:
    :param analysis_id:
    :return:
    """
    query = "SELECT username FROM watchlist WHERE coin_id ={coin_id}" \
            " AND analysis_id={analysis_id}".format(coin_id=coin_id,
                                                    analysis_id=analysis_id)
    return execute_query(query=query)


def get_chat_ids(username: str = None):
    """
    :param username:
    :return:
    """
    if username is None:
        query = "SELECT chat_id from users"
        return execute_query(query=query)
    else:
        query = "SELECT chat_id FROM users WHERE username ='{username}'".format(username=username)
        return execute_query(query=query)[0][0]


def is_admin(chat_id: str):
    """
    :param chat_id:
    :return:
    """
    query = "SELECT * from users WHERE role='admin' AND chat_id='{chat_id}'".format(chat_id=chat_id)
    if execute_query(query=query):
        return True
    else:
        return False


def get_usernames():
    """
    :return:
    """
    query = "SELECT username from users"
    return execute_query(query=query)


def set_recommendation(analysis_id: int, coin_id: int, timeframe_id: int, position: str, price: float, risk: str):
    """
    :param analysis_id:
    :param coin_id:
    :param timeframe_id:
    :param position:
    :param price:
    :param risk:
    :return:
    """
    query = "INSERT INTO recommendations (analysis_id, coin_id, timeframe_id, position, price, risk) " \
            "VALUES (%s, %s , %s ,%s, %s , %s )"
    val = (analysis_id, coin_id, timeframe_id, position, price, risk)
    return insert_query(query=query, values=val)


def get_last_recommendations(analysis_id: int, coin_id: int, timeframe_id: int = None):
    """
    :param analysis_id:
    :param coin_id:
    :param timeframe_id:
    :return:
    """
    if timeframe_id is None:
        query = "SELECT * FROM recommendations WHERE coin_id={coin_id} AND  analysis_id={analysis_id}" \
                " order by timestamp DESC LIMIT 1".format(coin_id=coin_id, analysis_id=analysis_id)
    else:
        query = "SELECT * FROM recommendations WHERE coin_id={coin_id} AND analysis_id={analysis_id} AND" \
                " timeframe_id={timeframe_id} order by timestamp DESC LIMIT 1".format(coin_id=coin_id,
                                                                                      analysis_id=analysis_id,
                                                                                      timeframe_id=timeframe_id)
    return execute_query(query=query)


# coin queries

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


def get_coin_id(coin: str):
    """
    :param coin:
    :return:
    """
    query = "SELECT id from coins WHERE coin='{coin}'".format(coin=coin)
    return execute_query(query=query)[0][0]


def get_coin_name(coin_id: int):
    """
    :param coin_id:
    :return:
    """
    query = "SELECT coin FROM coins WHERE id={coin_id}".format(coin_id=coin_id)
    return execute_query(query=query)


def get_user_plan_profile(chat_id: str):
    query = "SELECT plans.plan, users.valid_time_plan from users, plans " \
            "where users.plan_id = plans.id and users.chat_id = '{chat_id}'".format(chat_id=chat_id)
    plan, valid_date = execute_query(query=query)[0]
    return plan, valid_date.strftime("%Y-%m-%d %H:%M:%S")


def get_user_exchanges_strategies_profile(chat_id: str):
    """
    :param chat_id:
    :return:
    """
    query = "SELECT coins.coin , analysis.name, watchlist.amount , exchanges.exchange " \
            "FROM watchlist inner join users on watchlist.username = users.username " \
            "inner join user_settings ON watchlist.user_setting_id = user_settings.id " \
            "inner join coins on watchlist.coin_id = coins.id " \
            "inner join analysis on watchlist.analysis_id = analysis.id " \
            "inner join exchanges on user_settings.exchange_id = exchanges.id " \
            "where users.chat_id = '{chat_id}'".format(chat_id=chat_id)

    return execute_query(query=query)

