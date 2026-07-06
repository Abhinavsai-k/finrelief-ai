from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth_dependency import get_current_user
from app.database.database import get_db
from app.models.schemas import FinancialAnalysisRequest
from app.services.financial_engine import analyze_finances

router = APIRouter(
    prefix="/financial-engine",
    tags=["Financial Engine"]
)


@router.post("/analyze")
def financial_analysis(
    request: FinancialAnalysisRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return analyze_finances(
        user_id=request.user_id,
        db=db
    )