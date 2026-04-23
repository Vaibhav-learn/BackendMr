"""
Target Management Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Target
from app.schemas import TargetCreate, TargetUpdate, TargetResponse
from typing import List

router = APIRouter(prefix="/api/v1/targets", tags=["Targets"])


@router.post("", response_model=TargetResponse, status_code=status.HTTP_201_CREATED)
def create_target(
    target: TargetCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create target (Admin only)"""
    db_target = Target(
        user_id=user_id,
        month=target.month,
        year=target.year,
        sales_target=target.sales_target,
        doctor_visits_target=target.doctor_visits_target,
        order_target=target.order_target,
    )
    
    db.add(db_target)
    db.commit()
    db.refresh(db_target)
    
    return db_target


@router.get("", response_model=List[TargetResponse])
def get_my_targets(user_id: int, db: Session = Depends(get_db)):
    """Get all targets for current user"""
    targets = db.query(Target).filter(
        Target.user_id == user_id
    ).order_by(Target.year.desc(), Target.month.desc()).all()
    return targets


@router.get("/{target_id}", response_model=TargetResponse)
def get_target(target_id: int, db: Session = Depends(get_db)):
    """Get target details"""
    target = db.query(Target).filter(Target.id == target_id).first()
    
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target not found"
        )
    
    return target


@router.put("/{target_id}", response_model=TargetResponse)
def update_target(
    target_id: int,
    target_update: TargetUpdate,
    db: Session = Depends(get_db)
):
    """Update target values"""
    target = db.query(Target).filter(Target.id == target_id).first()
    
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target not found"
        )
    
    update_data = target_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(target, key, value)
    
    db.commit()
    db.refresh(target)
    
    return target
