from crud.base import CRUDBase
from crud.sterategy import strategy as crudStrategy
from models.watchlist import Watchlist
from schema.watchlist import WatchlistCreate, WatchlistUpdate
from sqlalchemy.orm import Session
from typing import List, Dict, Union, Any

class CRUDWatchlist(CRUDBase[Watchlist, WatchlistCreate, WatchlistUpdate]):
    def create(self, db: Session, *, obj_in: WatchlistCreate) -> Watchlist:
        return super().create(db, obj_in=obj_in)
    
    def get_by_chat_id(self, db: Session, *, chat_id: str) -> List[Watchlist]:
        return db.query(Watchlist).filter(Watchlist.chat_id == chat_id)

watchlist = CRUDWatchlist(Watchlist)