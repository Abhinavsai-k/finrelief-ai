"""
==================================================
FinRelief AI Settlement Prediction Engine
==================================================
"""


# ==================================================
# Risk Category
# ==================================================

def calculate_risk_category(
    financial_score: int,
    overdue_months: int
):

    if financial_score < 40 or overdue_months >= 6:
        return "High"

    if financial_score < 70 or overdue_months >= 3:
        return "Medium"

    return "Low"


# ==================================================
# Settlement Percentage Prediction
# ==================================================

def predict_settlement_percentage(
    risk_category: str,
    loan_type: str
):

    base_percentage = 100

    if risk_category == "High":
        base_percentage = 45

    elif risk_category == "Medium":
        base_percentage = 60

    else:
        base_percentage = 85

    # Loan Type Adjustment
    if loan_type.lower() == "credit card":
        base_percentage -= 5

    elif loan_type.lower() == "personal":
        base_percentage -= 3

    return max(base_percentage, 35)


# ==================================================
# Settlement Amount
# ==================================================

def predict_settlement_amount(
    remaining_balance: float,
    settlement_percentage: float
):

    return round(
        remaining_balance * (settlement_percentage / 100),
        2
    )

# ==================================================
# Settlement Confidence
# ==================================================

def settlement_confidence(
    financial_score: int,
    overdue_months: int,
    risk_category: str
):

    confidence = 50

    if financial_score < 40:
        confidence += 20

    elif financial_score < 60:
        confidence += 10

    if overdue_months >= 6:
        confidence += 20

    elif overdue_months >= 3:
        confidence += 10

    if risk_category == "High":
        confidence += 10

    return min(confidence, 100)


# ==================================================
# Negotiation Window
# ==================================================

def negotiation_window(overdue_months: int):

    if overdue_months >= 6:
        return "Immediate"

    if overdue_months >= 3:
        return "Within 30 Days"

    return "Continue Regular Payments"


# ==================================================
# Recommendation Reason
# ==================================================

def recommendation_reason(
    financial_score: int,
    overdue_months: int,
    risk_category: str
):

    # Highest priority
    if risk_category == "High":
        return (
            "Immediate settlement negotiation is recommended "
            "to reduce financial risk."
        )

    # Medium priority
    if risk_category == "Medium":
        return (
            "Borrower should negotiate with the lender "
            "within the next 30 days."
        )

    # Financial weakness
    if financial_score < 40:
        return (
            "Borrower's financial health is weak. "
            "Settlement may prevent further defaults."
        )

    # Mild overdue
    if overdue_months >= 3:
        return (
            "Monitor repayments closely and prepare "
            "for possible negotiation."
        )

    # Healthy borrower
    return (
        "Continue regular repayments."
    )
# ==================================================
# Settlement Analysis
# ==================================================

def analyze_settlement(
    loan,
    financial_score: int
):
    """
    Analyze a single loan and generate
    settlement prediction.
    """

    risk_category = calculate_risk_category(
        financial_score,
        loan.overdue_months
    )

    settlement_percentage = predict_settlement_percentage(
        risk_category,
        loan.loan_type
    )

    settlement_amount = predict_settlement_amount(
        loan.remaining_balance,
        settlement_percentage
    )

    confidence = settlement_confidence(
        financial_score,
        loan.overdue_months,
        risk_category
    )

    window = negotiation_window(
        loan.overdue_months
    )

    reason = recommendation_reason(
    financial_score,
    loan.overdue_months,
    risk_category
)

    return {
        "loan_id": loan.id,
        "loan_type": loan.loan_type,
        "lender": loan.lender,
        "remaining_balance": loan.remaining_balance,
        "overdue_months": loan.overdue_months,
        "risk_category": risk_category,
        "settlement_percentage": settlement_percentage,
        "predicted_settlement_amount": settlement_amount,
        "settlement_confidence": confidence,
        "negotiation_window": window,
        "recommendation_reason": reason
    }


# ==================================================
# Portfolio Settlement Analysis
# ==================================================

def analyze_portfolio_settlement(
    loans,
    financial_score: int
):
    """
    Analyze all loans of a borrower.
    """

    results = []

    for loan in loans:
        results.append(
            analyze_settlement(
                loan,
                financial_score
            )
        )

    return results