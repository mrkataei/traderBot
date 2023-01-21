from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from crud.plan import plan as crudPlan
from models.user import User
from schema.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_chat_id(self, db: Session, *, chat_id: str) -> Optional[User]:
        return db.query(User).filter(User.chat_id == chat_id).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def check_expire(self, db: Session, *, chat_id: str) -> bool:
        user = db.query(User).filter(User.chat_id == chat_id).first()
        now_time = datetime.now()
        if now_time <= user.valid_time_plan:
            return True
        else:
            return False

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        freemium = crudPlan.get_by_name(db=db, name='freemium')
        db_obj = User(
            username= obj_in.username,
            password= get_password_hash(obj_in.password),
            phone= obj_in.phone,
            chat_id = obj_in.chat_id,
            is_superuser = obj_in.is_superuser,
            plan_id = freemium.id,
            valid_time_plan = datetime.now() + timedelta(days=freemium.duration)
            )
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
