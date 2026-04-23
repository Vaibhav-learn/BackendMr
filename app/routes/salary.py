"""
Salary Slip Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import SalarySlip
from app.schemas import SalarySlipResponse
from typing import List

router = APIRouter(prefix="/api/v1/salary", tags=["Salary"])


@router.get("/slips", response_model=List[SalarySlipResponse])
def get_my_salary_slips(user_id: int, db: Session = Depends(get_db)):
    """Get all salary slips for current user"""
    slips = db.query(SalarySlip).filter(
        SalarySlip.user_id == user_id
    ).order_by(SalarySlip.year.desc(), SalarySlip.month.desc()).all()
    return slips


@router.get("/slips/{slip_id}", response_model=SalarySlipResponse)
def get_salary_slip(slip_id: int, db: Session = Depends(get_db)):
    """Get specific salary slip"""
    slip = db.query(SalarySlip).filter(SalarySlip.id == slip_id).first()
    
    if not slip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salary slip not found"
        )
    
    return slip


@router.get("/slips/{month}/{year}", response_model=SalarySlipResponse)
def get_salary_slip_by_month(
    month: str,
    year: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get salary slip for specific month"""
    slip = db.query(SalarySlip).filter(
        SalarySlip.user_id == user_id,
        SalarySlip.month == month,
        SalarySlip.year == year
    ).first()
    
    if not slip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salary slip not found for this month"
        )
    
    return slip
