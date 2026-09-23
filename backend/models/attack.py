from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, String, Float, Text, Boolean, func

from backend.database.base import Base


class AttackEvent(Base):
    """Represents a detected or suspicious attack event with model output."""

    __tablename__ = "attack_events"

    id = Column(Integer, primary_key=True, index=True)
    attack_id = Column(String(64), unique=True, index=True, nullable=False)
    event_id = Column(String(64), index=True, nullable=False)
    correlation_id = Column(String(64), index=True, nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True, server_default=func.now())
    source_ip = Column(String(45), index=True, nullable=False)
    destination_ip = Column(String(45), index=True, nullable=False)
    attack_type = Column(String(50), index=True, nullable=False)
    prediction = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False, default=0.0)
    risk_score = Column(Integer, nullable=False, default=0)
    severity = Column(String(20), nullable=False)
    model_version = Column(String(50), nullable=False)
    action = Column(String(50), nullable=True)
    status = Column(String(30), default="open", nullable=False)
    details = Column(Text, nullable=True)
