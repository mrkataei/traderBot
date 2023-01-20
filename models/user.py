from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.base_class import Base

class User(Base):
    username = Column(String(15), primary_key=True, index=True)
    chat_id = Column(String(15), index=True)
    phone = Column(String(12), index=True)
    email = Column(String(30), unique=True, index=True, nullable=False)
    password = Column(String(60), nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    signup_date =Column(DateTime(timezone=True), server_default=func.now())
    is_use_freemium = Column(Boolean(), default=False)
    # valid_time_plan = Column(DateTime(timezone=True), default=None)
    # plan_id = relationship("Plan", back_populates="id")
    is_valid = Column(Boolean(), default=True)

