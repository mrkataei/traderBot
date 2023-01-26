from sqlalchemy import Boolean, Column, String, DateTime, Integer, Float, ForeignKey
from sqlalchemy.sql import func

from db.base_class import Base

class Recommendation(Base):
    id = Column(Integer, primary_key=True, index=True)
    watchlist_id = Column(Integer, ForeignKey("watchlist.id"))
    asset = Column(String(12), index=True)
    timefarme = Column(String(12), index=True)
    # 1 buy 0 sell
    signal = Column(Boolean(), default=True) 
    created_at =Column(DateTime(timezone=True), server_default=func.now())
    high = Column(Float,  index=True)
    close = Column(Float,  index=True)
    low = Column(Float,  index=True)
    open = Column(Float,  index=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
