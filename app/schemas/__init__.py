"""
Pydantic Schemas for Request/Response Validation
"""
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum


class UserRole(str, Enum):
    MR = "MR"
    ASM = "ASM"
    ADMIN = "ADMIN"


# ============= User Schemas =============
class UserBase(BaseModel):
    employee_id: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    phone: Optional[str] = None
    role: UserRole = UserRole.MR
    assigned_area: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    assigned_area: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None


class UserChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


# ============= Auth Schemas =============
class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ============= Attendance Schemas =============
class AttendanceCheckIn(BaseModel):
    latitude: str
    longitude: str
    selfie_url: Optional[str] = None


class AttendanceCheckOut(BaseModel):
    latitude: str
    longitude: str
    selfie_url: Optional[str] = None


class AttendanceResponse(BaseModel):
    id: int
    user_id: int
    check_in_time: datetime
    check_out_time: Optional[datetime]
    check_in_latitude: str
    check_in_longitude: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============= Doctor Schemas =============
class DoctorBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    phone: str = Field(..., min_length=10, max_length=20)
    specialization: str = Field(..., max_length=255)
    registration_number: Optional[str] = None
    clinic_name: str
    clinic_address: Optional[str] = None
    clinic_latitude: Optional[str] = None
    clinic_longitude: Optional[str] = None


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    clinic_latitude: Optional[str] = None
    clinic_longitude: Optional[str] = None


class DoctorResponse(DoctorBase):
    id: int
    mr_id: int
    visit_frequency: int
    last_visited: Optional[datetime]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============= Chemist Schemas =============
class ChemistBase(BaseModel):
    shop_name: str = Field(..., max_length=255)
    owner_name: str = Field(..., max_length=255)
    phone: str = Field(..., min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    gst_number: Optional[str] = None


class ChemistCreate(ChemistBase):
    pass


class ChemistResponse(ChemistBase):
    id: int
    mr_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============= Distributor Schemas =============
class DistributorBase(BaseModel):
    business_name: str = Field(..., max_length=255)
    contact_person: str = Field(..., max_length=255)
    phone: str = Field(..., min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    warehouse_location: Optional[str] = None
    distribution_area: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None


class DistributorCreate(DistributorBase):
    pass


class DistributorResponse(DistributorBase):
    id: int
    mr_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============= Doctor Call Report Schemas =============
class DCRCreate(BaseModel):
    doctor_id: int
    products_discussed: Optional[str] = None
    remarks: Optional[str] = None
    visual_aid_presented: bool = False
    visual_aid_url: Optional[str] = None


class DCRResponse(BaseModel):
    id: int
    mr_id: int
    doctor_id: int
    visit_date: datetime
    products_discussed: Optional[str]
    remarks: Optional[str]
    visual_aid_presented: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============= Order Schemas =============
class OrderCreate(BaseModel):
    product_details: str = Field(..., min_length=5, max_length=1000)
    quantity: int = Field(..., gt=0)
    order_notes: Optional[str] = None


class OrderApprove(BaseModel):
    approved: bool
    rejection_reason: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    mr_id: int
    product_details: str
    quantity: int
    status: str
    approval_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============= Leave Schemas =============
class LeaveCreate(BaseModel):
    leave_type: str = Field(..., min_length=3, max_length=50)
    start_date: datetime
    end_date: datetime
    reason: Optional[str] = None

    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v


class LeaveApprove(BaseModel):
    approved: bool
    rejection_reason: Optional[str] = None


class LeaveResponse(BaseModel):
    id: int
    user_id: int
    leave_type: str
    start_date: datetime
    end_date: datetime
    reason: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============= Target Schemas =============
class TargetCreate(BaseModel):
    month: str
    year: int
    sales_target: int = Field(default=0, ge=0)
    doctor_visits_target: int = Field(default=0, ge=0)
    order_target: int = Field(default=0, ge=0)


class TargetUpdate(BaseModel):
    sales_target: Optional[int] = None
    doctor_visits_target: Optional[int] = None
    order_target: Optional[int] = None


class TargetResponse(BaseModel):
    id: int
    user_id: int
    month: str
    year: int
    sales_target: int
    sales_achieved: int
    doctor_visits_target: int
    doctor_visits_achieved: int
    order_target: int
    order_achieved: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============= Salary Slip Schemas =============
class SalarySlipResponse(BaseModel):
    id: int
    user_id: int
    month: str
    year: int
    basic_salary: int
    allowances: int
    deductions: int
    net_salary: int
    tax_deducted: int
    slip_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ============= Notification Schemas =============
class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MarkNotificationAsRead(BaseModel):
    is_read: bool


# ============= Error Response Schema =============
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
