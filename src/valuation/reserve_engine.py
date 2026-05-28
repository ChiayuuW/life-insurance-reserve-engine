import pandas as pd
from src.assumptions.mortality import get_mortality_rate


def calculate_expected_claim(face_amount: float, qx: float) -> float:
    return face_amount * qx


def calculate_simple_reserve(
    face_amount: float,
    annual_premium: float,
    qx: float,
    remaining_term: int,
    discount_rate: float = 0.03
) -> float:
    if remaining_term <= 0:
        return 0

    expected_annual_claim = face_amount * qx

    pv_future_claims = sum(
        expected_annual_claim / ((1 + discount_rate) ** t)
        for t in range(1, remaining_term + 1)
    )

    pv_future_premiums = sum(
        annual_premium / ((1 + discount_rate) ** t)
        for t in range(1, remaining_term + 1)
    )

    reserve = pv_future_claims - pv_future_premiums
    return max(reserve, 0)


def value_policies(policy_df: pd.DataFrame, mortality_table: pd.DataFrame) -> pd.DataFrame:
    results = []

    for _, policy in policy_df.iterrows():
        current_age = int(policy["valuation_year"] - policy["birth_year"])
        remaining_term = int(policy["policy_term"] - policy["policy_duration"])

        qx = get_mortality_rate(
            age=current_age,
            gender=policy["gender"],
            mortality_table=mortality_table
        )

        expected_claim = calculate_expected_claim(
            face_amount=policy["face_amount"],
            qx=qx
        )

        reserve = calculate_simple_reserve(
            face_amount=policy["face_amount"],
            annual_premium=policy["annual_premium"],
            qx=qx,
            remaining_term=remaining_term
        )

        results.append({
            "policy_id": policy["policy_id"],
            "insured_id": policy["insured_id"],
            "gender": policy["gender"],
            "birth_year": policy["birth_year"],
            "issue_age": policy["issue_age"],
            "current_age": current_age,
            "issue_year": policy["issue_year"],
            "valuation_year": policy["valuation_year"],
            "product_type": policy["product_type"],
            "policy_term": policy["policy_term"],
            "policy_duration": policy["policy_duration"],
            "remaining_term": remaining_term,
            "face_amount": policy["face_amount"],
            "annual_premium": policy["annual_premium"],
            "payment_mode": policy["payment_mode"],
            "smoking_status": policy["smoking_status"],
            "risk_class": policy["risk_class"],
            "policy_status": policy["policy_status"],
            "account_value": policy["account_value"],
            "claim_flag": policy["claim_flag"],
            "qx": qx,
            "expected_claim": expected_claim,
            "reserve": reserve
        })

    return pd.DataFrame(results)