from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, String, Float, Text, Boolean, func

from backend.database.base import Base


class BlockedIP(Base):
    """Represents an IP that has been blocked or flagged for mitigation."""

    __tablename__ = "blocked_ips"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(45), unique=True, index=True, nullable=False)
    first_detected = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_detected = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    attack_count = Column(Integer, nullable=False, default=0)
    risk_score = Column(Integer, nullable=False, default=0)
    status = Column(String(20), default="blocked", nullable=False)
    reason = Column(Text, nullable=True)
    action = Column(String(30), default="BLOCK_IP", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
