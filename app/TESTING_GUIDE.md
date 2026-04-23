# Test Cases for MR & ASM Reporting Application

## Prerequisites
- Backend running on http://localhost:8000
- PostgreSQL database configured
- Postman or similar API client

## 1. Authentication Tests

### Test 1.1: User Registration
```
POST /api/v1/auth/register
Content-Type: application/json

{
    "employee_id": "MR001",
    "email": "mr.john@company.com",
    "full_name": "John Doe",
    "phone": "+919876543210",
    "role": "MR",
    "assigned_area": "Mumbai",
    "password": "SecurePass@123"
}

Expected: 201 Created
```

### Test 1.2: Login
```
POST /api/v1/auth/login
Content-Type: application/json

{
    "email": "mr.john@company.com",
    "password": "SecurePass@123"
}

Expected: 200 OK
Response includes: access_token, refresh_token
```

### Test 1.3: Duplicate Email Registration
```
Same as Test 1.1 with same email

Expected: 400 Bad Request
Message: "Email already registered"
```

### Test 1.4: Invalid Credentials
```
POST /api/v1/auth/login
{
    "email": "mr.john@company.com",
    "password": "WrongPassword"
}

Expected: 401 Unauthorized
```

## 2. Attendance Tests

### Test 2.1: Check-In
```
POST /api/v1/attendance/check-in
Authorization: Bearer {access_token}

{
    "latitude": "19.0760",
    "longitude": "72.8777",
    "selfie_url": "https://example.com/selfie.jpg"
}

Expected: 201 Created
```

### Test 2.2: Check-Out
```
POST /api/v1/attendance/check-out
Authorization: Bearer {access_token}

{
    "latitude": "19.0761",
    "longitude": "72.8778",
    "selfie_url": "https://example.com/selfie_out.jpg"
}

Expected: 200 OK
```

### Test 2.3: Get Today's Attendance
```
GET /api/v1/attendance/today
Authorization: Bearer {access_token}

Expected: 200 OK
Response: Attendance record with check-in and check-out times
```

### Test 2.4: Double Check-In
```
POST /api/v1/attendance/check-in (immediately after first check-in)

Expected: 400 Bad Request
Message: "Already checked in today"
```

## 3. Doctor Network Tests

### Test 3.1: Add Doctor
```
POST /api/v1/doctors
Authorization: Bearer {access_token}

{
    "name": "Dr. Rajesh Kumar",
    "email": "dr.rajesh@hospital.com",
    "phone": "+919876543210",
    "specialization": "Cardiology",
    "registration_number": "MCI-12345",
    "clinic_name": "Heart Care Hospital",
    "clinic_address": "123 Medical Lane, Mumbai",
    "clinic_latitude": "19.0760",
    "clinic_longitude": "72.8777"
}

Expected: 201 Created
```

### Test 3.2: List Doctors
```
GET /api/v1/doctors
Authorization: Bearer {access_token}

Expected: 200 OK
Response: Array of doctor objects
```

### Test 3.3: Update Doctor
```
PUT /api/v1/doctors/{doctor_id}
Authorization: Bearer {access_token}

{
    "name": "Dr. Rajesh Kumar Updated"
}

Expected: 200 OK
```

### Test 3.4: Delete Doctor
```
DELETE /api/v1/doctors/{doctor_id}
Authorization: Bearer {access_token}

Expected: 204 No Content
```

## 4. Chemist Tests

### Test 4.1: Add Chemist
```
POST /api/v1/chemists
Authorization: Bearer {access_token}

{
    "shop_name": "Pharmacy Plus",
    "owner_name": "Mr. Patel",
    "phone": "+919876543210",
    "email": "contact@pharmacyplus.com",
    "address": "456 Retail Street, Mumbai",
    "latitude": "19.0761",
    "longitude": "72.8778",
    "gst_number": "27AABCT1234F1Z0"
}

Expected: 201 Created
```

### Test 4.2: List Chemists
```
GET /api/v1/chemists
Authorization: Bearer {access_token}

Expected: 200 OK
```

## 5. DCR (Doctor Call Report) Tests

### Test 5.1: Create DCR
```
POST /api/v1/dcr
Authorization: Bearer {access_token}

{
    "doctor_id": 1,
    "products_discussed": "Aspirin 500mg, New Cardio Formula",
    "remarks": "Doctor showed interest in new product",
    "visual_aid_presented": true,
    "visual_aid_url": "https://example.com/visual_aid.pdf"
}

Expected: 201 Created
Doctor visit_frequency should increment
```

### Test 5.2: List DCRs
```
GET /api/v1/dcr
Authorization: Bearer {access_token}

Expected: 200 OK
```

## 6. Order Tests

### Test 6.1: Create Order
```
POST /api/v1/orders
Authorization: Bearer {access_token}

{
    "product_details": "Aspirin 500mg - 100 tablets",
    "quantity": 500,
    "order_notes": "Urgent delivery"
}

Expected: 201 Created
Status: "pending"
```

### Test 6.2: Admin Approve Order
```
POST /api/v1/orders/{order_id}/approve
Authorization: Bearer {admin_token}

{
    "approved": true,
    "rejection_reason": null
}

Expected: 200 OK
Status changed to: "approved"
```

### Test 6.3: Admin Reject Order
```
POST /api/v1/orders/{order_id}/approve
Authorization: Bearer {admin_token}

{
    "approved": false,
    "rejection_reason": "Out of stock"
}

Expected: 200 OK
Status changed to: "rejected"
```

## 7. Leave Tests

### Test 7.1: Apply Leave
```
POST /api/v1/leaves
Authorization: Bearer {access_token}

{
    "leave_type": "sick",
    "start_date": "2024-01-20T00:00:00",
    "end_date": "2024-01-22T00:00:00",
    "reason": "Medical treatment"
}

Expected: 201 Created
Status: "pending"
```

### Test 7.2: Admin Approve Leave
```
POST /api/v1/leaves/{leave_id}/approve
Authorization: Bearer {admin_token}

{
    "approved": true,
    "rejection_reason": null
}

Expected: 200 OK
```

## 8. Target Tests

### Test 8.1: Get Targets
```
GET /api/v1/targets
Authorization: Bearer {access_token}

Expected: 200 OK
```

## 9. Profile Tests

### Test 9.1: Get Profile
```
GET /api/v1/profile
Authorization: Bearer {access_token}

Expected: 200 OK
```

### Test 9.2: Update Profile
```
PUT /api/v1/profile
Authorization: Bearer {access_token}

{
    "full_name": "John Doe Updated",
    "phone": "+919876543211",
    "emergency_contact_name": "Jane Doe",
    "emergency_contact_phone": "+919876543212"
}

Expected: 200 OK
```

## 10. Admin Tests

### Test 10.1: Get All Users
```
GET /api/v1/admin/users
Authorization: Bearer {admin_token}

Expected: 200 OK
```

### Test 10.2: Get Dashboard Stats
```
GET /api/v1/admin/dashboard/stats
Authorization: Bearer {admin_token}

Expected: 200 OK
Response includes: user counts, doctor counts, order counts, etc.
```

## 11. Error Handling Tests

### Test 11.1: Invalid Token
```
GET /api/v1/profile
Authorization: Bearer invalid_token

Expected: 401 Unauthorized
```

### Test 11.2: Missing Authorization
```
GET /api/v1/profile

Expected: 403 Forbidden
```

### Test 11.3: Invalid Request Body
```
POST /api/v1/auth/register
{
    "email": "not-a-valid-email",
    "password": "123"  // too short
}

Expected: 422 Unprocessable Entity
```

## Test Execution Script

```bash
#!/bin/bash

BASE_URL="http://localhost:8000/api/v1"

# Register
REGISTER=$(curl -X POST $BASE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id":"TEST001",
    "email":"test@example.com",
    "full_name":"Test User",
    "password":"Test@1234",
    "role":"MR"
  }')

echo "Registration: $REGISTER"

# Login
LOGIN=$(curl -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "password":"Test@1234"
  }')

echo "Login: $LOGIN"

# Extract token
TOKEN=$(echo $LOGIN | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo "Token: $TOKEN"

# Check-in
curl -X POST $BASE_URL/attendance/check-in \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude":"19.0760",
    "longitude":"72.8777"
  }'
```

## Performance Testing

For load testing, use Apache JMeter or similar tools:

```
Thread Group: 10 threads
Ramp-up: 60 seconds
Loop: 100

Test Cases:
- Login: 20%
- Check-in: 30%
- Add Doctor: 10%
- Create Order: 20%
- View Profile: 20%
```

Expected response times:
- Login: < 500ms
- Check-in: < 300ms
- List operations: < 1000ms

## Conclusion

All test cases should pass when properly configured.
For debugging, check:
- Database connection
- JWT token expiration
- Timestamp formats
- Request validation
