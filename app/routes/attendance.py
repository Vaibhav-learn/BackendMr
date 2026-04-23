"""
Attendance Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import AttendanceService
from app.schemas import AttendanceCheckIn, AttendanceCheckOut, AttendanceResponse
from typing import List

router = APIRouter(prefix="/api/v1/attendance", tags=["Attendance"])


@router.post("/check-in", response_model=AttendanceResponse)
def check_in(
    check_in_data: AttendanceCheckIn,
    user_id: int,
    db: Session = Depends(get_db)
):
    today_attendance = AttendanceService.get_today_attendance(db, user_id)
    if today_attendance and today_attendance.check_out_time is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already checked in today"
        )
    
    attendance = AttendanceService.check_in(db, user_id, check_in_data)
    return attendance


@router.post("/check-out", response_model=AttendanceResponse)
def check_out(
    check_out_data: AttendanceCheckOut,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Record employee check-out"""
    attendance = AttendanceService.check_out(db, user_id, check_out_data)
    
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active check-in found"
        )
    
    return attendance


@router.get("/today", response_model=AttendanceResponse)
def get_today_attendance(user_id: int, db: Session = Depends(get_db)):
    attendance = AttendanceService.get_today_attendance(db, user_id)
    
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No attendance record found for today"
        )
    
    return attendance


@router.get("/history", response_model=List[AttendanceResponse])
def get_attendance_history(
    user_id: int,
    limit: int = 30,
    db: Session = Depends(get_db)
):
    history = AttendanceService.get_attendance_history(db, user_id, limit)
    return history
