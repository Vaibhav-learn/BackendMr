from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum
from datetime import datetime
from enum import Enum as PyEnum
from app.core.database import Base


class UserRole(str, PyEnum):
    """User roles"""
    MR = "MR"
    ASM = "ASM"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)

    role = Column(Enum(UserRole), default=UserRole.MR, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    assigned_area = Column(String(255), nullable=True)
    manager_id = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    emergency_contact_name = Column(String(255), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)

    check_in_time = Column(DateTime, nullable=False)
    check_out_time = Column(DateTime, nullable=True)

    check_in_latitude = Column(String(50), nullable=False)
    check_in_longitude = Column(String(50), nullable=False)
    check_out_latitude = Column(String(50), nullable=True)
    check_out_longitude = Column(String(50), nullable=True)

    check_in_selfie_url = Column(String(500), nullable=True)
    check_out_selfie_url = Column(String(500), nullable=True)
    is_valid = Column(Boolean, default=True, nullable=False)

    status = Column(String(50), default="present", nullable=False)  # present, absent, leave
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    mr_id = Column(Integer, nullable=False, index=True)

    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=False)

    specialization = Column(String(255), nullable=False)
    registration_number = Column(String(100), nullable=True)

    clinic_name = Column(String(255), nullable=False)
    clinic_address = Column(String(500), nullable=True)
    clinic_latitude = Column(String(50), nullable=True)
    clinic_longitude = Column(String(50), nullable=True)

    visit_frequency = Column(Integer, default=0, nullable=False)
    last_visited = Column(DateTime, nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Chemist(Base):
    __tablename__ = "chemists"

    id = Column(Integer, primary_key=True, index=True)
    mr_id = Column(Integer, nullable=False, index=True)

    shop_name = Column(String(255), nullable=False)
    owner_name = Column(String(255), nullable=False)

    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)

    address = Column(String(500), nullable=True)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)

    gst_number = Column(String(100), nullable=True)
    license_url = Column(String(500), nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Distributor(Base):
    __tablename__ = "distributors"

    id = Column(Integer, primary_key=True, index=True)
    mr_id = Column(Integer, nullable=False, index=True)

    business_name = Column(String(255), nullable=False)
    contact_person = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)

    warehouse_location = Column(String(500), nullable=True)
    distribution_area = Column(String(255), nullable=True)

    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class DoctorCallReport(Base):
    __tablename__ = "doctor_call_reports"

    id = Column(Integer, primary_key=True, index=True)
    mr_id = Column(Integer, nullable=False, index=True)
    doctor_id = Column(Integer, nullable=False, index=True)

    visit_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    products_discussed = Column(String(1000), nullable=True)
    remarks = Column(String(1000), nullable=True)

    visual_aid_presented = Column(Boolean, default=False, nullable=False)
    visual_aid_url = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    mr_id = Column(Integer, nullable=False, index=True)

    product_details = Column(String(1000), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_notes = Column(String(500), nullable=True)

    status = Column(String(50), default="pending", nullable=False)  # pending, approved, rejected, shipped
    approved_by = Column(Integer, nullable=True)
    approval_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)

    leave_type = Column(String(50), nullable=False)  # sick, casual, personal, etc.
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    reason = Column(String(500), nullable=True)

    status = Column(String(50), default="pending", nullable=False)  # pending, approved, rejected
    approved_by = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)

    month = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    
    sales_target = Column(Integer, default=0, nullable=False)
    sales_achieved = Column(Integer, default=0, nullable=False)
    
    doctor_visits_target = Column(Integer, default=0, nullable=False)
    doctor_visits_achieved = Column(Integer, default=0, nullable=False)
    
    order_target = Column(Integer, default=0, nullable=False)
    order_achieved = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SalarySlip(Base):
    __tablename__ = "salary_slips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)

    month = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)

    basic_salary = Column(Integer, default=0, nullable=False)
    allowances = Column(Integer, default=0, nullable=False)
    deductions = Column(Integer, default=0, nullable=False)
    net_salary = Column(Integer, default=0, nullable=False)

    tax_deducted = Column(Integer, default=0, nullable=False)

    slip_url = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)

    title = Column(String(255), nullable=False)
    message = Column(String(1000), nullable=False)
    notification_type = Column(String(50), default="info", nullable=False)  # info, alert, urgent

    is_read = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
