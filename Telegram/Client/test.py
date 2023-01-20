from crud.user import CRUDUser
from db.session import SessionLocal
from schema.user import UserCreate
session = SessionLocal()
c_user = UserCreate(username='dasfs', password='sdsd', chat_id='sdfdsf')

user = CRUDUser.create(db=session, obj_in=c_user)

