# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    api_key = Column(String, unique=True, nullable=False, index=True)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    api_key = Column(String, ForeignKey("sites.api_key"), nullable=False, index=True)
    event_type = Column(String, nullable=False, index=True)
    page = Column(String, nullable=False)
    properties = Column(JSONB, nullable=False, server_default="{}")
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)