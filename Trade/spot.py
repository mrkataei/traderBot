from Account.clients import BitfinexClient


def buy_market(client: BitfinexClient, symbol: str):
    if symbol == 'tETHUSD' or symbol == 'tADAUSD':
        amount = client.get_balance_available(symbol=symbol, direction=1)
        result = client.submit_market_order(symbol=symbol, amount=str(amount))
        return result
    else:
        return None


def sell_market(client: BitfinexClient, symbol: str):
    if symbol == 'tETHUSD' or symbol == 'tADAUSD':
        amount = client.get_balance_available(symbol=symbol, direction=-1)
        result = client.submit_market_order(symbol=symbol, amount=str(amount))
        return result
    else:
        return None
