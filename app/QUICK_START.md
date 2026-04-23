# ⚡ QUICK START - MR & ASM Reporting App Backend

## 🚀 Getting Started in 5 Minutes

### Step 1: Setup Virtual Environment (Windows)
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 1: Setup Virtual Environment (macOS/Linux)
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Database
```bash
# .env file is already configured with PHARMA database
DATABASE_URL=postgresql://postgres:Vaibhav%4014@localhost:54321/Vaibhav
```

### Step 4: Using Existing Database
```bash
# Database 'Vaibhav' already exists from PHARMA-BACKEND-CORE
# No database creation needed
```

### Step 5: Initialize Tables
```bash
python -c "from app.core.database import init_db; init_db()"
```

### Step 6: Run Server
```bash
python -m uvicorn app.main:app --reload
```

✅ Server running at: http://localhost:8000

---

## 📚 Access Documentation

- **Swagger UI (Interactive):** http://localhost:8000/docs
- **ReDoc (Static):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 🔧 Common Commands

### Test API with cURL

```bash
# Health Check
curl http://localhost:8000/health

# Register User
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "MR001",
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "Pass@123",
    "role": "MR"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Pass@123"
  }'
```

---

## 🗄️ Database Commands

### PostgreSQL Basics

```bash
# Connect to PostgreSQL
psql -U postgres

# List databases
\l

# Connect to database
# Connect to PHARMA database on port 54321
psql -U postgres -h localhost -p 54321 -d Vaibhav

# List tables
\dt

# Describe table
\d users

# Run SQL query
SELECT * FROM users;

# Drop table
DROP TABLE users;

# Backup database
pg_dump -U postgres -h localhost -p 54321 Vaibhav > backup.sql

# Restore database
psql -U postgres -h localhost -p 54321 Vaibhav < backup.sql
```

---

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError
**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate

# Install dependencies again
pip install -r requirements.txt
```

### Issue: Database Connection Error
**Solution:**
```bash
# Check PostgreSQL is running
psql -U postgres

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://postgres:Vaibhav%4014@localhost:54321/Vaibhav

# Using existing PHARMA database 'Vaibhav'
# No database creation needed
```

### Issue: Port 8000 Already in Use
**Solution:**
```bash
# Run on different port
python -m uvicorn app.main:app --reload --port 8001

# Or kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID {PID} /F

# Or kill process on port 8000 (macOS/Linux)
lsof -i :8000
kill -9 {PID}
```

---

## 📊 Project Structure

```
BackendMr/
├── app/
│   ├── core/          # Config, DB, security
│   ├── models/        # Database models
│   ├── schemas/       # Validation schemas
│   ├── services/      # Business logic
│   ├── routes/        # API endpoints
│   ├── utils/         # Helpers
│   └── main.py        # Entry point
├── requirements.txt   # Dependencies
├── .env              # Configuration
└── README.md         # Documentation
```

---

## 📖 API Quick Reference

### Authentication
```
POST   /api/v1/auth/register          - Register
POST   /api/v1/auth/login             - Login
POST   /api/v1/auth/refresh           - Refresh token
POST   /api/v1/auth/change-password   - Change password
```

### Attendance
```
POST   /api/v1/attendance/check-in    - Check-in
POST   /api/v1/attendance/check-out   - Check-out
GET    /api/v1/attendance/today       - Today's attendance
GET    /api/v1/attendance/history     - Attendance history
```

### Doctors
```
POST   /api/v1/doctors                - Add doctor
GET    /api/v1/doctors                - List doctors
GET    /api/v1/doctors/{id}           - Doctor details
PUT    /api/v1/doctors/{id}           - Update doctor
DELETE /api/v1/doctors/{id}           - Delete doctor
```

### Chemists
```
POST   /api/v1/chemists               - Add chemist
GET    /api/v1/chemists               - List chemists
```

### Distributors
```
POST   /api/v1/distributors           - Add distributor
GET    /api/v1/distributors           - List distributors
```

### Orders
```
POST   /api/v1/orders                 - Create order
GET    /api/v1/orders                 - List orders
POST   /api/v1/orders/{id}/approve    - Approve order
```

### Leaves
```
POST   /api/v1/leaves                 - Apply leave
GET    /api/v1/leaves                 - List leaves
POST   /api/v1/leaves/{id}/approve    - Approve leave
```

### Targets
```
GET    /api/v1/targets                - List targets
GET    /api/v1/targets/{id}           - Target details
PUT    /api/v1/targets/{id}           - Update target
```

### Profile
```
GET    /api/v1/profile                - Get profile
PUT    /api/v1/profile                - Update profile
```

### Admin
```
GET    /api/v1/admin/users            - All users
GET    /api/v1/admin/dashboard/stats  - Statistics
```

---

## 💡 Tips & Tricks

### Development Mode
```bash
# Run with auto-reload
python -m uvicorn app.main:app --reload

# Run with specific log level
python -m uvicorn app.main:app --log-level debug

# Run on specific host/port
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Using Postman

1. **Import API**
   - Create new Postman collection
   - Add base URL: `http://localhost:8000/api/v1`
   - Set auth header: `Authorization: Bearer {token}`

2. **Sample Request**
   ```
   POST /auth/login
   Content-Type: application/json
   
   {
     "email": "user@example.com",
     "password": "Pass@123"
   }
   ```

3. **Use Token**
   - Copy `access_token` from login response
   - Set in Authorization header for next requests

---

## 🔍 File Locations

| File | Purpose |
|------|---------|
| `app/main.py` | Application entry point |
| `app/core/config.py` | Settings |
| `app/core/database.py` | DB setup |
| `app/models/__init__.py` | Database models |
| `app/schemas/__init__.py` | Validation schemas |
| `app/routes/` | API endpoints |
| `requirements.txt` | Dependencies |
| `.env` | Configuration |
| `README.md` | Setup guide |

---

## ✅ Verification Checklist

- [ ] Python installed (3.8+)
- [ ] Virtual environment created & activated
- [ ] Dependencies installed
- [ ] PostgreSQL running
- [ ] Database created
- [ ] .env configured
- [ ] Server running
- [ ] API docs accessible at /docs
- [ ] Health check responding

---

## 📞 Quick Help

```bash
# Check Python version
python --version

# Check PostgreSQL version
psql --version

# List installed packages
pip list

# Check virtual environment
which python  # macOS/Linux
where python  # Windows

# Update package
pip install --upgrade fastapi

# Freeze requirements
pip freeze > requirements.txt
```

---

## 🎯 Next Steps

1. ✅ Run the backend
2. ✅ Test endpoints at http://localhost:8000/docs
3. ✅ Create test user
4. ✅ Test authentication
5. ✅ Integrate with frontend

---

**Happy Coding! 🚀**

For detailed documentation, see:
- API_DOCUMENTATION.md
- README.md
- DEPLOYMENT.md
