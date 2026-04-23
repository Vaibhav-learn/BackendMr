"""
Distributor Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import DistributorService
from app.schemas import DistributorCreate, DistributorResponse
from typing import List

router = APIRouter(prefix="/api/v1/distributors", tags=["Distributors"])


@router.post("", response_model=DistributorResponse, status_code=status.HTTP_201_CREATED)
def create_distributor(
    distributor: DistributorCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new distributor profile"""
    db_distributor = DistributorService.create_distributor(db, user_id, distributor)
    return db_distributor


@router.get("", response_model=List[DistributorResponse])
def get_my_distributors(user_id: int, db: Session = Depends(get_db)):
    """Get all distributors for current user"""
    distributors = DistributorService.get_mr_distributors(db, user_id)
    return distributors
