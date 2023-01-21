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
            sterategy_number=obj_in.sterategy_number,
            account_number=obj_in.account_number,
            description=obj_in.description
            )
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

plan = CRUDPlan(Plan)
