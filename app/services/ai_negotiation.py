"""
==================================================
FinRelief AI
AI Negotiation Strategy Engine
==================================================
"""

from app.services.ai_engine import generate_ai_response


# ==================================================
# Prompt Generator
# ==================================================

def build_negotiation_prompt(profile, loans):
    """
    Builds a detailed prompt for Gemini AI.
    """

    loan_summary = ""

    for loan in loans:
        loan_summary += f"""
Loan Type: {loan.loan_type}
Lender: {loan.lender}
Outstanding Balance: ₹{loan.remaining_balance}
Interest Rate: {loan.interest_rate}%
Monthly EMI: ₹{loan.emi}
Overdue Months: {loan.overdue_months}

"""

    return f"""
You are an experienced debt settlement consultant.

Analyze the following borrower profile.

Borrower Information
--------------------
Monthly Income: ₹{profile.monthly_income}
Monthly Expenses: ₹{profile.monthly_expenses}
Savings: ₹{profile.savings}
Credit Score: {profile.credit_score}
Employment Type: {profile.employment_type}
Dependents: {profile.dependents}

Loans
------
{loan_summary}

Tasks

1. Analyze the borrower's financial situation.

2. Recommend the best debt settlement strategy.

3. Suggest the order in which loans should be negotiated.

4. Recommend an estimated settlement percentage for each loan.

5. Explain why this strategy is appropriate.

Return the answer in professional business English.
"""


# ==================================================
# Rule-Based Fallback Engine
# ==================================================

def fallback_negotiation_strategy(profile, loans):

    strategy = []

    strategy.append(f"Monthly Income: ₹{profile.monthly_income}")
    strategy.append(f"Monthly Expenses: ₹{profile.monthly_expenses}")
    strategy.append(f"Available Savings: ₹{profile.savings}")
    strategy.append("")
    strategy.append("Recommended Loan Priority:")

    sorted_loans = sorted(
        loans,
        key=lambda loan: (
            loan.overdue_months,
            loan.interest_rate
        ),
        reverse=True
    )

    for index, loan in enumerate(sorted_loans, start=1):

        strategy.append(
            f"{index}. {loan.lender} "
            f"({loan.loan_type}) "
            f"- Outstanding ₹{loan.remaining_balance}"
        )

    strategy.append("")
    strategy.append("Recommendation:")
    strategy.append("Negotiate high-interest and overdue loans first.")
    strategy.append("Maintain regular payments for lower-risk loans.")
    strategy.append("Keep communication with lenders documented.")

    return "\n".join(strategy)


# ==================================================
# AI Negotiation Strategy
# ==================================================

def generate_negotiation_strategy(profile, loans):

    prompt = build_negotiation_prompt(profile, loans)

    response = generate_ai_response(prompt)

    if response["success"]:

        return {
            "success": True,
            "source": "Google Gemini",
            "strategy": response["response"]
        }

    return {
        "success": True,
        "source": "Rule-Based Fallback",
        "strategy": fallback_negotiation_strategy(
            profile,
            loans
        )
    }


# ==================================================
# Professional Negotiation Letter
# ==================================================

def generate_negotiation_letter(
    profile,
    loan,
    strategy
):

    return f"""
Subject: Request for One-Time Settlement (OTS)

To,
The Settlement Officer,
{loan.lender}

Dear Sir/Madam,

I hope this letter finds you well.

I am writing to respectfully request your consideration for a One-Time Settlement (OTS) of my {loan.loan_type.lower()} loan.

Due to my present financial circumstances, I am facing difficulty maintaining regular EMI payments despite my sincere efforts.

Financial Summary
--------------------------------------------------

Monthly Income : ₹{profile.monthly_income}

Monthly Expenses : ₹{profile.monthly_expenses}

Savings : ₹{profile.savings}

Credit Score : {profile.credit_score}

Loan Details
--------------------------------------------------

Outstanding Balance : ₹{loan.remaining_balance}

Monthly EMI : ₹{loan.emi}

Interest Rate : {loan.interest_rate}%

Overdue Months : {loan.overdue_months}

Recommended Strategy
--------------------------------------------------

{strategy}

I sincerely request your bank to consider a mutually beneficial settlement.

Thank you for your understanding.

Yours faithfully,

Borrower
"""


# ==================================================
# AI Letter Generator
# ==================================================

def generate_ai_letter(profile, loan):

    prompt = f"""
You are a banking debt settlement expert.

Write a professional one-page loan settlement request letter.

Borrower Details
----------------
Monthly Income: ₹{profile.monthly_income}
Monthly Expenses: ₹{profile.monthly_expenses}
Savings: ₹{profile.savings}
Credit Score: {profile.credit_score}

Loan Details
------------
Lender: {loan.lender}
Loan Type: {loan.loan_type}
Outstanding Balance: ₹{loan.remaining_balance}
Monthly EMI: ₹{loan.emi}
Interest Rate: {loan.interest_rate}%
Overdue Months: {loan.overdue_months}

Write a formal, respectful settlement request letter.
"""

    response = generate_ai_response(prompt)

    if response["success"]:
        return response["response"]

    return generate_negotiation_letter(
        profile,
        loan,
        "Professional settlement request."
    )