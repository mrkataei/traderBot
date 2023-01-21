# from Analysis.stream import StrategiesThreads
# from time import sleep

# thread = StrategiesThreads('BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOGEUSDT', 'BCHUSDT', 'ETCUSDT')

# if __name__ == '__main__':
#     thread.start_threads()
#     while True:
#         print("Running...")
#         sleep(2000000)

import pkgutil
import importlib
import inspect


# print(base.)
# packages = pkgutil.walk_packages(['./exchanges/'])
# for pack in packages:
#     print(pack.name)

# print(importlib.import_module('models'))
import importlib, inspect
exchanges =  inspect.getmembers(importlib.import_module("exchanges"), inspect.isclass)
print(exchanges[0][1](public='',secret='').symbols)
for name, cls in inspect.getmembers(importlib.import_module("exchanges"), inspect.isclass):
    print(cls)