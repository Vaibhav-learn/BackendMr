from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import DoctorService
from app.schemas import DoctorCreate, DoctorResponse, DoctorUpdate
from typing import List

router = APIRouter(prefix="/api/v1/doctors", tags=["Doctors"])


@router.post("", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(
    doctor: DoctorCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    db_doctor = DoctorService.create_doctor(db, user_id, doctor)
    return db_doctor


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = DoctorService.get_doctor(db, doctor_id)
    
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    return doctor


@router.get("", response_model=List[DoctorResponse])
def get_my_doctors(user_id: int, db: Session = Depends(get_db)):
    doctors = DoctorService.get_mr_doctors(db, user_id)
    return doctors


@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor_update: DoctorUpdate,
    db: Session = Depends(get_db)
):
    doctor = DoctorService.update_doctor(db, doctor_id, doctor_update.dict(exclude_unset=True))
    
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    return doctor


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = DoctorService.get_doctor(db, doctor_id)
    
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    doctor.is_active = False
    db.commit()
    
    return None
