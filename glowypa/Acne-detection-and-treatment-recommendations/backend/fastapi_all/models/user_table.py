from pydantic import BaseModel, constr, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[constr(strip_whitespace=True, min_length=1)] = None

class UserTable(BaseModel):
    first_name: Optional[constr(strip_whitespace=True, min_length=1)] = None
    last_name: Optional[constr(strip_whitespace=True, min_length=1)] = None
    birth_date: Optional[str] = None
    skin_type: Optional[constr(strip_whitespace=True, min_length=1)] = None
    location: Optional[constr(strip_whitespace=True, min_length=1)] = None
    email: Optional[EmailStr] = None
    gender: Optional[str] = None
    password: Optional[constr(strip_whitespace=True, min_length=1)] = None

class UserUpdateRequest(BaseModel):
    user_id: constr(strip_whitespace=True, min_length=1)
    first_name: Optional[constr(strip_whitespace=True, min_length=1)] = None
    last_name: Optional[constr(strip_whitespace=True, min_length=1)] = None
    birth_date: Optional[str] = None
    skin_type: Optional[constr(strip_whitespace=True, min_length=1)] = None
    location: Optional[constr(strip_whitespace=True, min_length=1)] = None
    email: Optional[EmailStr] = None
    gender: Optional[str] = None
    password: Optional[constr(strip_whitespace=True, min_length=1)] = None
