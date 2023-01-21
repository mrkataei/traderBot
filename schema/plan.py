from typing import Optional
from pydantic import BaseModel

# Shared properties
class PlanBase(BaseModel):
    name: str
    cost: str
    duration: int = 30
    sterategy_number: int = 1
    account_number: int = 1
    description : Optional[str] = None



# Properties to receive via API on creation
class PlanCreate(PlanBase):
    pass

# Properties to receive via API on update
class PlanUpdate(PlanBase):
    description : Optional[str] = None
    sterategy_number: int = 1
    account_number: int = 1
