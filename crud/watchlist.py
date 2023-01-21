from crud.base import CRUDBase
from models.watchlist import Watchlist
from schema.watchlist import WatchlistCreate, WatchlistUpdate
from sqlalchemy.orm import Session

class CRUDUser(CRUDBase[Watchlist, WatchlistCreate, WatchlistUpdate]):
    def create(self, db: Session, *, obj_in: WatchlistCreate) -> Watchlist:
        return super().create(db, obj_in=obj_in)