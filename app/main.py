from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.routes import (
    auth, attendance, doctors, chemists, distributors,
    dcr, orders, leaves, targets, salary, notifications, profile, admin
)

init_db()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="MR & ASM Reporting Application Backend API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.ALLOWED_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*"]
)

app.include_router(auth.router)
app.include_router(attendance.router)
app.include_router(doctors.router)
app.include_router(chemists.router)
app.include_router(distributors.router)
app.include_router(dcr.router)
app.include_router(orders.router)
app.include_router(leaves.router)
app.include_router(targets.router)
app.include_router(salary.router)
app.include_router(notifications.router)
app.include_router(profile.router)
app.include_router(admin.router)


@app.get("/", tags=["Health"])
def read_root():
    return {
        "status": "healthy",
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "database": "connected"
    }


@app.get("/api/v1", tags=["Health"])
def api_status():
    return {
        "api": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG
    )