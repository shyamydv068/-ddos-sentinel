from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, String, Float, Text, func

from backend.database.base import Base


class Alert(Base):
    """Security alert generated for suspicious or malicious behavior."""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(64), unique=True, index=True, nullable=False)
    correlation_id = Column(String(64), index=True, nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True, server_default=func.now())
    source = Column(String(100), nullable=False)
    alert_type = Column(String(50), index=True, nullable=False)
    description = Column(Text, nullable=False)
    risk_score = Column(Integer, nullable=False, default=0)
    severity = Column(String(20), nullable=False)
    status = Column(String(30), default="open", nullable=False)
    action = Column(String(50), nullable=True)
