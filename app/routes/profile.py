"""
User Profile Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import UserService
from app.schemas import UserResponse, UserUpdate

router = APIRouter(prefix="/api/v1/profile", tags=["Profile"])


@router.get("", response_model=UserResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    """Get current user profile"""
    user = UserService.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.put("", response_model=UserResponse)
def update_profile(
    user_update: UserUpdate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Update user profile"""
    user = UserService.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    
    return user
