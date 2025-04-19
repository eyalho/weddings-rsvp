"""
RSVP API endpoints.

This module provides endpoints for retrieving RSVP information and statistics.
"""
from typing import Dict, Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.backend.db.session import get_db
from app.backend.db import crud
from app.backend.db.models import RsvpGuest, RsvpStatistics

router = APIRouter()


@router.get("/stats")
def get_rsvp_statistics(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get RSVP statistics.
    
    Returns summary statistics about RSVPs including:
    - Total number of guests
    - Number of guests attending
    - Number of guests not attending
    - Attendance rate
    """
    stats = crud.get_rsvp_statistics(db)
    if not stats:
        return {
            "total_guests": 0,
            "attending_guests": 0,
            "not_attending_guests": 0,
            "attendance_rate": 0,
            "total_responses": 0
        }
    
    return {
        "total_guests": stats.total_guests or 0,
        "attending_guests": stats.attending_guests or 0,
        "not_attending_guests": stats.not_attending_guests or 0,
        "attendance_rate": stats.attendance_rate,
        "total_responses": stats.total_responses or 0
    }


@router.get("/guests")
def get_all_rsvp_guests(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Get all RSVP guests with pagination.
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        
    Returns:
        List of RSVP guest information
    """
    guests = db.query(RsvpGuest).order_by(RsvpGuest.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for guest in guests:
        # Get the associated user response to get the phone number
        user_response = guest.user_response
        
        result.append({
            "id": guest.id,
            "name": guest.name,
            "attending": guest.attending,
            "dietary_restrictions": guest.dietary_restrictions,
            "phone_number": user_response.phone_number if user_response else None,
            "created_at": guest.created_at.isoformat() if guest.created_at else None,
            "updated_at": guest.updated_at.isoformat() if guest.updated_at else None
        })
    
    return result


@router.get("/guests/search")
def search_rsvp_guests(
    query: str,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Search for RSVP guests by name or phone number.
    
    Args:
        query: Search term (name or phone number)
        
    Returns:
        List of matching RSVP guests
    """
    # Search in both the name field and phone number field
    guests = db.query(RsvpGuest).join(RsvpGuest.user_response).filter(
        (RsvpGuest.name.ilike(f"%{query}%")) | 
        (RsvpGuest.user_response.has(phone_number=query))
    ).all()
    
    result = []
    for guest in guests:
        user_response = guest.user_response
        
        result.append({
            "id": guest.id,
            "name": guest.name,
            "attending": guest.attending,
            "dietary_restrictions": guest.dietary_restrictions,
            "phone_number": user_response.phone_number if user_response else None,
            "created_at": guest.created_at.isoformat() if guest.created_at else None,
            "updated_at": guest.updated_at.isoformat() if guest.updated_at else None
        })
    
    return result 