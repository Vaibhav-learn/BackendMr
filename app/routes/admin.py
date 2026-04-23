from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import User, Order, Leave, Attendance, Doctor, Chemist, Distributor
from app.schemas import UserResponse, OrderResponse, LeaveResponse
from typing import List, Optional

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_details(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.get("/attendance", response_model=List[dict])
def get_all_attendance(
    db: Session = Depends(get_db),
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
):
    query = db.query(Attendance)
    
    if date_from:
        query = query.filter(Attendance.check_in_time >= date_from)
    if date_to:
        query = query.filter(Attendance.check_in_time <= date_to)
    
    records = query.order_by(Attendance.check_in_time.desc()).all()
    
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "date": r.check_in_time.date(),
            "check_in_time": r.check_in_time,
            "check_out_time": r.check_out_time,
            "status": r.status
        }
        for r in records
    ]


@router.get("/attendance/{user_id}", response_model=List[dict])
def get_user_attendance(
    user_id: int,
    db: Session = Depends(get_db),
    limit: int = Query(30, ge=1, le=100)
):
    records = db.query(Attendance).filter(
        Attendance.user_id == user_id
    ).order_by(Attendance.check_in_time.desc()).limit(limit).all()
    
    return [
        {
            "id": r.id,
            "date": r.check_in_time.date(),
            "check_in_time": r.check_in_time,
            "check_out_time": r.check_out_time,
            "status": r.status,
            "latitude": r.check_in_latitude,
            "longitude": r.check_in_longitude
        }
        for r in records
    ]


@router.get("/doctors", response_model=List[dict])
def get_all_doctors(db: Session = Depends(get_db)):
    """Get all onboarded doctors (Admin only)"""
    doctors = db.query(Doctor).all()
    
    return [
        {
            "id": d.id,
            "name": d.name,
            "specialization": d.specialization,
            "mr_id": d.mr_id,
            "visits": d.visit_frequency,
            "last_visited": d.last_visited,
            "is_active": d.is_active
        }
        for d in doctors
    ]


@router.get("/chemists", response_model=List[dict])
def get_all_chemists(db: Session = Depends(get_db)):
    """Get all onboarded chemists (Admin only)"""
    chemists = db.query(Chemist).all()
    
    return [
        {
            "id": c.id,
            "shop_name": c.shop_name,
            "owner_name": c.owner_name,
            "mr_id": c.mr_id,
            "is_active": c.is_active
        }
        for c in chemists
    ]


@router.get("/distributors", response_model=List[dict])
def get_all_distributors(db: Session = Depends(get_db)):
    """Get all onboarded distributors (Admin only)"""
    distributors = db.query(Distributor).all()
    
    return [
        {
            "id": d.id,
            "business_name": d.business_name,
            "contact_person": d.contact_person,
            "mr_id": d.mr_id,
            "is_active": d.is_active
        }
        for d in distributors
    ]


@router.get("/pending-orders", response_model=List[OrderResponse])
def get_pending_orders(db: Session = Depends(get_db)):
    """Get all pending orders (Admin only)"""
    orders = db.query(Order).filter(
        Order.status == "pending"
    ).order_by(Order.created_at.desc()).all()
    return orders


@router.get("/pending-leaves", response_model=List[LeaveResponse])
def get_pending_leaves(db: Session = Depends(get_db)):
    """Get all pending leave requests (Admin only)"""
    leaves = db.query(Leave).filter(
        Leave.status == "pending"
    ).order_by(Leave.created_at.desc()).all()
    return leaves


@router.get("/dashboard/stats", response_model=dict)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics (Admin only)"""
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_doctors = db.query(Doctor).count()
    total_chemists = db.query(Chemist).count()
    total_distributors = db.query(Distributor).count()
    pending_orders = db.query(Order).filter(Order.status == "pending").count()
    pending_leaves = db.query(Leave).filter(Leave.status == "pending").count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_doctors": total_doctors,
        "total_chemists": total_chemists,
        "total_distributors": total_distributors,
        "pending_orders": pending_orders,
        "pending_leaves": pending_leaves
    }
