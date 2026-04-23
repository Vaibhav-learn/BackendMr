# MR & ASM Reporting Application - Backend

## Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip

## Installation

### 1. Clone Repository
\`\`\`bash
git clone <repo-url>
cd BackendMr
\`\`\`

### 2. Create Virtual Environment
\`\`\`bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Setup Environment Variables
Create a `.env` file in the root directory:
\`\`\`
DATABASE_URL=postgresql://postgres:Vaibhav%4014@localhost:54321/Vaibhav
SECRET_KEY=your-super-secret-key-here
DEBUG=True
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
\`\`\`

### 5. Initialize Database
\`\`\`bash
alembic upgrade head
\`\`\`

## Running the Application

### Development Server
\`\`\`bash
python -m uvicorn app.main:app --reload
\`\`\`

The API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

## Project Structure
\`\`\`
app/
├── core/              # Core configuration, DB, security
├── models/            # SQLAlchemy ORM models
├── schemas/           # Pydantic schemas for validation
├── services/          # Business logic layer
├── routes/            # API endpoints
├── utils/             # Helper functions
└── main.py           # Application entry point
\`\`\`

## API Endpoints

### Authentication
- POST `/api/v1/auth/register` - Register new user
- POST `/api/v1/auth/login` - Login user
- POST `/api/v1/auth/refresh` - Refresh token
- POST `/api/v1/auth/change-password` - Change password

### Attendance
- POST `/api/v1/attendance/check-in` - Check-in
- POST `/api/v1/attendance/check-out` - Check-out
- GET `/api/v1/attendance/today` - Get today's attendance
- GET `/api/v1/attendance/history` - Get attendance history

### Doctors
- POST `/api/v1/doctors` - Create doctor
- GET `/api/v1/doctors` - List doctors
- GET `/api/v1/doctors/{id}` - Get doctor details
- PUT `/api/v1/doctors/{id}` - Update doctor
- DELETE `/api/v1/doctors/{id}` - Delete doctor

### Chemists
- POST `/api/v1/chemists` - Create chemist
- GET `/api/v1/chemists` - List chemists

### Distributors
- POST `/api/v1/distributors` - Create distributor
- GET `/api/v1/distributors` - List distributors

## Database Setup

### PostgreSQL Installation

**Windows:**
1. Download from https://www.postgresql.org/download/windows/
2. Run installer and follow setup wizard
3. Note down the password for postgres user

**macOS:**
\`\`\`bash
brew install postgresql@14
\`\`\`

**Linux (Ubuntu):**
\`\`\`bash
sudo apt-get install postgresql postgresql-contrib
\`\`\`

### Create Database
\`\`\`bash
# Database 'Vaibhav' should already exist from PHARMA-BACKEND-CORE setup
# Connect with: psql -U postgres -h localhost -p 54321
\`\`\`

## Technologies

- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL
- **Authentication:** JWT
- **Validation:** Pydantic
- **Password Hashing:** Bcrypt

## Security Notes

- Always use strong SECRET_KEY in production
- Never commit .env file
- Use HTTPS in production
- Implement proper CORS policy
- Validate all user inputs
- Use environment variables for sensitive data

## Contributing

1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## Support

For issues or questions, please contact the development team.
