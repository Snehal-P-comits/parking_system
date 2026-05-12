"""SQLAlchemy engine/session setup and DB session dependency."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    # Declarative base shared by all ORM models.
    pass


# Engine is configured once from settings to keep DB access centralized.
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session, future=True)


def get_db_session() -> Generator[Session, None, None]:
    # FastAPI dependency: yields a unit-of-work session per request.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
