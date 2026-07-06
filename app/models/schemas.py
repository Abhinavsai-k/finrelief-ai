from pydantic import BaseModel, EmailStr


# ==================================================
# User Schemas
# ==================================================
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    password: str


# ==================================================
# Loan Schemas
# ==================================================
class LoanCreate(BaseModel):
    user_id: int
    loan_type: str
    lender: str
    amount: float
    interest_rate: float
    tenure: int
    emi: float
    overdue_months: int = 0
    remaining_balance: float
    status: str


class LoanUpdate(BaseModel):
    loan_type: str
    lender: str
    amount: float
    interest_rate: float
    tenure: int
    emi: float
    overdue_months: int = 0
    remaining_balance: float
    status: str


# ==================================================
# Financial Profile Schemas
# ==================================================
class FinancialProfileCreate(BaseModel):
    user_id: int
    monthly_income: float
    monthly_expenses: float
    savings: float
    employment_type: str
    credit_score: int
    dependents: int


class FinancialProfileUpdate(BaseModel):
    monthly_income: float
    monthly_expenses: float
    savings: float
    employment_type: str
    credit_score: int
    dependents: int


# ==================================================
# Settlement Schemas
# ==================================================
class SettlementCreate(BaseModel):
    loan_id: int
    settlement_percentage: float
    predicted_amount: float
    eligibility: str
    status: str


class SettlementUpdate(BaseModel):
    settlement_percentage: float
    predicted_amount: float
    eligibility: str
    status: str


# ==================================================
# Financial Engine Schema
# ==================================================
class FinancialAnalysisRequest(BaseModel):
    user_id: int
   
 # ==================================================
# AI Negotiation Schema
# ==================================================

class AINegotiationRequest(BaseModel):
    user_id: int
    loan_id: int


 # ==================================================
# Login Schema
# ==================================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str