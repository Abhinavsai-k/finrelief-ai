"""
==================================================
FinRelief AI Financial Engine
Story 2 - Part 1
==================================================
"""

from sqlalchemy.orm import Session
from app.database.models import Loan, FinancialProfile


# ==================================================
# Portfolio Calculations
# ==================================================

def calculate_total_emi(loans):
    return round(sum(loan.emi for loan in loans), 2)


def calculate_total_outstanding(loans):
    return round(sum(loan.remaining_balance for loan in loans), 2)


def calculate_average_interest(loans):
    if not loans:
        return 0

    return round(
        sum(loan.interest_rate for loan in loans) / len(loans),
        2
    )


# ==================================================
# Financial Metrics
# ==================================================

def calculate_emi_ratio(
    monthly_income: float,
    total_emi: float
):

    if monthly_income <= 0:
        return 0

    return round(
        (total_emi / monthly_income) * 100,
        2
    )


def calculate_dti(
    monthly_income: float,
    total_emi: float
):

    if monthly_income <= 0:
        return 0

    return round(
        (total_emi / monthly_income) * 100,
        2
    )


def calculate_monthly_surplus(
    monthly_income: float,
    monthly_expenses: float,
    total_emi: float
):

    return round(
        monthly_income
        - monthly_expenses
        - total_emi,
        2
    )


# ==================================================
# Financial Stress Engine
# ==================================================

def calculate_financial_stress(
    emi_ratio,
    monthly_surplus
):

    if monthly_surplus <= 0:
        return "High"

    if emi_ratio >= 60:
        return "High"

    if emi_ratio >= 40:
        return "Medium"

    return "Low"


# ==================================================
# Financial Score
# ==================================================

def calculate_financial_score(
    emi_ratio,
    savings,
    credit_score
):

    score = 100

    if emi_ratio >= 60:
        score -= 40

    elif emi_ratio >= 40:
        score -= 25

    elif emi_ratio >= 20:
        score -= 10

    if savings >= 200000:
        score += 10

    elif savings >= 100000:
        score += 5

    if credit_score >= 750:
        score += 10

    elif credit_score < 600:
        score -= 15

    return max(0, min(score, 100))

# ==================================================
# Loan Priority Analysis
# ==================================================

def calculate_priority_score(loan):
    """
    Calculates a priority score for a loan based on:
    - Overdue Months (40%)
    - Interest Rate (30%)
    - EMI Burden (30%)
    """

    score = 0

    # Overdue Duration
    if loan.overdue_months >= 12:
        score += 40
    elif loan.overdue_months >= 6:
        score += 30
    elif loan.overdue_months >= 3:
        score += 20
    elif loan.overdue_months > 0:
        score += 10

    # Interest Rate
    if loan.interest_rate >= 20:
        score += 30
    elif loan.interest_rate >= 15:
        score += 20
    elif loan.interest_rate >= 10:
        score += 10

    # EMI Burden
    if loan.emi >= 30000:
        score += 30
    elif loan.emi >= 15000:
        score += 20
    elif loan.emi >= 5000:
        score += 10

    return score


# ==================================================
# Loan Priority Classification
# ==================================================

def classify_priority(score):

    if score >= 70:
        return "High"

    if score >= 40:
        return "Medium"

    return "Low"


# ==================================================
# Priority Based Loan Sorting
# ==================================================

def prioritize_loans(loans):

    prioritized = []

    for loan in loans:

        score = calculate_priority_score(loan)

        prioritized.append({
            "loan_id": loan.id,
            "loan_type": loan.loan_type,
            "lender": loan.lender,
            "remaining_balance": loan.remaining_balance,
            "interest_rate": loan.interest_rate,
            "emi": loan.emi,
            "overdue_months": loan.overdue_months,
            "priority_score": score,
            "priority": classify_priority(score)
        })

    prioritized.sort(
        key=lambda loan: loan["priority_score"],
        reverse=True
    )

    return prioritized


# ==================================================
# Debt Repayment Timeline Simulation
# ==================================================

def simulate_repayment(loans):

    timeline = []

    for loan in loans:

        balance = loan.remaining_balance
        month = 0

        while balance > 0 and month < 240:

            month += 1
            balance -= loan.emi

            if balance < 0:
                balance = 0

        timeline.append({
            "loan_id": loan.id,
            "loan_type": loan.loan_type,
            "months_to_close": month
        })

    return timeline


# ==================================================
# Settlement Recommendation
# ==================================================

def settlement_eligibility(financial_score, financial_stress):

    if financial_stress == "High" or financial_score <= 40:
        return "Eligible"

    if financial_stress == "Medium":
        return "Review Required"

    return "Not Eligible"


def estimated_settlement(total_outstanding, eligibility):

    if eligibility == "Eligible":
        percentage = 0.45

    elif eligibility == "Review Required":
        percentage = 0.60

    else:
        percentage = 1.00

    return round(total_outstanding * percentage, 2)


def recommendation(financial_score):

    if financial_score >= 80:
        return "Continue regular EMI payments."

    if financial_score >= 60:
        return "Reduce monthly expenses and increase savings."

    if financial_score >= 40:
        return "Consider loan restructuring."

    return "Debt settlement is recommended."


# ==================================================
# Main Financial Analysis
# ==================================================

def analyze_finances(user_id: int, db: Session):

    # ------------------------------------------
    # Fetch Financial Profile
    # ------------------------------------------
    profile = (
        db.query(FinancialProfile)
        .filter(FinancialProfile.user_id == user_id)
        .first()
    )

    if profile is None:
        return {
            "success": False,
            "message": "Financial Profile not found."
        }

    # ------------------------------------------
    # Fetch User Loans
    # ------------------------------------------
    loans = (
        db.query(Loan)
        .filter(Loan.user_id == user_id)
        .all()
    )

    if not loans:
        return {
            "success": False,
            "message": "No loans found."
        }

    # ------------------------------------------
    # Portfolio Calculations
    # ------------------------------------------
    total_emi = calculate_total_emi(loans)

    total_outstanding = calculate_total_outstanding(loans)

    average_interest = calculate_average_interest(loans)

    emi_ratio = calculate_emi_ratio(
        profile.monthly_income,
        total_emi
    )

    dti = calculate_dti(
        profile.monthly_income,
        total_emi
    )

    monthly_surplus = calculate_monthly_surplus(
        profile.monthly_income,
        profile.monthly_expenses,
        total_emi
    )

    financial_stress = calculate_financial_stress(
        emi_ratio,
        monthly_surplus
    )

    financial_score = calculate_financial_score(
        emi_ratio,
        profile.savings,
        profile.credit_score
    )

    eligibility = settlement_eligibility(
        financial_score,
        financial_stress
    )

    settlement_amount = estimated_settlement(
        total_outstanding,
        eligibility
    )

    loan_priority = prioritize_loans(loans)

    repayment_timeline = simulate_repayment(loans)

    advice = recommendation(financial_score)

    return {

        "success": True,

        "financial_score": financial_score,

        "financial_stress_level": financial_stress,

        "monthly_income": profile.monthly_income,

        "monthly_expenses": profile.monthly_expenses,

        "monthly_surplus": monthly_surplus,

        "total_emi": total_emi,

        "debt_to_income_ratio": dti,

        "emi_to_income_ratio": emi_ratio,

        "total_outstanding_debt": total_outstanding,

        "average_interest_rate": average_interest,

        "settlement_eligibility": eligibility,

        "estimated_settlement_amount": settlement_amount,

        "recommendation": advice,

        "loan_priority_analysis": loan_priority,

        "repayment_timeline": repayment_timeline
    }