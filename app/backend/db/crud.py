"""
CRUD operations for the database models.

This module provides Create, Read, Update, Delete operations for database models.
It serves as an abstraction layer between the API endpoints and the database.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any, Union

from sqlalchemy.orm import Session

from app.backend.db.models import UserResponse, RsvpGuest, ButtonResponse, NumericResponse, RsvpStatistics


# UserResponse CRUD operations
def create_user_response(db: Session, response_data: Dict[str, Any]) -> UserResponse:
    """
    Create a new user response record.
    
    Args:
        db: Database session
        response_data: Dictionary containing response data
        
    Returns:
        The created UserResponse object
    """
    response = UserResponse(**response_data)
    db.add(response)
    db.commit()
    db.refresh(response)
    return response


def get_user_response(db: Session, response_id: int) -> Optional[UserResponse]:
    """
    Get a user response by ID.
    
    Args:
        db: Database session
        response_id: ID of the response to retrieve
        
    Returns:
        UserResponse object if found, None otherwise
    """
    return db.query(UserResponse).filter(UserResponse.id == response_id).first()


def get_user_responses_by_phone(db: Session, phone_number: str) -> List[UserResponse]:
    """
    Get all responses from a specific phone number.
    
    Args:
        db: Database session
        phone_number: Phone number to filter by
        
    Returns:
        List of UserResponse objects
    """
    return db.query(UserResponse).filter(UserResponse.phone_number == phone_number).order_by(UserResponse.created_at).all()


def get_user_responses_by_question(db: Session, question_key: str) -> List[UserResponse]:
    """
    Get all responses for a specific question.
    
    Args:
        db: Database session
        question_key: Question key to filter by
        
    Returns:
        List of UserResponse objects
    """
    return db.query(UserResponse).filter(UserResponse.question_key == question_key).order_by(UserResponse.created_at).all()


def update_user_response(db: Session, response_id: int, update_data: Dict[str, Any]) -> Optional[UserResponse]:
    """
    Update user response information.
    
    Args:
        db: Database session
        response_id: ID of the response to update
        update_data: Dictionary containing fields to update
        
    Returns:
        Updated UserResponse object or None if not found
    """
    response = get_user_response(db, response_id)
    if not response:
        return None
        
    for key, value in update_data.items():
        if hasattr(response, key):
            setattr(response, key, value)
    
    db.commit()
    db.refresh(response)
    return response


# RsvpGuest CRUD operations
def create_rsvp_guest(db: Session, guest_data: Dict[str, Any]) -> RsvpGuest:
    """
    Create a new RSVP guest record.
    
    Args:
        db: Database session
        guest_data: Dictionary containing guest data
        
    Returns:
        The created RsvpGuest object
    """
    guest = RsvpGuest(**guest_data)
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest


def get_rsvp_guest(db: Session, guest_id: int) -> Optional[RsvpGuest]:
    """
    Get an RSVP guest by ID.
    
    Args:
        db: Database session
        guest_id: ID of the guest to retrieve
        
    Returns:
        RsvpGuest object if found, None otherwise
    """
    return db.query(RsvpGuest).filter(RsvpGuest.id == guest_id).first()


def get_rsvp_guests_by_response(db: Session, user_response_id: int) -> List[RsvpGuest]:
    """
    Get all RSVP guests associated with a specific user response.
    
    Args:
        db: Database session
        user_response_id: ID of the user response
        
    Returns:
        List of RsvpGuest objects
    """
    return db.query(RsvpGuest).filter(RsvpGuest.user_response_id == user_response_id).all()


def update_rsvp_guest(db: Session, guest_id: int, update_data: Dict[str, Any]) -> Optional[RsvpGuest]:
    """
    Update RSVP guest information.
    
    Args:
        db: Database session
        guest_id: ID of the guest to update
        update_data: Dictionary containing fields to update
        
    Returns:
        Updated RsvpGuest object or None if not found
    """
    guest = get_rsvp_guest(db, guest_id)
    if not guest:
        return None
        
    for key, value in update_data.items():
        if hasattr(guest, key):
            setattr(guest, key, value)
    
    db.commit()
    db.refresh(guest)
    return guest


def delete_rsvp_guest(db: Session, guest_id: int) -> bool:
    """
    Delete an RSVP guest.
    
    Args:
        db: Database session
        guest_id: ID of the guest to delete
        
    Returns:
        True if deleted, False if not found
    """
    guest = get_rsvp_guest(db, guest_id)
    if not guest:
        return False
        
    db.delete(guest)
    db.commit()
    return True


# View CRUD operations - Read-only
def get_button_responses(db: Session) -> List[ButtonResponse]:
    """
    Get all button responses.
    
    Args:
        db: Database session
        
    Returns:
        List of ButtonResponse objects
    """
    return db.query(ButtonResponse).order_by(ButtonResponse.created_at).all()


def get_button_responses_by_question(db: Session, question_key: str) -> List[ButtonResponse]:
    """
    Get button responses for a specific question.
    
    Args:
        db: Database session
        question_key: Question key to filter by
        
    Returns:
        List of ButtonResponse objects
    """
    return db.query(ButtonResponse).filter(ButtonResponse.question_key == question_key).order_by(ButtonResponse.created_at).all()


def get_numeric_responses(db: Session) -> List[NumericResponse]:
    """
    Get all numeric responses.
    
    Args:
        db: Database session
        
    Returns:
        List of NumericResponse objects
    """
    return db.query(NumericResponse).order_by(NumericResponse.created_at).all()


def get_numeric_responses_by_question(db: Session, question_key: str) -> List[NumericResponse]:
    """
    Get numeric responses for a specific question.
    
    Args:
        db: Database session
        question_key: Question key to filter by
        
    Returns:
        List of NumericResponse objects
    """
    return db.query(NumericResponse).filter(NumericResponse.question_key == question_key).order_by(NumericResponse.created_at).all()


def get_rsvp_statistics(db: Session) -> Optional[RsvpStatistics]:
    """
    Get RSVP statistics.
    
    Args:
        db: Database session
        
    Returns:
        RsvpStatistics object if found, None otherwise
    """
    return db.query(RsvpStatistics).first() 