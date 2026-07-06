from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import FinancialProfile
from app.models.schemas import (
    FinancialProfileCreate,
    FinancialProfileUpdate
)

router = APIRouter(
    prefix="/financial-profile",
    tags=["Financial Profile"]
)


# ==========================
# Create Financial Profile
# ==========================
@router.post("/")
def create_financial_profile(
    profile: FinancialProfileCreate,
    db: Session = Depends(get_db)
):

    new_profile = FinancialProfile(
        user_id=profile.user_id,
        monthly_income=profile.monthly_income,
        monthly_expenses=profile.monthly_expenses,
        savings=profile.savings,
        employment_type=profile.employment_type,
        credit_score=profile.credit_score,
        dependents=profile.dependents
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return {
        "message": "Financial Profile created successfully",
        "profile_id": new_profile.id
    }


# ==========================
# Get All Profiles
# ==========================
@router.get("/")
def get_profiles(db: Session = Depends(get_db)):
    return db.query(FinancialProfile).all()


# ==========================
# Get Profile By User ID
# ==========================
@router.get("/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)):

    profile = (
        db.query(FinancialProfile)
        .filter(FinancialProfile.user_id == user_id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Financial Profile not found"
        )

    return profile


# ==========================
# Update Profile
# ==========================
@router.put("/{user_id}")
def update_profile(
    user_id: int,
    updated_profile: FinancialProfileUpdate,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(FinancialProfile)
        .filter(FinancialProfile.user_id == user_id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Financial Profile not found"
        )

    profile.monthly_income = updated_profile.monthly_income
    profile.monthly_expenses = updated_profile.monthly_expenses
    profile.savings = updated_profile.savings
    profile.employment_type = updated_profile.employment_type
    profile.credit_score = updated_profile.credit_score
    profile.dependents = updated_profile.dependents

    db.commit()
    db.refresh(profile)

    return {
        "message": "Financial Profile updated successfully",
        "profile": profile
    }


# ==========================
# Delete Profile
# ==========================
@router.delete("/{user_id}")
def delete_profile(
    user_id: int,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(FinancialProfile)
        .filter(FinancialProfile.user_id == user_id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Financial Profile not found"
        )

    db.delete(profile)
    db.commit()

    return {
        "message": "Financial Profile deleted successfully"
    }