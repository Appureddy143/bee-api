from pydantic import BaseModel, EmailStr
from typing import List, Optional
import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

class FarmCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    size_acres: float

class FarmResponse(FarmCreate):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class HiveCreate(BaseModel):
    name: str
    latitude: float
    longitude: float

class HiveResponse(HiveCreate):
    id: int
    owner_id: int
    health_score: float

    class Config:
        from_attributes = True

class SprayAlertCreate(BaseModel):
    farm_id: int
    pesticide_type: str
    scheduled_time: datetime.datetime
    radius_km: float

class SprayAlertResponse(SprayAlertCreate):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class BeeHealthLogCreate(BaseModel):
    temperature: float
    humidity: float
    honey_production_kg: float

class BeeHealthLogResponse(BeeHealthLogCreate):
    id: int
    hive_id: int
    recorded_at: datetime.datetime

    class Config:
        from_attributes = True

class AiChatRequest(BaseModel):
    prompt: str

class AiChatResponse(BaseModel):
    response: str

class SosCreate(BaseModel):
    latitude: float
    longitude: float
    details: str

class SosResponse(SosCreate):
    id: int
    user_id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    is_read: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True
