
MR & ASM Reporting Application - API Endpoints Documentation

Base URL: http://localhost:8000/api/v1

Authentication:
- Use JWT tokens obtained from login endpoint
- Include token in Authorization header: "Bearer <token>"

AUTHENTICATION ENDPOINTS

1. Register User
POST /auth/register
Request:
{
    "employee_id": "EMP001",
    "email": "user@example.com",
    "full_name": "John Doe",
    "phone": "+919876543210",
    "role": "MR",
    "assigned_area": "Mumbai",
    "password": "SecurePassword123"
}

Response:
{
    "id": 1,
    "employee_id": "EMP001",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "MR",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00"
}


2. Login
POST /auth/login
Request:
{
    "email": "user@example.com",
    "password": "SecurePassword123"
}

Response:
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}


3. Refresh Token
POST /auth/refresh
Request:
{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}


4. Change Password
POST /auth/change-password
Request:
{
    "old_password": "OldPassword123",
    "new_password": "NewPassword456"
}

ATTENDANCE ENDPOINTS

1. Check-In
POST /attendance/check-in
Request:
{
    "latitude": "19.0760",
    "longitude": "72.8777",
    "selfie_url": "https://..."
}

Response:
{
    "id": 1,
    "user_id": 1,
    "check_in_time": "2024-01-15T09:00:00",
    "check_in_latitude": "19.0760",
    "check_in_longitude": "72.8777",
    "status": "present"
}


2. Check-Out
POST /attendance/check-out
Request:
{
    "latitude": "19.0761",
    "longitude": "72.8778",
    "selfie_url": "https://..."
}


3. Get Today's Attendance
GET /attendance/today


4. Get Attendance History
GET /attendance/history?limit=30

DOCTOR ENDPOINTS

1. Add Doctor
POST /doctors
Request:
{
    "name": "Dr. Sharma",
    "email": "dr.sharma@hospital.com",
    "phone": "+919876543210",
    "specialization": "Cardiology",
    "registration_number": "MCI-12345",
    "clinic_name": "Sharma Clinic",
    "clinic_address": "123 Medical Street, Mumbai",
    "clinic_latitude": "19.0760",
    "clinic_longitude": "72.8777"
}


2. Get Doctor List
GET /doctors


3. Get Doctor Details
GET /doctors/{doctor_id}


4. Update Doctor
PUT /doctors/{doctor_id}


5. Delete Doctor
DELETE /doctors/{doctor_id}

CHEMIST ENDPOINTS

1. Add Chemist
POST /chemists
Request:
{
    "shop_name": "Pharmacy Plus",
    "owner_name": "Mr. Patel",
    "phone": "+919876543210",
    "email": "contact@pharmacy.com",
    "address": "456 Retail Street, Mumbai",
    "gst_number": "27AABCT1234F1Z0"
}


2. Get Chemist List
GET /chemists

DISTRIBUTOR ENDPOINTS

1. Add Distributor
POST /distributors
Request:
{
    "business_name": "Pharma Distributors Ltd",
    "contact_person": "Mr. Verma",
    "phone": "+919876543210",
    "warehouse_location": "Industrial Area, Mumbai",
    "distribution_area": "Western Region"
}


2. Get Distributor List
GET /distributors

DCR (DOCTOR CALL REPORT) ENDPOINTS

1. Create DCR
POST /dcr
Request:
{
    "doctor_id": 1,
    "products_discussed": "Aspirin, Paracetamol",
    "remarks": "Doctor interested in new formulation",
    "visual_aid_presented": true,
    "visual_aid_url": "https://..."
}


2. Get DCR List
GET /dcr


3. Get DCR Details
GET /dcr/{dcr_id}

ORDER ENDPOINTS

1. Create Order
POST /orders
Request:
{
    "product_details": "Aspirin 500mg - 100 tablets",
    "quantity": 500,
    "order_notes": "Urgent delivery required"
}


2. Get Order List
GET /orders


3. Get Order Details
GET /orders/{order_id}


4. Approve/Reject Order (Admin)
POST /orders/{order_id}/approve
Request:
{
    "approved": true,
    "rejection_reason": null
}

LEAVE ENDPOINTS

1. Apply Leave
POST /leaves
Request:
{
    "leave_type": "sick",
    "start_date": "2024-01-20T00:00:00",
    "end_date": "2024-01-22T00:00:00",
    "reason": "Medical checkup"
}


2. Get Leave List
GET /leaves


3. Approve/Reject Leave (Admin)
POST /leaves/{leave_id}/approve
Request:
{
    "approved": true,
    "rejection_reason": null
}

TARGET ENDPOINTS

1. Get Targets
GET /targets


2. Get Target Details
GET /targets/{target_id}


3. Update Target
PUT /targets/{target_id}
Request:
{
    "sales_target": 100000,
    "doctor_visits_target": 50
}

SALARY ENDPOINTS

1. Get Salary Slips
GET /salary/slips


2. Get Specific Salary Slip
GET /salary/slips/{slip_id}


3. Get Salary for Month
GET /salary/slips/{month}/{year}
Example: GET /salary/slips/January/2024

NOTIFICATION ENDPOINTS

1. Get Notifications
GET /notifications


2. Get Unread Notifications
GET /notifications/unread


3. Mark as Read
PUT /notifications/{notification_id}/read
Request:
{
    "is_read": true
}


4. Mark All as Read
POST /notifications/mark-all-read

PROFILE ENDPOINTS

1. Get Profile
GET /profile


2. Update Profile
PUT /profile
Request:
{
    "full_name": "John Updated",
    "phone": "+919876543211",
    "emergency_contact_name": "Jane Doe",
    "emergency_contact_phone": "+919876543212"
}

ADMIN ENDPOINTS

1. Get All Users
GET /admin/users?skip=0&limit=100


2. Get User Details
GET /admin/users/{user_id}


3. Get All Attendance
GET /admin/attendance


4. Get User Attendance
GET /admin/attendance/{user_id}


5. Get All Doctors
GET /admin/doctors


6. Get All Chemists
GET /admin/chemists


7. Get All Distributors
GET /admin/distributors


8. Get Pending Orders
GET /admin/pending-orders


9. Get Pending Leaves
GET /admin/pending-leaves


10. Get Dashboard Statistics
GET /admin/dashboard/stats

ERROR RESPONSES

All errors return standard error format:
{
    "detail": "Error message",
    "error_code": "ERROR_CODE"
}

Common HTTP Status Codes:
- 200: OK
- 201: Created
- 204: No Content
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error
