from typing import Optional

from pydantic import BaseModel, EmailStr

# Shared properties
class RecommendationBase(BaseModel):
    asset: str
    timeframe: str
    open: float
    close: float
    high: float
    low: float
    signl: bool = True

# Properties to receive via API on creation
class RecommendationCreate(RecommendationBase):
    signal: bool
    sterategy_id: int

# Properties to receive via API on update
class RecommendationUpdate(RecommendationBase):
    pass
