from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_dependency import get_current_user
from app.database.database import get_db
from app.database.models import FinancialProfile, Loan
from app.models.schemas import AINegotiationRequest

from app.services.ai_negotiation import (
    generate_negotiation_strategy,
    generate_ai_letter
)

router = APIRouter(
    prefix="/ai-negotiation",
    tags=["AI Negotiation"]
)


# ==================================================
# Generate AI Negotiation Strategy
# ==================================================

@router.post("/generate")
def generate_strategy(
    request: AINegotiationRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    profile = (
        db.query(FinancialProfile)
        .filter(FinancialProfile.user_id == request.user_id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Financial profile not found."
        )

    loans = (
        db.query(Loan)
        .filter(Loan.user_id == request.user_id)
        .all()
    )

    if not loans:
        raise HTTPException(
            status_code=404,
            detail="No loans found."
        )

    return generate_negotiation_strategy(
        profile,
        loans
    )


# ==================================================
# Generate AI Negotiation Letter
# ==================================================

@router.post("/letter")
def generate_letter(
    request: AINegotiationRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    profile = (
        db.query(FinancialProfile)
        .filter(FinancialProfile.user_id == request.user_id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Financial profile not found."
        )

    loan = (
        db.query(Loan)
        .filter(
            Loan.id == request.loan_id,
            Loan.user_id == request.user_id
        )
        .first()
    )

    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan not found."
        )

    letter = generate_ai_letter(
        profile,
        loan
    )

    return {
        "success": True,
        "letter": letter
    }