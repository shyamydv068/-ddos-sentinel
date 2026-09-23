from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, String, Float, Text, Boolean, func

from backend.database.base import Base


class TrafficEvent(Base):
    """Represents a network traffic event ingested from Kafka or synthetic generation."""

    __tablename__ = "traffic_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String(64), unique=True, index=True, nullable=False)
    correlation_id = Column(String(64), index=True, nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True, server_default=func.now())
    source_ip = Column(String(45), index=True, nullable=False)
    destination_ip = Column(String(45), index=True, nullable=False)
    source_port = Column(Integer, nullable=True)
    destination_port = Column(Integer, nullable=True)
    protocol = Column(String(20), index=True, nullable=False)
    packet_count = Column(Integer, nullable=False, default=0)
    byte_count = Column(Integer, nullable=False, default=0)
    flow_duration = Column(Float, nullable=True)
    packets_per_second = Column(Float, nullable=True)
    bytes_per_second = Column(Float, nullable=True)
    active_connections = Column(Integer, nullable=True, default=0)
    unique_source_ips = Column(Integer, nullable=True, default=0)
    raw_payload = Column(Text, nullable=True)
    is_attack = Column(Boolean, default=False, nullable=False)
