from crud.base import CRUDBase
from models.strategy import Strategy
from schema.strategy import SterategyCreate, SterategyUpdate
from sqlalchemy.orm import Session

class CRUDUser(CRUDBase[Strategy, SterategyCreate, SterategyUpdate]):
    def create(self, db: Session, *, obj_in: SterategyCreate) -> Strategy:
        return super().create(db, obj_in=obj_in)