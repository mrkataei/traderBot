from bfxapi import Client, Order


class Spot:
    def __init__(self, API_KEY: str, API_SECRET: str):
        self.client = Client(api_key=API_KEY, api_secret=API_SECRET)

    def create_order(self, symbol: str, price: float, amount: float, quantity: float):
        symbol = ''
        self.client.rest.submit_order(symbol=symbol, price=price, amount=amount, market_type=Order.Type.MARKET,
                                      hidden=False, price_trailing=None, price_aux_limit=None, oco_stop_price=None,
                                      close=False, reduce_only=False, post_only=False, oco=False, aff_code=None,
                                      time_in_force=None, leverage=None, gid=None)
        """
            :param symbol: required
            :type symbol: str
            :param side: required
            :type side: str
            :param type: required
            :type type: str
            :param timeInForce: required if limit order
            :type timeInForce: str
            :param quantity: required
            :type quantity: decimal
            :param quoteOrderQty: amount the user wants to spend (when buying) or receive (when selling)
                of the quote asset, applicable to MARKET orders
            :type quoteOrderQty: decimal
            :param price: required
            :type price: str
            :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
            :type newClientOrderId: str
            :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
            :type icebergQty: decimal
            :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
            :type newOrderRespType: str
            :param recvWindow: the number of milliseconds the request is valid for
            :type recvWindow: int
            :returns: API response

        """
        self.client.create_order()
