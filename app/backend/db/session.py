"""
Database session management.

This module provides functions for creating database sessions and connections.
It includes utilities for dependency injection in FastAPI routes.
"""
from typing import Generator, Any
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.backend.core.config import settings

engine = create_engine(
    settings.DATABASE_URI,
    pool_pre_ping=True,
    echo=settings.SQL_ECHO,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, Any, None]:
    """
    FastAPI dependency that provides a database session.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session() -> Generator[Session, Any, None]:
    """
    Context manager that provides a database session.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 