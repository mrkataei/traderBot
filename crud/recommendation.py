from crud.base import CRUDBase
from models.recommendation import Recommendation
from schema.recommendation import RecommendationCreate, RecommendationUpdate
from sqlalchemy.orm import Session
from typing import List, Dict, Union, Any

class CRUDRecommendation(CRUDBase[Recommendation, RecommendationCreate, RecommendationUpdate]):
    def create(self, db: Session, *, obj_in: RecommendationCreate) -> Recommendation:
        return super().create(db, obj_in=obj_in)

    def get_last(self, db: Session, *, watchlist_id: id) -> Recommendation:
        return db.query(Recommendation).filter(Recommendation.watchlist_id == watchlist_id)

watchlist = CRUDRecommendation(Recommendation)