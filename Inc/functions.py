""""
Mr.Kataei 8/7/2021
all functions about queries from database define here, for now
soon this file must be cluster and to be multiple files
"""

from mysql.connector import Error
from Inc.db import con_db
from datetime import datetime


# queries function : update , insert , delete , fetch
def update_and_delete_query(query: str):
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

    elif table == 'trade_history':
        return {'recom_id': record[0], 'user_setting': record[1], 'timestamp': record[2]}

    elif table == 'user_settings':
        return {'username': record[0], 'public': record[1], 'secret': record[2],
                'exchange_id': record[3]}

    elif table == 'watchlist':
        return {'id': record[0], 'user_setting_id': [1], 'coin_id': record[2], 'username': record[3],
                'analysis_id': record[4], 'amount': record[5], 'sell_amount': record[6]}

    elif table == 'plan_payments':
        return {'username': record[0], 'plan_id': record[1], 'timestamp': record[2], 'cost': record[3],
                'is_pay': record[4]}
    else:
        return None


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
    query = "SELECT username, chat_id, role, email, phone, signup_time, last_login, is_online," \
            " is_use_freemium, valid_time_plan, plan_id, timeframe from users " \
            "WHERE chat_id='{chat_id}'".format(chat_id=chat_id)
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
    query = "SELECT id, name from tutorials_category"
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
    query = "SELECT exchanges.exchange, user_settings.id, user_settings.exchange_id " \
            "from user_settings, users, exchanges " \
            "WHERE chat_id='{chat_id}' " \
            "and users.username = user_settings.username " \
            "and exchanges.id = user_settings.exchange_id".format(chat_id=chat_id)
    return execute_query(query=query)


def get_user_api(user_setting_id: int):
    """
    :param user_setting_id:
    :return: public and secret key
    """
    query = "SELECT public, secret FROM user_settings " \
            "WHERE id={user_setting_id}".format(user_setting_id=user_setting_id)
    return execute_query(query=query)[0]


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
        update_and_delete_query(query)
    online = 1 if online else 0
    query = "UPDATE users SET is_online={online} WHERE username='{username}'".format(online=online, username=username)
    update_and_delete_query(query)


def get_timeframes(timeframe_id: int = -1):
    """
    :param timeframe_id: coin_id in already set in database
    :return: all timeframes if timeframe_id equal -1
    :return: timeframe name if timeframe_id
    :rtype: List of timeframes
    """
    if timeframe_id < 0:
        query = 'SELECT id, timeframe from timeframes'
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
        query = "SELECT id, name, description from analysis"
    else:
        query = "SELECT id, name, description from analysis WHERE id={analysis_id}".format(analysis_id=analysis_id)
    return execute_query(query=query)


def get_plans(plan_id: int = -1):
    """
    :param plan_id: plans in already set in database
    :return: all plans if plan_id equal -1
    :return: plans name if plan_id
    :rtype: List of plans
    """
    if plan_id < 0:
        query = "SELECT id, plan, cost, duration, description, strategy_number, account_number from plans"
    else:
        query = "SELECT id, plan, cost, duration, description, strategy_number, account_number" \
                " from plans WHERE id={plan_id}".format(plan_id=plan_id)
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
        query = "SELECT id, exchange from exchanges"
    else:
        query = "SELECT id, exchange from exchanges WHERE id={exchange_id}".format(exchange_id=exchange_id)
    return execute_query(query=query)


def get_user_watchlist(username: str):
    """
    :param username:
    :return:
    """
    query = "SELECT id, user_setting_id, coin_id, username," \
            " analysis_id, amount, sell_amount from watchlist WHERE username='{username}'".format(username=username)
    return execute_query(query=query)


def get_user_strategy(coin_id: int = None, analysis_id: int = None):
    """
    :param coin_id:
    :param analysis_id:
    :return:
    """
    query = "SELECT watchlist.username, users.chat_id, coins.coin , analysis.name " \
            "FROM watchlist inner join users on watchlist.username = users.username " \
            "inner join coins on watchlist.coin_id = coins.id " \
            "inner join analysis on watchlist.analysis_id = analysis.id " \
            "where watchlist.coin_id = {coin_id} " \
            "and watchlist.analysis_id = {analysis_id}  " \
            "group by watchlist.username, users.chat_id, coins.coin, analysis.name".format(analysis_id=analysis_id,
                                                                                           coin_id=coin_id)

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
    query = "SELECT username, chat_id, role, email, phone, signup_time, last_login, is_online, is_use_freemium," \
            " valid_time_plan, plan_id, timeframe from users " \
            "WHERE role='admin' AND chat_id='{chat_id}'".format(chat_id=chat_id)
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
        query = "SELECT id, analysis_id, coin_id, timeframe_id, position, price, risk, timestamp " \
                "FROM recommendations WHERE coin_id={coin_id} AND  analysis_id={analysis_id}" \
                " order by timestamp DESC LIMIT 1".format(coin_id=coin_id, analysis_id=analysis_id)
    else:
        query = "SELECT id, analysis_id, coin_id, timeframe_id, position, price, risk, timestamp " \
                "FROM recommendations WHERE coin_id={coin_id} AND analysis_id={analysis_id} AND" \
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
        query = 'SELECT id, coin from coins'
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
    query = "SELECT coins.coin , analysis.name, watchlist.amount , exchanges.exchange, watchlist.id " \
            "FROM watchlist inner join users on watchlist.username = users.username " \
            "inner join user_settings ON watchlist.user_setting_id = user_settings.id " \
            "inner join coins on watchlist.coin_id = coins.id " \
            "inner join analysis on watchlist.analysis_id = analysis.id " \
            "inner join exchanges on user_settings.exchange_id = exchanges.id " \
            "where users.chat_id = '{chat_id}'".format(chat_id=chat_id)

    return execute_query(query=query)


def delete_strategy(strategy_id: int):
    query = "DELETE FROM watchlist WHERE id ={strategy_id}".format(strategy_id=strategy_id)
    update_and_delete_query(query=query)


def update_user_exchange(user_setting_id: int, exchange_id: int, public: str, secret: str):
    query = "UPDATE user_settings SET exchange_id='{exchange_id}', public='{public}', secret='{secret}' " \
            "WHERE id='{user_setting_id}'".format(exchange_id=exchange_id, public=public, secret=secret,
                                                  user_setting_id=user_setting_id)
    return update_and_delete_query(query)


def update_user_strategy(user_setting_id: int, coin_id: int, watchlist_id: int, analysis_id: int, amount: float):
    query = "UPDATE watchlist SET user_setting_id={user_setting_id}, coin_id={coin_id}, analysis_id={analysis_id}," \
            " amount={amount} WHERE id='{watchlist_id}'".format(user_setting_id=user_setting_id,
                                                                coin_id=coin_id, analysis_id=analysis_id,
                                                                amount=amount, watchlist_id=watchlist_id)
    return update_and_delete_query(query)


def get_user_trade_history(chat_id: str):
    query = "SELECT trade.timestamp, exchanges.exchange,  analysis.name, trade.coin, trade.price, trade.position," \
            " trade.order_status, trade.status, trade.amount," \
            " trade.order_submit_time, trade.signal_time from trade " \
            "inner join user_settings on trade.user_setting_id = user_settings.id " \
            "inner join users on user_settings.username = users.username " \
            "inner join analysis on trade.analysis_id = analysis.id " \
            "inner join exchanges on user_settings.exchange_id = exchanges.id " \
            "WHERE users.chat_id='{chat_id}' order by trade.timestamp DESC LIMIT 10".format(chat_id=chat_id)
    return execute_query(query=query)


def set_trade_history(user_setting_id: int, coin: str, analysis_id, position: str, status: str,
                      signal_time, price: float = None, order_status: str = None, amount: str = None,
                      order_submit_time: str = None):
    """
    :param user_setting_id:
    :param coin:
    :param analysis_id:
    :param price:
    :param position:
    :param order_status:
    :param status:
    :param amount:
    :param order_submit_time:
    :param signal_time:
    :return:
    """
    if order_submit_time and amount and order_status and price:
        query = "INSERT INTO trade (user_setting_id, coin, analysis_id, price, position, order_status, status," \
                " amount, order_submit_time, signal_time) VALUES (%s, %s , %s ,%s , %s, %s , %s ,%s , %s ,%s)"
        val = (user_setting_id, coin, analysis_id, price, position, order_status, status, amount, order_submit_time,
               signal_time)
    else:
        query = "INSERT INTO trade (user_setting_id, coin, analysis_id, position, status," \
                " signal_time) VALUES (%s, %s , %s ,%s , %s, %s)"
        val = (user_setting_id, coin, analysis_id, position, status, signal_time)
    error, result = insert_query(query=query, values=val)
    return error, result


def get_users_submit_order_detail(analysis_id: int, coin_id: int):
    """
    :param analysis_id:
    :param coin_id:
    :return:user_setting_id , public, secret, exchange_id, symbol, percent
    """
    query = "SELECT watchlist.user_setting_id, user_settings.public, user_settings.secret," \
            "user_settings.exchange_id, coins.coin, watchlist.amount, watchlist.sell_amount, watchlist.username," \
            "watchlist.coin_id" \
            " FROM watchlist " \
            "inner join user_settings on watchlist.user_setting_id = user_settings.id " \
            "inner join coins on watchlist.coin_id = coins.id " \
            "WHERE watchlist.coin_id={coin_id} and watchlist.analysis_id={analysis_id}".format(coin_id=coin_id,
                                                                                               analysis_id=analysis_id)
    return execute_query(query=query)


def update_sell_amount(user_setting_id: int, coin_id: int, username: str, analysis_id: int, sell_amount: float):
    query = "UPDATE watchlist SET sell_amount={sell_amount} WHERE username='{username}' " \
            "and user_setting_id ={user_setting_id} and coin_id={coin_id} " \
            "and analysis_id={analysis_id}".format(user_setting_id=user_setting_id, username=username,
                                                   sell_amount=sell_amount, coin_id=coin_id, analysis_id=analysis_id)
    update_and_delete_query(query)


def get_demo_account_assets(chat_id: str):
    query = "SELECT BTC, ETH, BCH, ETC, ADA, DOGE, USDT FROM demo_account, users " \
            "WHERE users.username=demo_account.username and users.chat_id='{chat_id}'".format(chat_id=chat_id)
    return execute_query(query=query)


def create_demo_account(username: str):
    query = "INSERT INTO demo_account (username) VALUES (%s)"
    val = (username,)
    error, result = insert_query(query=query, values=val)
    return error, result


def get_users_validation_date():
    query = "SELECT username, valid_time_plan, chat_id FROM users WHERE is_valid=1 "
    return execute_query(query=query)


def delete_all_user_strategies(username: str):
    query = "DELETE FROM watchlist WHERE username ='{username}'".format(username=username)
    update_and_delete_query(query=query)


def set_is_valid_user(username: str, is_valid: bool = False):
    is_valid = 1 if is_valid else 0
    query = "UPDATE users SET is_valid={is_valid} WHERE username='{username}'".format(is_valid=is_valid,
                                                                                      username=username)
    return update_and_delete_query(query)
