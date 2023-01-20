from sqlalchemy import Boolean, Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.base_class import Base

class User(Base):
    username = Column(String(15), primary_key=True, index=True)
    chat_id = Column(String(15), index=True, unique=True)
    phone = Column(String(12), index=True)
    password = Column(String(60), nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    signup_date =Column(DateTime(timezone=True), server_default=func.now())
    is_use_freemium = Column(Boolean(), default=False)
    valid_time_plan = Column(DateTime(timezone=True), default=None)
    plan_id = Column(Integer, ForeignKey("plan.id"))
    is_valid = Column(Boolean(), default=True)

