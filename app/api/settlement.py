from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_dependency import get_current_user
from app.database.database import get_db
from app.database.models import Settlement, Loan, FinancialProfile
from app.models.schemas import SettlementCreate, SettlementUpdate
from app.services.settlement_engine import analyze_portfolio_settlement

router = APIRouter(
    prefix="/settlement",
    tags=["Settlement"]
)


# ==========================
# Create Settlement
# ==========================
@router.post("/")
def create_settlement(
    settlement: SettlementCreate,
    db: Session = Depends(get_db)
):

    new_settlement = Settlement(
        loan_id=settlement.loan_id,
        settlement_percentage=settlement.settlement_percentage,
        predicted_amount=settlement.predicted_amount,
        eligibility=settlement.eligibility,
        status=settlement.status
    )

    db.add(new_settlement)
    db.commit()
    db.refresh(new_settlement)

    return {
        "message": "Settlement created successfully",
        "settlement_id": new_settlement.id
    }


# ==========================
# Get All Settlements
# ==========================
@router.get("/")
def get_settlements(
    db: Session = Depends(get_db)
):
    return db.query(Settlement).all()


# ==========================
# Get Settlement By ID
# ==========================
@router.get("/{settlement_id}")
def get_settlement(
    settlement_id: int,
    db: Session = Depends(get_db)
):

    settlement = (
        db.query(Settlement)
        .filter(Settlement.id == settlement_id)
        .first()
    )

    if settlement is None:
        raise HTTPException(
            status_code=404,
            detail="Settlement not found"
        )

    return settlement


# ==========================
# Update Settlement
# ==========================
@router.put("/{settlement_id}")
def update_settlement(
    settlement_id: int,
    updated_settlement: SettlementUpdate,
    db: Session = Depends(get_db)
):

    settlement = (
        db.query(Settlement)
        .filter(Settlement.id == settlement_id)
        .first()
    )

    if settlement is None:
        raise HTTPException(
            status_code=404,
            detail="Settlement not found"
        )

    settlement.settlement_percentage = updated_settlement.settlement_percentage
    settlement.predicted_amount = updated_settlement.predicted_amount
    settlement.eligibility = updated_settlement.eligibility
    settlement.status = updated_settlement.status

    db.commit()
    db.refresh(settlement)

    return {
        "message": "Settlement updated successfully",
        "settlement": settlement
    }


# ==========================
# Delete Settlement
# ==========================
@router.delete("/{settlement_id}")
def delete_settlement(
    settlement_id: int,
    db: Session = Depends(get_db)
):

    settlement = (
        db.query(Settlement)
        .filter(Settlement.id == settlement_id)
        .first()
    )

    if settlement is None:
        raise HTTPException(
            status_code=404,
            detail="Settlement not found"
        )

    db.delete(settlement)
    db.commit()

    return {
        "message": "Settlement deleted successfully"
    }


# ==================================================
# Settlement Prediction Engine
# ==================================================
@router.get("/analysis/{user_id}")
def settlement_analysis(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    profile = (
        db.query(FinancialProfile)
        .filter(FinancialProfile.user_id == user_id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Financial profile not found."
        )

    loans = (
        db.query(Loan)
        .filter(Loan.user_id == user_id)
        .all()
    )

    if not loans:
        raise HTTPException(
            status_code=404,
            detail="No loans found."
        )

    results = analyze_portfolio_settlement(
        loans,
        profile.credit_score
    )

    return {
        "success": True,
        "user_id": user_id,
        "total_loans": len(loans),
        "settlement_analysis": results
    }