import importlib, inspect
from typing import List, Tuple
from exchanges.base import Exchange


def get_exchanges()-> List[Tuple[str, Exchange]]:
    exchanges =  inspect.getmembers(importlib.import_module("exchanges"), inspect.isclass)
    return exchanges

def get_exchange(exchange:str) -> Exchange:
    exchanges = get_exchanges()
    for name, cls in exchanges:
        if name == exchange:
            return cls
