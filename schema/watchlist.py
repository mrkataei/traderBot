from pydantic import BaseModel
from typing import Optional

# Shared properties
class WatchlistBase(BaseModel):
    chat_id: str
    asset: str
    exchange: str
    public_key: str
    secrete_key: str
    strategy_id: int


# Properties to receive via API on creation
class WatchlistCreate(WatchlistBase):
    name: Optional[str] = 'watchlist'

# Properties to receive via API on update
class WatchlistUpdate(WatchlistBase):
    asset: str
    exchange: str
    public_key: str
    secrete_key: str
    name: Optional[str]
