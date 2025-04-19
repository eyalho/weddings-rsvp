"""
SQLAlchemy ORM models for the database.

This module defines the ORM models for the database tables and views.
"""
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, Text,
    Float, func, text
)
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from typing import List, Optional, Dict, Any
from datetime import datetime
import os
import sys

Base = declarative_base()

# Define target_metadata for Alembic
target_metadata = Base.metadata


class UserResponse(Base):
    """
    Model for the user_responses table.
    
    Represents a response from a user to a question or RSVP.
    """
    __tablename__ = "user_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), nullable=False, index=True)
    question_key = Column(String(50), nullable=False, index=True)
    response_text = Column(Text)
    response_value = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rsvp_guests = relationship("RsvpGuest", back_populates="user_response", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<UserResponse(id={self.id}, phone={self.phone_number}, question={self.question_key})>"


class RsvpGuest(Base):
    """
    Model for the rsvp_guests table.
    
    Represents a guest in an RSVP response.
    """
    __tablename__ = "rsvp_guests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_response_id = Column(Integer, ForeignKey("user_responses.id"), nullable=False)
    name = Column(String(100), nullable=False)
    attending = Column(Boolean, nullable=False)
    dietary_restrictions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user_response = relationship("UserResponse", back_populates="rsvp_guests")
    
    def __repr__(self):
        return f"<RsvpGuest(id={self.id}, name={self.name}, attending={self.attending})>"


class ButtonResponse(Base):
    """
    Model for the button_responses view.
    
    Represents aggregated button response data.
    """
    __tablename__ = "button_responses"
    
    # This is a database view, not a table
    __table_args__ = {"info": {"is_view": True}}
    
    id = Column(Integer, primary_key=True)
    question_key = Column(String(50), nullable=False)
    response_value = Column(String(50), nullable=False)
    count = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<ButtonResponse(question={self.question_key}, value={self.response_value}, count={self.count})>"


class NumericResponse(Base):
    """
    Model for the numeric_responses view.
    
    Represents aggregated numeric response data.
    """
    __tablename__ = "numeric_responses"
    
    # This is a database view, not a table
    __table_args__ = {"info": {"is_view": True}}
    
    id = Column(Integer, primary_key=True)
    question_key = Column(String(50), nullable=False)
    min_value = Column(Float)
    max_value = Column(Float)
    avg_value = Column(Float)
    count = Column(Integer)
    
    def __repr__(self):
        return f"<NumericResponse(question={self.question_key}, avg={self.avg_value}, count={self.count})>"


class RsvpStatistics(Base):
    """
    Model for the rsvp_statistics view.
    
    Represents aggregated RSVP statistics.
    """
    __tablename__ = "rsvp_statistics"
    
    # This is a database view, not a table
    __table_args__ = {"info": {"is_view": True}}
    
    id = Column(Integer, primary_key=True)
    total_responses = Column(Integer)
    attending_count = Column(Integer)
    not_attending_count = Column(Integer)
    total_guests = Column(Integer)
    attending_guests = Column(Integer)
    not_attending_guests = Column(Integer)
    
    @hybrid_property
    def attendance_rate(self) -> float:
        """Calculate the attendance rate as a percentage."""
        if self.total_guests == 0:
            return 0.0
        return (self.attending_guests / self.total_guests) * 100
    
    def __repr__(self):
        return f"<RsvpStatistics(attending={self.attending_guests}, total={self.total_guests})>"


# Helper functions for SQLAlchemy models
def create_response(db: Session, phone_number: str, question_key: str, response_data: Dict[str, Any]) -> UserResponse:
    """
    Create a new response record.
    
    Args:
        db: Database session
        phone_number: User's phone number
        question_key: Key identifying the question or interaction
        response_data: Dictionary with response_text and/or response_value
        
    Returns:
        The created UserResponse object
    """
    user_response = UserResponse(
        phone_number=phone_number,
        question_key=question_key,
        response_text=response_data.get("response_text", ""),
        response_value=response_data.get("response_value", "")
    )
    
    db.add(user_response)
    db.commit()
    db.refresh(user_response)
    return user_response


def get_guest_by_phone(db: Session, phone_number: str) -> Optional[RsvpGuest]:
    """
    Get the most recent RSVP guest record for a phone number.
    
    Args:
        db: Database session
        phone_number: Phone number to look up
        
    Returns:
        The most recent RsvpGuest object or None
    """
    # Find the most recent user response for this phone number
    latest_response = db.query(UserResponse).filter(
        UserResponse.phone_number == phone_number
    ).order_by(UserResponse.created_at.desc()).first()
    
    if not latest_response:
        return None
    
    # Get the associated guest
    guest = db.query(RsvpGuest).filter(
        RsvpGuest.user_response_id == latest_response.id
    ).first()
    
    return guest


def update_guest(db: Session, guest_id: int, update_data: Dict[str, Any]) -> Optional[RsvpGuest]:
    """
    Update an RSVP guest record.
    
    Args:
        db: Database session
        guest_id: ID of the guest to update
        update_data: Dictionary with fields to update
        
    Returns:
        The updated RsvpGuest object or None
    """
    guest = db.query(RsvpGuest).filter(RsvpGuest.id == guest_id).first()
    if not guest:
        return None
    
    for key, value in update_data.items():
        if hasattr(guest, key):
            setattr(guest, key, value)
    
    db.commit()
    db.refresh(guest)
    return guest


def create_guest(db: Session, response_id: int, guest_data: Dict[str, Any]) -> RsvpGuest:
    """
    Create a new RSVP guest record.
    
    Args:
        db: Database session
        response_id: ID of the associated user response
        guest_data: Dictionary with guest details
        
    Returns:
        The created RsvpGuest object
    """
    guest = RsvpGuest(
        user_response_id=response_id,
        name=guest_data.get("name", ""),
        attending=guest_data.get("attending", False),
        dietary_restrictions=guest_data.get("dietary_restrictions", "")
    )
    
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest


def get_rsvp_statistics(db: Session) -> Optional[RsvpStatistics]:
    """
    Get the RSVP statistics.
    
    Args:
        db: Database session
        
    Returns:
        The RsvpStatistics object or None
    """
    return db.query(RsvpStatistics).first()


def get_responses_by_phone(db: Session, phone_number: str) -> List[UserResponse]:
    """
    Get all responses from a specific phone number.
    
    Args:
        db: Database session
        phone_number: Phone number to filter by
        
    Returns:
        List of UserResponse objects
    """
    return db.query(UserResponse).filter(
        UserResponse.phone_number == phone_number
    ).order_by(UserResponse.created_at).all() 