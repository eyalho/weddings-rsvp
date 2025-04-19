"""
SQLAlchemy ORM models for the database.

This module defines the ORM models for the database tables and views.
"""
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, Text,
    Float, func, text
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from typing import List, Optional
from datetime import datetime

Base = declarative_base()


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