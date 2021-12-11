"""
    Mr.Kataei 11/12/2021
    need risk profile for users - this work just for Aran account
"""

from Inc import functions
from Account.clients import BitfinexClient

symbols_bitfinix = {'BTCUSDT': 'tBTCUSD', 'ETHUSDT': 'tETHUSD', 'ADAUSDT': 'tADAUSD', 'DOGEUSDT': 'tDOGE:USD',
                    'BCHUSDT': 'tBCHN:USD', 'ETCUSDT': 'tETCUSD'}


def get_exchange_class(exchange_id: int, public: str, secret: str):
    if exchange_id == 1:
        return BitfinexClient(public=public, secret=secret)
    else:
        return None


def submit_order(coin_id: int, analysis_id: int, time_receive_signal, position: str):
    orders = functions.get_users_submit_order_detail(analysis_id=analysis_id, coin_id=coin_id)
    print(orders)
    for order in orders:
        client = get_exchange_class(exchange_id=order[3], public=order[1], secret=order[2])
        print(client)
        if position == 'buy':
            result = client.buy_market(symbol=symbols_bitfinix[order[4]], percent=order[5])
            if result is not None:
                order_detail = result[4][0]
                functions.set_trade_history(user_setting_id=order[0], coin=order[4], analysis_id=analysis_id,
                                            position='buy', signal_time=time_receive_signal, price=order_detail[14],
                                            amount=order_detail[7], order_status=order_detail[13],
                                            order_submit_time=order_detail[4], status=result[4][2])
            else:
                print(functions.set_trade_history(user_setting_id=order[0], coin=order[4], analysis_id=analysis_id,
                                                  position='buy', signal_time=time_receive_signal, status='failed'))
        else:
            result = client.sell_market(symbol=symbols_bitfinix[order[4]], amount=order[5])
            if result is not None:
                order_detail = result[4][0]
                functions.set_trade_history(user_setting_id=order[0], coin=order[4], analysis_id=analysis_id,
                                            position='sell', signal_time=time_receive_signal, price=order_detail[14],
                                            amount=order_detail[7], order_status=order_detail[13],
                                            order_submit_time=order_detail[4], status=result[4][2])
            else:
                functions.set_trade_history(user_setting_id=order[0], coin=order[4], analysis_id=analysis_id,
                                            position='sell', signal_time=time_receive_signal, status='failed')
