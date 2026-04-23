from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import ChemistService
from app.schemas import ChemistCreate, ChemistResponse
from typing import List

router = APIRouter(prefix="/api/v1/chemists", tags=["Chemists"])


@router.post("", response_model=ChemistResponse, status_code=status.HTTP_201_CREATED)
def create_chemist(
    chemist: ChemistCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    db_chemist = ChemistService.create_chemist(db, user_id, chemist)
    return db_chemist


@router.get("", response_model=List[ChemistResponse])
def get_my_chemists(user_id: int, db: Session = Depends(get_db)):
    chemists = ChemistService.get_mr_chemists(db, user_id)
    return chemists
