from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.database.database import Base, engine
from app.database.models import (
    User,
    Loan,
    FinancialProfile,
    Settlement,
)

from app.api.users import router as user_router
from app.api.loans import router as loan_router
from app.api.financial_profile import router as financial_profile_router
from app.api.settlement import router as settlement_router
from app.api.financial_engine import router as financial_engine_router
from app.api.ai_negotiation import router as ai_negotiation_router
from app.api.auth import router as auth_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinRelief AI API",
    description="AI Powered Debt Relief & Financial Recovery Platform",
    version="1.0.0",
)

# ==========================
# CORS Configuration
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Welcome to FinRelief AI 🚀"
    }


# Register API Routers
app.include_router(user_router)
app.include_router(loan_router)
app.include_router(financial_profile_router)
app.include_router(settlement_router)
app.include_router(financial_engine_router)
app.include_router(ai_negotiation_router)
app.include_router(auth_router)