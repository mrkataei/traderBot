from typing import Optional

from pydantic import BaseModel, EmailStr

# Shared properties
class UserBase(BaseModel):
    username: str
    chat_id: str
    is_active: Optional[bool] = True
    is_superuser: bool = False
    is_valid: bool = True

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    phone: str
    is_use_freemium: bool = True

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
