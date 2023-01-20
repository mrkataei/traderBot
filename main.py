# from Analysis.stream import StrategiesThreads
# from time import sleep

# thread = StrategiesThreads('BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOGEUSDT', 'BCHUSDT', 'ETCUSDT')

# if __name__ == '__main__':
#     thread.start_threads()
#     while True:
#         print("Running...")
#         sleep(2000000)
from crud.user import CRUDUser
from db.session import SessionLocal
from schema.user import UserCreate
from models.user import User
session = SessionLocal()
c_user = UserCreate(username='dasfs', password='sdsd', chat_id='sdfdsf', email='dsfdfs@dfdf.com', phone='0231513')

user = CRUDUser(model=User).create(db=session, obj_in=c_user)