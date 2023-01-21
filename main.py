# from Analysis.stream import StrategiesThreads
# from time import sleep

# thread = StrategiesThreads('BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOGEUSDT', 'BCHUSDT', 'ETCUSDT')

# if __name__ == '__main__':
#     thread.start_threads()
#     while True:
#         print("Running...")
#         sleep(2000000)
from db.session import SessionLocal

from db.init_db import init_db

session = SessionLocal()

init_db(db=session)