from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Leave
from app.schemas import LeaveCreate, LeaveApprove, LeaveResponse
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api/v1/leaves", tags=["Leaves"])


@router.post("", response_model=LeaveResponse, status_code=status.HTTP_201_CREATED)
def apply_leave(
    leave: LeaveCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    db_leave = Leave(
        user_id=user_id,
        leave_type=leave.leave_type,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status="pending"
    )
    
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    
    return db_leave


@router.get("", response_model=List[LeaveResponse])
def get_my_leaves(user_id: int, db: Session = Depends(get_db)):
    leaves = db.query(Leave).filter(
        Leave.user_id == user_id
    ).order_by(Leave.created_at.desc()).all()
    return leaves


@router.get("/{leave_id}", response_model=LeaveResponse)
def get_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    
    if not leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave not found"
        )
    
    return leave


@router.post("/{leave_id}/approve", response_model=LeaveResponse)
def approve_leave(
    leave_id: int,
    approval: LeaveApprove,
    admin_id: int,
    db: Session = Depends(get_db)
):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    
    if not leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave not found"
        )
    
    leave.status = "approved" if approval.approved else "rejected"
    leave.approved_by = admin_id
    
    db.commit()
    db.refresh(leave)
    
    return leave
