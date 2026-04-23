"""
Service Layer for Business Logic
"""
from sqlalchemy.orm import Session
from app.models import User, Attendance, Doctor, Chemist, Distributor
from app.schemas import (
    UserCreate, DoctorCreate, ChemistCreate, DistributorCreate,
    AttendanceCheckIn, AttendanceCheckOut
)
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from datetime import datetime
from typing import Optional, List


class UserService:
    """User management service"""
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        db_user = User(
            employee_id=user_data.employee_id,
            email=user_data.email,
            full_name=user_data.full_name,
            phone=user_data.phone,
            role=user_data.role,
            assigned_area=user_data.assigned_area,
            hashed_password=hash_password(user_data.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    def update_last_login(db: Session, user_id: int):
        """Update last login timestamp"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.last_login = datetime.utcnow()
            db.commit()


class AttendanceService:
    """Attendance management service"""
    
    @staticmethod
    def check_in(db: Session, user_id: int, check_in_data: AttendanceCheckIn) -> Attendance:
        """Record check-in"""
        attendance = Attendance(
            user_id=user_id,
            check_in_time=datetime.utcnow(),
            check_in_latitude=check_in_data.latitude,
            check_in_longitude=check_in_data.longitude,
            check_in_selfie_url=check_in_data.selfie_url,
        )
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        return attendance
    
    @staticmethod
    def check_out(db: Session, user_id: int, check_out_data: AttendanceCheckOut) -> Optional[Attendance]:
        """Record check-out"""
        attendance = db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.check_out_time == None
        ).order_by(Attendance.check_in_time.desc()).first()
        
        if not attendance:
            return None
        
        attendance.check_out_time = datetime.utcnow()
        attendance.check_out_latitude = check_out_data.latitude
        attendance.check_out_longitude = check_out_data.longitude
        attendance.check_out_selfie_url = check_out_data.selfie_url
        
        db.commit()
        db.refresh(attendance)
        return attendance
    
    @staticmethod
    def get_today_attendance(db: Session, user_id: int) -> Optional[Attendance]:
        """Get today's attendance record"""
        today = datetime.utcnow().date()
        return db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.check_in_time >= datetime(today.year, today.month, today.day)
        ).first()
    
    @staticmethod
    def get_attendance_history(db: Session, user_id: int, limit: int = 30) -> List[Attendance]:
        """Get attendance history"""
        return db.query(Attendance).filter(
            Attendance.user_id == user_id
        ).order_by(Attendance.check_in_time.desc()).limit(limit).all()


class DoctorService:
    """Doctor management service"""
    
    @staticmethod
    def create_doctor(db: Session, mr_id: int, doctor_data: DoctorCreate) -> Doctor:
        """Create a new doctor profile"""
        doctor = Doctor(
            mr_id=mr_id,
            **doctor_data.dict()
        )
        db.add(doctor)
        db.commit()
        db.refresh(doctor)
        return doctor
    
    @staticmethod
    def get_doctor(db: Session, doctor_id: int) -> Optional[Doctor]:
        """Get doctor by ID"""
        return db.query(Doctor).filter(Doctor.id == doctor_id).first()
    
    @staticmethod
    def get_mr_doctors(db: Session, mr_id: int) -> List[Doctor]:
        """Get all doctors for an MR"""
        return db.query(Doctor).filter(Doctor.mr_id == mr_id, Doctor.is_active == True).all()
    
    @staticmethod
    def update_doctor(db: Session, doctor_id: int, update_data: dict) -> Optional[Doctor]:
        """Update doctor profile"""
        doctor = DoctorService.get_doctor(db, doctor_id)
        if not doctor:
            return None
        
        for key, value in update_data.items():
            if value is not None:
                setattr(doctor, key, value)
        
        db.commit()
        db.refresh(doctor)
        return doctor
    
    @staticmethod
    def increment_visit_count(db: Session, doctor_id: int):
        """Increment doctor visit count"""
        doctor = DoctorService.get_doctor(db, doctor_id)
        if doctor:
            doctor.visit_frequency += 1
            doctor.last_visited = datetime.utcnow()
            db.commit()


class ChemistService:
    """Chemist management service"""
    
    @staticmethod
    def create_chemist(db: Session, mr_id: int, chemist_data: ChemistCreate) -> Chemist:
        """Create a new chemist profile"""
        chemist = Chemist(
            mr_id=mr_id,
            **chemist_data.dict()
        )
        db.add(chemist)
        db.commit()
        db.refresh(chemist)
        return chemist
    
    @staticmethod
    def get_mr_chemists(db: Session, mr_id: int) -> List[Chemist]:
        """Get all chemists for an MR"""
        return db.query(Chemist).filter(Chemist.mr_id == mr_id, Chemist.is_active == True).all()


class DistributorService:
    """Distributor management service"""
    
    @staticmethod
    def create_distributor(db: Session, mr_id: int, distributor_data: DistributorCreate) -> Distributor:
        """Create a new distributor profile"""
        distributor = Distributor(
            mr_id=mr_id,
            **distributor_data.dict()
        )
        db.add(distributor)
        db.commit()
        db.refresh(distributor)
        return distributor
    
    @staticmethod
    def get_mr_distributors(db: Session, mr_id: int) -> List[Distributor]:
        """Get all distributors for an MR"""
        return db.query(Distributor).filter(Distributor.mr_id == mr_id, Distributor.is_active == True).all()
