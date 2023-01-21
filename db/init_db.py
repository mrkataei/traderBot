from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from crud.plan import plan as crudPlan
from schema.plan import PlanCreate
from crud.user import user as curdUser
from schema.user import UserCreate


FIRST_SUPERUSER = 'kourosh'
FIRST_SUPERUSER_PASSWORD = 'admin'
FIRST_SUPERUSER_CHAT_ID = '1210507821'
FIRST_SUPERUSER_PHONE = '+98903692842'

def init_db(db: Session) -> None:
    try:
        freemium = crudPlan.get_by_name(db=db, name='freemium')
        if not freemium:
            crudPlan.create(db=db, obj_in=PlanCreate(name='freemium', cost='0',
                    duration=30, sterategy_number=1, account_number=1, description='free'))
        user = curdUser.get_by_username(db=db, username=FIRST_SUPERUSER)
        if not user:
            user_in = UserCreate(
                username=FIRST_SUPERUSER,
                password=FIRST_SUPERUSER_PASSWORD,
                chat_id=FIRST_SUPERUSER_CHAT_ID,
                phone=FIRST_SUPERUSER_PHONE,
                is_superuser=True,
            )

            user = curdUser.create(db, obj_in=user_in)
    except OperationalError as e:
        pass

