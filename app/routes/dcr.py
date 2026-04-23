"""
Doctor Call Report (DCR) Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import DoctorCallReport
from app.schemas import DCRCreate, DCRResponse
from app.services import DoctorService
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api/v1/dcr", tags=["Doctor Call Reports"])


@router.post("", response_model=DCRResponse, status_code=status.HTTP_201_CREATED)
def create_dcr(
    dcr: DCRCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new doctor call report"""
    # Verify doctor exists
    doctor = DoctorService.get_doctor(db, dcr.doctor_id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    db_dcr = DoctorCallReport(
        mr_id=user_id,
        doctor_id=dcr.doctor_id,
        products_discussed=dcr.products_discussed,
        remarks=dcr.remarks,
        visual_aid_presented=dcr.visual_aid_presented,
        visual_aid_url=dcr.visual_aid_url,
    )
    
    db.add(db_dcr)
    db.commit()
    db.refresh(db_dcr)
    
    # Increment doctor visit count
    DoctorService.increment_visit_count(db, dcr.doctor_id)
    
    return db_dcr


@router.get("", response_model=List[DCRResponse])
def get_dcr_list(user_id: int, db: Session = Depends(get_db)):
    """Get all DCR for current user"""
    dcrs = db.query(DoctorCallReport).filter(
        DoctorCallReport.mr_id == user_id
    ).order_by(DoctorCallReport.visit_date.desc()).all()
    return dcrs


@router.get("/{dcr_id}", response_model=DCRResponse)
def get_dcr(dcr_id: int, db: Session = Depends(get_db)):
    """Get specific DCR"""
    dcr = db.query(DoctorCallReport).filter(DoctorCallReport.id == dcr_id).first()
    
    if not dcr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DCR not found"
        )
    
    return dcr
