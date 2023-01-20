from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.base_class import Base

class Plan(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(15), index=True)
    cost = Column(String(15), index=True)
    duration = Column(Integer, index=True)
    sterategy_number =  Column(Integer, index=True)
    account_number =  Column(Integer, index=True)
    description = Column(Text, index=True)