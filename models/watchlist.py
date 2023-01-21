from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func

from db.base_class import Base

class Watchlist(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(15), ForeignKey("user.username"))
    asset = Column(String(15), index=True)
    name = Column(String(15), index=True)
    exchange = Column(String(15), index=True)
    public_key = Column(String(60), nullable=False)
    secrete_key = Column(String(60), nullable=False)
    strategy_id = Column(Integer, ForeignKey("strategy.id"))
    created =Column(DateTime(timezone=True), server_default=func.now())