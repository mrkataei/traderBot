from sqlalchemy.orm import Session

from crud.plan import plan
from schema.plan import PlanCreate
from crud.user import user as curdUser
from schema.user import UserCreate

FIRST_SUPERUSER = 'kourosh'
FIRST_SUPERUSER_PASSWORD = 'admin'

def init_db(db: Session) -> None:
    user = curdUser.get_by_username(db=db, username=FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=FIRST_SUPERUSER,
            password=FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )

        user = crud.user.create(db, obj_in=user_in)

    plan.create(db=db, obj_in=PlanCreate(name='freemium', cost='0', duration=30, sterategy_number=1, account_number=1, description='free'))
