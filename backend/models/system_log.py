from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, String, Text, func

from backend.database.base import Base


class SystemLog(Base):
    """Application and security events for observability and audit logs."""

    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True, server_default=func.now())
    service = Column(String(60), nullable=False, index=True)
    level = Column(String(20), nullable=False, index=True)
    message = Column(Text, nullable=False)
    correlation_id = Column(String(64), index=True, nullable=True)
