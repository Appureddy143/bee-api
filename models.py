from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import datetime
from .database import Base
import enum

class UserRole(str, enum.Enum):
    FARMER = "farmer"
    BEEKEEPER = "beekeeper"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    role = Column(String) # 'farmer' or 'beekeeper'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    farms = relationship("Farm", back_populates="owner")
    hives = relationship("Hive", back_populates="owner")

class Farm(Base):
    __tablename__ = "farms"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    size_acres = Column(Float)

    owner = relationship("User", back_populates="farms")
    spray_alerts = relationship("SprayAlert", back_populates="farm")

class Hive(Base):
    __tablename__ = "hives"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    health_score = Column(Float, default=100.0)

    owner = relationship("User", back_populates="hives")
    health_logs = relationship("BeeHealthLog", back_populates="hive")

class SprayAlert(Base):
    __tablename__ = "spray_alerts"
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    pesticide_type = Column(String)
    scheduled_time = Column(DateTime)
    radius_km = Column(Float, default=5.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    farm = relationship("Farm", back_populates="spray_alerts")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    message = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class BeeHealthLog(Base):
    __tablename__ = "bee_health_logs"
    id = Column(Integer, primary_key=True, index=True)
    hive_id = Column(Integer, ForeignKey("hives.id"))
    temperature = Column(Float)
    humidity = Column(Float)
    honey_production_kg = Column(Float, default=0.0)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)

    hive = relationship("Hive", back_populates="health_logs")

class SosRequest(Base):
    __tablename__ = "sos_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    latitude = Column(Float)
    longitude = Column(Float)
    details = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AiChatHistory(Base):
    __tablename__ = "ai_chat_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    prompt = Column(String)
    response = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
