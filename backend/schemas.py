from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime


# ---------- Auth ----------

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "industrialist"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Mines ----------

class MineCreate(BaseModel):
    name: str
    location_name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class MineOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    location_name: str
    latitude: Optional[float]
    longitude: Optional[float]


# ---------- Exploration ----------

class AnalysisRequest(BaseModel):
    location: str
    buffer_degrees: float = 0.01
    grid_rows: int = 10
    grid_cols: int = 10
    mine_id: Optional[int] = None  # if provided, result is saved against this mine


# ---------- Production ----------

class TargetIn(BaseModel):
    month: str  # "2026-01"
    target_tonnes: float
