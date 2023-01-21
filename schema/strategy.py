from pydantic import BaseModel
from typing import Optional

# Shared properties
class SterategyBase(BaseModel):
    name: str
    description: str

# Properties to receive via API on creation
class SterategyCreate(SterategyBase):
    name: Optional[str] = 'startegy'

# Properties to receive via API on update
class SterategyUpdate(SterategyBase):
    description: str
    name: Optional[str]
