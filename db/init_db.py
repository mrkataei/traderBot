from sqlalchemy.orm import Session

from app import crud, schemas


FIRST_SUPERUSER = ''
FIRST_SUPERUSER_PASSWORD = ''

def init_db(db: Session) -> None:
    user = crud.user.get_by_email(db, email=FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=FIRST_SUPERUSER,
            password=FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )

        user = crud.user.create(db, obj_in=user_in)


