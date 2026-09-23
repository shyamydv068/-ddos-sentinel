from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database.base import Base
from backend.database.connection import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def init_db() -> None:
    """Initialize all database tables defined in the app models."""
    # Import model modules so SQLAlchemy can register them.
    from backend.models.alert import Alert
    from backend.models.attack import AttackEvent
    from backend.models.blocked_ip import BlockedIP
    from backend.models.system_log import SystemLog
    from backend.models.traffic import TrafficEvent

    Base.metadata.create_all(bind=engine)


def get_db_session():
    """Yield a database session for repository/service use."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
