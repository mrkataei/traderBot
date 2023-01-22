from crud.base import CRUDBase
from models.plan import Plan
from schema.plan import PlanCreate, PlanUpdate
from sqlalchemy.orm import Session


class CRUDPlan(CRUDBase[Plan, PlanCreate, PlanUpdate]):
    def create(self, db: Session, *, obj_in: PlanCreate) -> Plan:
        db_obj = Plan(
            name=obj_in.name,
            cost=obj_in.cost,
            duration=obj_in.duration,
            watchlist_number=obj_in.watchlist_number,
            description=obj_in.description
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    def get_by_name(self, db: Session, *, name: str) -> Plan:
        return db.query(Plan).filter(Plan.name == name).first()

plan = CRUDPlan(Plan)
