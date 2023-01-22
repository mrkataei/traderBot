from sqlalchemy import Text, Column, String, Integer, DateTime
from sqlalchemy.sql import func

from db.base_class import Base

class Strategy(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(15), index=True)
    description = Column(Text, index=True)
    created =Column(DateTime(timezone=True), server_default=func.now())

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}