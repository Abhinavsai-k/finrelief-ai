from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Loan
from app.models.schemas import LoanCreate, LoanUpdate

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


# ==========================
# Create Loan
# ==========================
@router.post("/")
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    new_loan = Loan(
        user_id=loan.user_id,
        loan_type=loan.loan_type,
        lender=loan.lender,
        amount=loan.amount,
        interest_rate=loan.interest_rate,
        tenure=loan.tenure,
        emi=loan.emi,
        overdue_months=loan.overdue_months,
        remaining_balance=loan.remaining_balance,
        status=loan.status
    )

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    return {
        "message": "Loan created successfully",
        "loan_id": new_loan.id
    }


# ==========================
# Get All Loans
# ==========================
@router.get("/")
def get_loans(db: Session = Depends(get_db)):
    return db.query(Loan).all()


# ==========================
# Get Loan By ID
# ==========================
@router.get("/{loan_id}")
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan not found"
        )

    return loan


# ==========================
# Update Loan
# ==========================
@router.put("/{loan_id}")
def update_loan(
    loan_id: int,
    updated_loan: LoanUpdate,
    db: Session = Depends(get_db)
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan not found"
        )

    loan.loan_type = updated_loan.loan_type
    loan.lender = updated_loan.lender
    loan.amount = updated_loan.amount
    loan.interest_rate = updated_loan.interest_rate
    loan.tenure = updated_loan.tenure
    loan.emi = updated_loan.emi
    loan.overdue_months = updated_loan.overdue_months
    loan.remaining_balance = updated_loan.remaining_balance
    loan.status = updated_loan.status

    db.commit()
    db.refresh(loan)

    return {
        "message": "Loan updated successfully",
        "loan": loan
    }


# ==========================
# Delete Loan
# ==========================
@router.delete("/{loan_id}")
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan not found"
        )

    db.delete(loan)
    db.commit()

    return {
        "message": "Loan deleted successfully"
    }